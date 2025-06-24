#!/usr/bin/env python3
import os
import re
import requests
import yaml
from pathlib import Path

# Load configuration from YAML file
def load_config():
    """Load configuration from YAML file"""
    config_path = Path('.github/i18n-config.yml')

    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}")
        print("Please create the configuration file first.")
        exit(1)

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        exit(1)

# Load configuration
CONFIG = load_config()
API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY')

# Extract configuration values
TRANSLATION_ENABLED = CONFIG['translation']['enabled']
SOURCE_FILE = CONFIG['translation']['source_file']
OUTPUT_DIR = CONFIG['translation']['output_dir']
ENABLED_LANGUAGES = CONFIG['translation']['enabled_languages']
ADD_LANGUAGE_NAV = CONFIG['translation']['add_language_nav']
UPDATE_ROOT_README = CONFIG['translation'].get('update_root_readme', True)
OVERWRITE_MODE = CONFIG['translation'].get('overwrite_mode', 'auto')
LANGUAGES_INFO = CONFIG['languages']
PROTECTED_TERMS = CONFIG['protected_terms']
FOOTER_TEMPLATES = CONFIG['footer_templates']

def protect_terms(text):
    """Protect specific terms from being translated"""
    protected_text = text
    term_map = {}
    
    for i, term in enumerate(PROTECTED_TERMS):
        pattern = r'\b' + re.escape(term) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for j, match in enumerate(matches):
            placeholder = f"__PROTECTED_TERM_{i}_{j}__"
            protected_text = protected_text.replace(match, placeholder, 1)
            term_map[placeholder] = match
    
    return protected_text, term_map

def restore_terms(text, term_map):
    """Restore protected terms"""
    restored_text = text
    for placeholder, term in term_map.items():
        restored_text = restored_text.replace(placeholder, term)
    return restored_text

def is_file_manually_modified(target_file):
    """Check if file appears to be manually modified by looking for manual edit markers"""
    if not os.path.exists(target_file):
        return False

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for manual edit markers
        manual_markers = [
            "<!-- MANUAL EDIT -->",
            "<!-- DO NOT OVERWRITE -->",
            "<!-- MANUALLY MODIFIED -->",
            "<!-- CUSTOM CONTENT -->"
        ]

        for marker in manual_markers:
            if marker in content:
                return True

        # Check if the file doesn't have our standard footer (might be manually modified)
        if "i18n-Translator" not in content:
            return True

        return False

    except Exception:
        return False

def generate_dated_filename(original_filename):
    """Generate filename with current date suffix"""
    from datetime import datetime

    # Get current date in MMDDYY format
    date_suffix = datetime.now().strftime("%m%d%y")

    # Split filename and extension
    if '.' in original_filename:
        name_part, ext_part = original_filename.rsplit('.', 1)
        return f"{name_part}_{date_suffix}.{ext_part}"
    else:
        return f"{original_filename}_{date_suffix}"

def should_translate_file(source_file, target_file, language_code):
    """Check if translation is needed based on overwrite mode and file status"""

    # If file doesn't exist, always translate
    if not os.path.exists(target_file):
        return True, target_file, "File does not exist"

    # Check overwrite mode
    if OVERWRITE_MODE == "always":
        return True, target_file, "Overwrite mode: always"

    elif OVERWRITE_MODE == "never":
        return False, target_file, "Overwrite mode: never (file exists)"

    elif OVERWRITE_MODE == "create_new":
        # Create new file with date suffix
        new_filename = generate_dated_filename(target_file)
        return True, new_filename, f"Create new file with date suffix: {new_filename}"

    elif OVERWRITE_MODE == "auto":
        # Check if file was manually modified
        if is_file_manually_modified(target_file):
            return False, target_file, "File appears to be manually modified (skipping to preserve changes)"

        # Check file modification time
        source_mtime = os.path.getmtime(source_file)
        target_mtime = os.path.getmtime(target_file)

        if source_mtime > target_mtime:
            return True, target_file, "Source file is newer"
        else:
            return False, target_file, "Translation file is up to date"

    else:
        # Default to auto mode
        return should_translate_file(source_file, target_file, language_code)

