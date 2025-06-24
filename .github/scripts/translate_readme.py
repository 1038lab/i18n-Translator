#!/usr/bin/env python3
import os
import re
import requests
import yaml
from pathlib import Path
from datetime import datetime

class TranslationConfig:
    def __init__(self):
        self.config = self._load_config()
        self.api_key = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
        self._validate_config()

    def _load_config(self):
        config_path = Path('.github/i18n-config.yml')
        if not config_path.exists():
            raise FileNotFoundError("Configuration file not found: .github/i18n-config.yml")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")

    def _validate_config(self):
        required_keys = ['translation', 'languages', 'protected_terms', 'footer_templates']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration key: {key}")

        if not self.api_key:
            raise ValueError("GOOGLE_TRANSLATE_API_KEY environment variable not set")

    @property
    def enabled(self): return self.config['translation']['enabled']
    @property
    def source_file(self): return self.config['translation']['source_file']
    @property
    def output_dir(self): return self.config['translation']['output_dir']
    @property
    def enabled_languages(self): return self.config['translation']['enabled_languages']
    @property
    def add_language_nav(self): return self.config['translation']['add_language_nav']
    @property
    def update_root_readme(self): return self.config['translation'].get('update_root_readme', True)
    @property
    def overwrite_mode(self): return self.config['translation'].get('overwrite_mode', 'auto')
    @property
    def languages_info(self): return self.config['languages']
    @property
    def protected_terms(self): return self.config['protected_terms']
    @property
    def footer_templates(self): return self.config['footer_templates']

class TextProcessor:
    def __init__(self, protected_terms):
        self.protected_terms = protected_terms

    def protect_content(self, text):
        """Protect terms and markdown structure from translation"""
        protected_text = text
        term_map = {}

        # Protect terms
        for i, term in enumerate(self.protected_terms):
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, protected_text, re.IGNORECASE)
            for j, match in enumerate(matches):
                placeholder = f"__TERM_{i}_{j}__"
                protected_text = protected_text.replace(match, placeholder, 1)
                term_map[placeholder] = match

        # Protect code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', protected_text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__CODE_{i}__"
            protected_text = protected_text.replace(block, placeholder, 1)
            term_map[placeholder] = block

        # Protect inline code and links
        inline_codes = re.findall(r'`[^`\n]+`', protected_text)
        for i, code in enumerate(inline_codes):
            placeholder = f"__INLINE_{i}__"
            protected_text = protected_text.replace(code, placeholder, 1)
            term_map[placeholder] = code

        links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', protected_text)
        for i, (text_part, url) in enumerate(links):
            full_link = f'[{text_part}]({url})'
            placeholder = f"__LINK_{i}__"
            protected_text = protected_text.replace(full_link, placeholder, 1)
            term_map[placeholder] = full_link

        return protected_text, term_map

    def restore_content(self, text, term_map):
        """Restore protected content"""
        for placeholder, original in term_map.items():
            text = text.replace(placeholder, original)
        return text

class FileManager:
    def __init__(self, overwrite_mode):
        self.overwrite_mode = overwrite_mode

    def is_manually_modified(self, file_path):
        """Check if file was manually modified"""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            manual_markers = ["<!-- MANUAL EDIT -->", "<!-- DO NOT OVERWRITE -->",
                            "<!-- MANUALLY MODIFIED -->", "<!-- CUSTOM CONTENT -->"]

            return any(marker in content for marker in manual_markers) or "i18n-Translator" not in content
        except Exception:
            return False

    def generate_dated_filename(self, filename):
        """Generate filename with date suffix"""
        date_suffix = datetime.now().strftime("%m%d%y")
        if '.' in filename:
            name_part, ext_part = filename.rsplit('.', 1)
            return f"{name_part}_{date_suffix}.{ext_part}"
        return f"{filename}_{date_suffix}"

    def should_translate(self, source_file, target_file):
        """Determine if file should be translated based on overwrite mode"""
        if not os.path.exists(target_file):
            return True, target_file, "File does not exist"

        if self.overwrite_mode == "always":
            return True, target_file, "Overwrite mode: always"
        elif self.overwrite_mode == "never":
            return False, target_file, "Overwrite mode: never"
        elif self.overwrite_mode == "create_new":
            new_filename = self.generate_dated_filename(target_file)
            return True, new_filename, f"Creating new file: {new_filename}"
        elif self.overwrite_mode == "auto":
            if self.is_manually_modified(target_file):
                return False, target_file, "File manually modified"

            source_mtime = os.path.getmtime(source_file)
            target_mtime = os.path.getmtime(target_file)

            if source_mtime > target_mtime:
                return True, target_file, "Source file is newer"
            return False, target_file, "Translation is up to date"

        return True, target_file, "Default behavior"