def create_root_navigation():
    """Create navigation for root README.md based on current config"""
    if not ADD_LANGUAGE_NAV:
        return ""

    nav_lines = [
        "",
        "## 🌍 Available Languages",
        "",
        "| 🌐 Language | 📄 File | 📊 Status |",
        "|:-----------|:--------|:----------|",
        "| English | [README.md](README.md) | ✅ Current |"
    ]

    # Add languages based on current configuration
    for lang_code in ENABLED_LANGUAGES:
        if lang_code in LANGUAGES_INFO:
            lang_info = LANGUAGES_INFO[lang_code]
            name = lang_info['name']  # Already in format "Chinese (中文)"
            file_suffix = lang_info['file_suffix']
            filename = f"{OUTPUT_DIR}/README{file_suffix}.md"

            nav_lines.append(f"| {name} | [README{file_suffix}.md]({filename}) | ✅ Available |")

    nav_lines.extend([
        "",
        ""
    ])

    return "\n".join(nav_lines)

def preserve_markdown_structure(text):
    """Protect Markdown structure from being translated"""
    protected_text = text
    structure_map = {}

    # Protect code blocks
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    for i, block in enumerate(code_blocks):
        placeholder = f"__CODE_BLOCK_{i}__"
        protected_text = protected_text.replace(block, placeholder, 1)
        structure_map[placeholder] = block

    # Protect inline code
    inline_codes = re.findall(r'`[^`\n]+`', protected_text)
    for i, code in enumerate(inline_codes):
        placeholder = f"__INLINE_CODE_{i}__"
        protected_text = protected_text.replace(code, placeholder, 1)
        structure_map[placeholder] = code

    # Protect links
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', protected_text)
    for i, (text_part, url) in enumerate(links):
        full_link = f'[{text_part}]({url})'
        placeholder = f"__LINK_{i}__"
        protected_text = protected_text.replace(full_link, placeholder, 1)
        structure_map[placeholder] = full_link

    return protected_text, structure_map

def translate_text_with_rest_api(text, target_language):
    """Translate text using REST API"""
    if not API_KEY:
        raise ValueError("Google Translate API key not found")
    
    print(f"Translating to {target_language} using REST API...")
    
    # Google Translate REST API endpoint
    url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
    
    # Protect terms and Markdown structure
    protected_text, term_map = protect_terms(text)
    protected_text, structure_map = preserve_markdown_structure(protected_text)
    
    # Split into paragraphs for translation
    paragraphs = protected_text.split('\n\n')
    translated_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            try:
                print(f"  Translating paragraph {i+1}/{len(paragraphs)}")
                
                # Prepare request data
                data = {
                    'q': paragraph,
                    'target': target_language,
                    'source': 'en',
                    'format': 'text'
                }
                
                # Send request
                response = requests.post(url, data=data)
                response.raise_for_status()
                
                # Parse response
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                translated_paragraphs.append(translated_text)
                
            except Exception as e:
                print(f"  Warning: Translation error for paragraph {i+1}: {e}")
                translated_paragraphs.append(paragraph)  # Keep original text
        else:
            translated_paragraphs.append(paragraph)
    
    # Reassemble text
    translated_text = '\n\n'.join(translated_paragraphs)
    
    # Restore protected content
    translated_text = restore_terms(translated_text, structure_map)
    translated_text = restore_terms(translated_text, term_map)
    
    return translated_text

def add_translation_footer(content, language_code):
    """Add translation footer with developer info"""
    footer_template = FOOTER_TEMPLATES.get(language_code, FOOTER_TEMPLATES['default'])

    footer = f"""

---
> {footer_template}

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->"""

    return content + footer

def check_root_navigation_matches_config(content):
    """Check if root README.md navigation matches current configuration"""
    if not ADD_LANGUAGE_NAV:
        return True

    # Check if navigation exists
    has_nav = "## 🌍 Available Languages" in content
    if not has_nav:
        return False

    # Check if all configured languages are present in navigation
    for lang_code in ENABLED_LANGUAGES:
        if lang_code in LANGUAGES_INFO:
            lang_info = LANGUAGES_INFO[lang_code]
            file_suffix = lang_info['file_suffix']
            expected_link = f"README{file_suffix}.md"

            if expected_link not in content:
                print(f"  ⚠️  Language {lang_code} missing from navigation")
                return False

    return True

def ensure_root_navigation(content):
    """Ensure root README.md has correct navigation based on current config"""
    if not ADD_LANGUAGE_NAV:
        return content

    # Check if current navigation matches config
    if check_root_navigation_matches_config(content):
        print("  ✅ Root navigation is up to date")
        return content

    print("  🔄 Updating root navigation to match configuration")

    # Remove existing navigation if present
    if "## 🌍 Available Languages" in content:
        content = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', content, flags=re.DOTALL)
        content = re.sub(r'\n{3,}', '\n\n', content)

    # Get title
    title_match = re.match(r'^#\s+(.+)', content)
    title = title_match.group(1) if title_match else "README"

    # Create new navigation
    nav_content = create_root_navigation()

    # Insert navigation after title
    content_without_title = re.sub(r'^#\s+.+\n\n?', '', content)
    return f"# {title}\n{nav_content}{content_without_title}"

def fix_navigation_paths_for_locales(content):
    """Fix navigation paths for files inside locales folder"""
    # Fix paths from 'locales/README_xx.md' to './README_xx.md' for files inside locales
    content = re.sub(r'\[README(_[a-z]{2})\.md\]\(locales/README(_[a-z]{2})\.md\)',
                     r'[README\1.md](./README\2.md)', content)

    # Fix root README path from 'README.md' to '../README.md' for files inside locales
    content = re.sub(r'\[README\.md\]\(README\.md\)',
                     r'[README.md](../README.md)', content)

    return content

def fix_navigation_language_names(content):
    """Fix language names in navigation to maintain English format"""
    # Language name mappings to fix after translation
    language_fixes = {
        # Chinese translations back to English format
        r'\| 英语': '| English',
        r'\| 中国人': '| Chinese (中文)',
        r'\| 中文': '| Chinese (中文)',
        r'\| 日本人': '| Japanese (日本語)',
        r'\| 日语': '| Japanese (日本語)',
        r'\| 韩国人': '| Korean (한국어)',
        r'\| 韩语': '| Korean (한국어)',
        r'\| 西班牙语': '| Spanish (Español)',
        r'\| 法语': '| French (Français)',
        r'\| 俄语': '| Russian (Русский)',
        r'\| 德语': '| German (Deutsch)',
        r'\| 葡萄牙语': '| Portuguese (Português)',
        r'\| 阿拉伯语': '| Arabic (العربية)',

        # Fix table headers
        r'\| 🌐 语言': '| 🌐 Language',
        r'\| 📄 文件': '| 📄 File',
        r'\| 📊 状态': '| 📊 Status',
        r'\| ✅ 当前': '| ✅ Current',
        r'\| ✅ 可用': '| ✅ Available'
    }

    for pattern, replacement in language_fixes.items():
        content = re.sub(pattern, replacement, content)

    return content

def translate_entire_readme(content, language_code):
    """Translate entire README content (including navigation)"""
    print(f"  📝 Translating entire content to {LANGUAGES_INFO[language_code]['name']}...")

    # Translate the entire content including navigation
    translated_content = translate_text_with_rest_api(content, language_code)

    # Fix navigation paths for locales folder
    fixed_content = fix_navigation_paths_for_locales(translated_content)

    # Fix language names in navigation to maintain English format
    final_content = fix_navigation_language_names(fixed_content)

    return final_content