class NavigationManager:
    def __init__(self, config):
        self.config = config

    def create_navigation(self):
        """Create language navigation table"""
        if not self.config.add_language_nav:
            return ""

        nav_lines = [
            "", "## 🌍 Available Languages", "",
            "| 🌐 Language | 📄 File | 📊 Status |",
            "|:-----------|:--------|:----------|",
            "| English | [README.md](README.md) | ✅ Current |"
        ]

        for lang_code in self.config.enabled_languages:
            if lang_code in self.config.languages_info:
                lang_info = self.config.languages_info[lang_code]
                name = lang_info['name']
                file_suffix = lang_info['file_suffix']
                filename = f"{self.config.output_dir}/README{file_suffix}.md"
                nav_lines.append(f"| {name} | [README{file_suffix}.md]({filename}) | ✅ Available |")

        nav_lines.extend(["", ""])
        return "\n".join(nav_lines)

    def has_navigation(self, content):
        """Check if content has navigation section"""
        return "## 🌍 Available Languages" in content

    def update_root_navigation(self, content):
        """Update navigation in root README"""
        if not self.config.add_language_nav:
            return content

        # Remove existing navigation
        if self.has_navigation(content):
            content = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', content, flags=re.DOTALL)
            content = re.sub(r'\n{3,}', '\n\n', content)

        # Get title and insert navigation
        title_match = re.match(r'^#\s+(.+)', content)
        title = title_match.group(1) if title_match else "README"
        nav_content = self.create_navigation()
        content_without_title = re.sub(r'^#\s+.+\n\n?', '', content)

        return f"# {title}\n{nav_content}{content_without_title}"

    def fix_navigation_paths(self, content):
        """Fix navigation paths for files in locales folder"""
        content = re.sub(r'\[README(_[a-z]{2})\.md\]\(locales/README(_[a-z]{2})\.md\)',
                        r'[README\1.md](./README\2.md)', content)
        content = re.sub(r'\[README\.md\]\(README\.md\)', r'[README.md](../README.md)', content)
        return content

    def fix_language_names(self, content):
        """Fix translated language names back to English format"""
        language_fixes = {
            r'\| 英语(?!\s*\()': '| English',
            r'\| 中国人(?:\s*\([^)]*\))?': '| Chinese (中文)',
            r'\| 中文(?!\s*\([^)]*\))': '| Chinese (中文)',
            r'\| 日本人(?:\s*\([^)]*\))?': '| Japanese (日本語)',
            r'\| 韩国人(?:\s*\([^)]*\))?': '| Korean (한국어)',
            r'\| 西班牙语(?:\s*\([^)]*\))?': '| Spanish (Español)',
            r'\| 法语(?:\s*\([^)]*\))?': '| French (Français)',
            r'\| 俄语(?:\s*\([^)]*\))?': '| Russian (Русский)',
            r'\| 德语(?:\s*\([^)]*\))?': '| German (Deutsch)',
            r'\| 葡萄牙语(?:\s*\([^)]*\))?': '| Portuguese (Português)',
            r'\| 阿拉伯语(?:\s*\([^)]*\))?': '| Arabic (العربية)',
            r'\| 🌐 语言': '| 🌐 Language',
            r'\| 📄 文件': '| 📄 File',
            r'\| 📊 状态': '| 📊 Status',
            r'\| ✅ 当前': '| ✅ Current',
            r'\| ✅ 可用': '| ✅ Available'
        }

        for pattern, replacement in language_fixes.items():
            content = re.sub(pattern, replacement, content)
        return content