def test_api_connection():
    """Test API connection"""
    if not API_KEY:
        print("No API key found")
        return False
    
    try:
        print("Testing Google Translate API connection...")
        url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
        
        data = {
            'q': 'Hello',
            'target': 'ja',
            'source': 'en'
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        result = response.json()
        translated = result['data']['translations'][0]['translatedText']
        
        print(f"API connection successful!")
        print(f"Test translation: Hello -> {translated}")
        return True
        
    except Exception as e:
        print(f"API connection failed: {e}")
        return False

def main():
    """Main function"""
    print("Starting README translation process...")

    # Check if translation is enabled
    if not TRANSLATION_ENABLED:
        print("Translation is disabled in configuration (translation.enabled = false)")
        print("To enable translation, set 'translation.enabled: true' in .github/i18n-config.yml")
        return

    print(f"Configuration: {len(ENABLED_LANGUAGES)} languages enabled")

    # Test API connection
    if not test_api_connection():
        print("API test failed, exiting...")
        return

    if not os.path.exists(SOURCE_FILE):
        print(f"Source file {SOURCE_FILE} not found")
        return

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    # Read source file
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_content = f.read()

    print(f"Source content length: {len(source_content)} characters")

    # Track translation results
    translated_count = 0
    skipped_count = 0
    error_count = 0

    # Step 1: Ensure root README.md has correct navigation
    if ADD_LANGUAGE_NAV and UPDATE_ROOT_README:
        try:
            print("📋 Step 1: Ensuring root README.md has correct navigation...")

            # Check and update root navigation if needed
            updated_root_content = ensure_root_navigation(source_content)

            # Save updated root README if it changed
            if updated_root_content != source_content:
                with open(SOURCE_FILE, 'w', encoding='utf-8') as f:
                    f.write(updated_root_content)
                print("✅ Root README.md navigation updated")
                source_content = updated_root_content
            else:
                print("✅ Root README.md navigation is already correct")

        except Exception as e:
            print(f"❌ Error updating root README.md: {e}")
            return
    elif not UPDATE_ROOT_README:
        print("⚠️  Root README.md update is disabled in configuration")

    # Step 2: Create English version in locales directory (copy of root with footer)
    english_output = f"{OUTPUT_DIR}/README_en.md"
    try:
        print(f"📄 Creating English version: {english_output}")

        # Add English footer to the root content (which already has navigation)
        english_footer = """

---
> 🌐 This is the original English version | Translation tool: [i18n-Translator](https://github.com/1038lab/i18n-Translator)

<!-- ORIGINAL ENGLISH VERSION -->"""

        final_english_content = source_content + english_footer

        with open(english_output, 'w', encoding='utf-8') as f:
            f.write(final_english_content)

        print(f"✅ Created {english_output}")
        translated_count += 1

    except Exception as e:
        print(f"❌ Error creating English version: {e}")
        error_count += 1

    # Step 3: Translate entire README (including navigation) to each enabled language
    print(f"📚 Step 3: Translating to {len(ENABLED_LANGUAGES)} languages...")

    for lang_code in ENABLED_LANGUAGES:
        if lang_code not in LANGUAGES_INFO:
            print(f"⚠️  Warning: Language {lang_code} not found in language definitions")
            continue

        lang_info = LANGUAGES_INFO[lang_code]
        file_suffix = lang_info['file_suffix']
        output_file = f"{OUTPUT_DIR}/README{file_suffix}.md"

        try:
            # Check if translation is needed based on overwrite mode
            should_translate, actual_output_file, reason = should_translate_file(SOURCE_FILE, output_file, lang_code)

            if not should_translate:
                print(f"⏭️  Skipping {lang_code}: {reason}")
                skipped_count += 1
                continue

            print(f"\n🌐 Translating to {lang_info['name']} ({actual_output_file})...")
            if actual_output_file != output_file:
                print(f"  📝 Note: {reason}")

            # Translate entire content (including navigation)
            translated_content = translate_entire_readme(source_content, lang_code)

            # Add translation footer
            final_content = add_translation_footer(translated_content, lang_code)

            # Write to file
            with open(actual_output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            print(f"✅ Successfully created {actual_output_file}")
            translated_count += 1

        except Exception as e:
            print(f"❌ Error translating to {lang_code}: {e}")
            error_count += 1

    # Print summary
    print(f"\nTranslation process completed!")
    print(f"Results: {translated_count} translated, {skipped_count} skipped, {error_count} errors")

    if translated_count > 0:
        print(f"Translated files saved in: {OUTPUT_DIR}/")

    if error_count > 0:
        print("Some translations failed. Check the error messages above.")

if __name__ == "__main__":
    main()