class Translator:
    def __init__(self, api_key, text_processor):
        self.api_key = api_key
        self.text_processor = text_processor
        self.api_url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"

    def test_connection(self):
        """Test API connection with simple translation"""
        try:
            print("Testing Google Translate API connection...")
            response = requests.post(self.api_url, data={
                'q': 'Hello', 'target': 'ja', 'source': 'en'
            })
            response.raise_for_status()
            result = response.json()
            translated = result['data']['translations'][0]['translatedText']
            print(f"API connection successful! Test: Hello -> {translated}")
            return True
        except Exception as e:
            print(f"API connection failed: {e}")
            return False

    def translate_text(self, text, target_language):
        """Translate text to target language"""
        print(f"Translating to {target_language}...")

        # Protect content from translation
        protected_text, term_map = self.text_processor.protect_content(text)

        # Split into paragraphs and translate
        paragraphs = protected_text.split('\n\n')
        translated_paragraphs = []

        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                try:
                    print(f"  Translating paragraph {i+1}/{len(paragraphs)}")
                    response = requests.post(self.api_url, data={
                        'q': paragraph, 'target': target_language, 'source': 'en', 'format': 'text'
                    })
                    response.raise_for_status()
                    result = response.json()
                    translated_paragraphs.append(result['data']['translations'][0]['translatedText'])
                except Exception as e:
                    print(f"  Warning: Translation error for paragraph {i+1}: {e}")
                    translated_paragraphs.append(paragraph)
            else:
                translated_paragraphs.append(paragraph)

        # Restore protected content
        translated_text = '\n\n'.join(translated_paragraphs)
        return self.text_processor.restore_content(translated_text, term_map)

class TranslationManager:
    def __init__(self):
        self.config = TranslationConfig()
        self.text_processor = TextProcessor(self.config.protected_terms)
        self.translator = Translator(self.config.api_key, self.text_processor)
        self.nav_manager = NavigationManager(self.config)
        self.file_manager = FileManager(self.config.overwrite_mode)

    def add_footer(self, content, language_code):
        """Add translation footer"""
        footer_template = self.config.footer_templates.get(language_code,
                                                          self.config.footer_templates['default'])
        footer = f"""

---
> {footer_template}

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->"""
        return content + footer

    def translate_content(self, content, language_code):
        """Translate content and fix navigation"""
        lang_name = self.config.languages_info[language_code]['name']
        print(f"  📝 Translating content to {lang_name}...")

        # Translate entire content
        translated = self.translator.translate_text(content, language_code)

        # Fix navigation paths and language names
        fixed_content = self.nav_manager.fix_navigation_paths(translated)
        return self.nav_manager.fix_language_names(fixed_content)

    def detect_orphaned_files(self):
        """Detect orphaned translation files"""
        if not os.path.exists(self.config.output_dir):
            return []

        orphaned = []
        for file in os.listdir(self.config.output_dir):
            if file.startswith('README_') and file.endswith('.md') and file != 'README_en.md':
                lang_code = file.replace('README_', '').replace('.md', '')
                if lang_code not in self.config.enabled_languages:
                    file_path = os.path.join(self.config.output_dir, file)
                    orphaned.append((lang_code, file_path))
        return orphaned

    def handle_orphaned_files(self, orphaned_files):
        """Report orphaned files"""
        if not orphaned_files:
            return

        print(f"\n🗂️  Found {len(orphaned_files)} orphaned translation file(s):")
        for lang_code, file_path in orphaned_files:
            lang_name = self.config.languages_info.get(lang_code, {}).get('name', lang_code)
            print(f"  📄 {file_path} ({lang_name}) - no longer enabled")
        print("  💡 These files are preserved but no longer updated.")

    def run(self):
        """Main translation process"""
        print("Starting README translation process...")

        # Check if translation is enabled
        if not self.config.enabled:
            print("Translation is disabled in configuration")
            print("To enable: set 'translation.enabled: true' in .github/i18n-config.yml")
            return

        print(f"Configuration: {len(self.config.enabled_languages)} languages enabled")

        # Test API connection
        if not self.translator.test_connection():
            print("API test failed, exiting...")
            return

        # Check source file
        if not os.path.exists(self.config.source_file):
            print(f"Source file {self.config.source_file} not found")
            return

        # Create output directory
        os.makedirs(self.config.output_dir, exist_ok=True)
        print(f"Output directory: {self.config.output_dir}")

        # Handle orphaned files
        orphaned_files = self.detect_orphaned_files()
        if orphaned_files:
            self.handle_orphaned_files(orphaned_files)

        # Read source content
        with open(self.config.source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()

        print(f"Source content length: {len(source_content)} characters")

        # Track results
        translated_count = 0
        skipped_count = 0
        error_count = 0

        # Step 1: Update root navigation
        if self.config.add_language_nav and self.config.update_root_readme:
            try:
                print("📋 Step 1: Updating root README navigation...")
                updated_content = self.nav_manager.update_root_navigation(source_content)

                if updated_content != source_content:
                    with open(self.config.source_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print("✅ Root README navigation updated")
                    source_content = updated_content
                else:
                    print("✅ Root README navigation is current")
            except Exception as e:
                print(f"❌ Error updating root README: {e}")
                return

        # Step 2: Create English version
        english_output = f"{self.config.output_dir}/README_en.md"
        try:
            print(f"📄 Creating English version: {english_output}")
            english_footer = """

---
> 🌐 This is the original English version | Translation tool: [i18n-Translator](https://github.com/1038lab/i18n-Translator)

<!-- ORIGINAL ENGLISH VERSION -->"""

            with open(english_output, 'w', encoding='utf-8') as f:
                f.write(source_content + english_footer)

            print(f"✅ Created {english_output}")
            translated_count += 1
        except Exception as e:
            print(f"❌ Error creating English version: {e}")
            error_count += 1

        # Step 3: Translate to each language
        print(f"📚 Step 3: Translating to {len(self.config.enabled_languages)} languages...")

        for lang_code in self.config.enabled_languages:
            if lang_code not in self.config.languages_info:
                print(f"⚠️  Warning: Language {lang_code} not found in definitions")
                continue

            lang_info = self.config.languages_info[lang_code]
            file_suffix = lang_info['file_suffix']
            output_file = f"{self.config.output_dir}/README{file_suffix}.md"

            try:
                # Check if translation needed
                should_translate, actual_file, reason = self.file_manager.should_translate(
                    self.config.source_file, output_file)

                if not should_translate:
                    print(f"⏭️  Skipping {lang_code}: {reason}")
                    skipped_count += 1
                    continue

                print(f"\n🌐 Translating to {lang_info['name']} ({actual_file})...")
                if actual_file != output_file:
                    print(f"  📝 Note: {reason}")

                # Translate content
                translated_content = self.translate_content(source_content, lang_code)
                final_content = self.add_footer(translated_content, lang_code)

                # Write file
                with open(actual_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)

                print(f"✅ Successfully created {actual_file}")
                translated_count += 1

            except Exception as e:
                print(f"❌ Error translating to {lang_code}: {e}")
                error_count += 1

        # Print summary
        print(f"\nTranslation process completed!")
        print(f"Results: {translated_count} translated, {skipped_count} skipped, {error_count} errors")

        if translated_count > 0:
            print(f"Translated files saved in: {self.config.output_dir}/")
        if error_count > 0:
            print("Some translations failed. Check error messages above.")

def main():
    """Entry point"""
    try:
        manager = TranslationManager()
        manager.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
