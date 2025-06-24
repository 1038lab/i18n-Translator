#!/usr/bin/env python3
"""
Simple README translator - Clean and focused
"""

import os
import re
import sys
import yaml
import requests
from datetime import datetime

def load_config():
    """Load configuration"""
    with open('.github/i18n-config.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_api_key():
    """Get API key"""
    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_TRANSLATE_API_KEY not found")
        sys.exit(1)
    return api_key

def translate_text(text, target_language, api_key):
    """Translate text using Google Translate API"""
    url = "https://translation.googleapis.com/language/translate/v2"
    
    params = {
        'key': api_key,
        'q': text,
        'target': target_language,
        'source': 'en',
        'format': 'text'
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        result = response.json()
        return result['data']['translations'][0]['translatedText']
    else:
        print(f"❌ Translation failed: {response.status_code}")
        return text

def protect_terms(text, protected_terms):
    """Protect terms from translation"""
    term_map = {}
    protected_text = text
    
    for i, term in enumerate(protected_terms):
        pattern = r'\b' + re.escape(term) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for j, match in enumerate(matches):
            placeholder = f"__TERM_{i}_{j}__"
            protected_text = protected_text.replace(match, placeholder, 1)
            term_map[placeholder] = match
    
    return protected_text, term_map

def restore_terms(text, term_map):
    """Restore protected terms"""
    for placeholder, term in term_map.items():
        text = text.replace(placeholder, term)
    return text

def create_navigation(current_lang=None):
    """Create language navigation"""
    config = load_config()
    enabled_languages = config.get('enabled_languages', [])
    languages_info = config.get('languages', {})
    
    nav_lines = [
        "## 🌍 Available Languages",
        "",
        "| 🌐 Language | 📄 File | 📊 Status |",
        "|:-----------|:--------|:----------|"
    ]
    
    # Add English
    if current_lang == 'en':
        nav_lines.append("| English | [README_en.md](README_en.md) | ✅ Current |")
    else:
        nav_lines.append("| English | [README_en.md](README_en.md) | ✅ Available |")
    
    # Add other languages
    for lang_code in enabled_languages:
        if lang_code in languages_info:
            lang_info = languages_info[lang_code]
            name = lang_info['name']
            file_suffix = lang_info['file_suffix']
            
            if current_lang == lang_code:
                status = "✅ Current"
            else:
                status = "✅ Available"
                
            nav_lines.append(f"| {name} | [README{file_suffix}.md](locales/README{file_suffix}.md) | {status} |")
    
    nav_lines.extend(["", ""])
    return "\n".join(nav_lines)

def add_navigation_to_root():
    """Add navigation to root README.md"""
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if navigation already exists
    if "## 🌍 Available Languages" in content:
        # Remove existing navigation
        lines = content.split('\n')
        new_lines = []
        skip_nav = False
        
        for line in lines:
            if line.startswith("## 🌍 Available Languages"):
                skip_nav = True
                continue
            elif skip_nav and line.startswith("## ") and "Available Languages" not in line:
                skip_nav = False
                new_lines.append(line)
            elif not skip_nav:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
    
    # Add new navigation after title
    lines = content.split('\n')
    title_line = 0
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title_line = i
            break
    
    # Insert navigation after title
    navigation = create_navigation()
    lines.insert(title_line + 1, "")
    lines.insert(title_line + 2, navigation)
    
    new_content = '\n'.join(lines)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Updated root README navigation")
    return new_content

def translate_file(source_content, target_language, api_key, protected_terms):
    """Translate entire file content"""
    print(f"  📝 Translating content...")
    
    # Protect terms
    protected_content, term_map = protect_terms(source_content, protected_terms)
    
    # Split into paragraphs for better translation
    paragraphs = protected_content.split('\n\n')
    translated_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            print(f"    Translating paragraph {i+1}/{len(paragraphs)}")
            translated = translate_text(paragraph, target_language, api_key)
            translated_paragraphs.append(translated)
        else:
            translated_paragraphs.append(paragraph)
    
    # Reassemble
    translated_content = '\n\n'.join(translated_paragraphs)
    
    # Restore terms
    final_content = restore_terms(translated_content, term_map)
    
    return final_content

def add_footer(content, language_code, footer_templates):
    """Add translation footer"""
    footer = footer_templates.get(language_code, footer_templates.get('default', ''))
    if footer:
        return content + '\n\n---\n\n' + footer
    return content

def main():
    """Main function"""
    print("🚀 Starting README translation...")
    
    # Load config
    config = load_config()
    
    # Check if translation is enabled
    if not config['translation']['enabled']:
        print("❌ Translation is disabled in configuration")
        return
    
    # Get API key
    api_key = get_api_key()
    
    # Get configuration
    enabled_languages = config['enabled_languages']
    languages_info = config['languages']
    protected_terms = config['protected_terms']
    footer_templates = config['footer_templates']
    output_dir = config['translation']['output_dir']
    
    print(f"📋 Enabled languages: {', '.join(enabled_languages)}")
    
    # Update root README navigation
    add_navigation_to_root()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read source file
    with open('README.md', 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    # Create English version
    english_nav = create_navigation('en')
    english_content = re.sub(r'## 🌍 Available Languages.*?(?=## |\Z)', english_nav, source_content, flags=re.DOTALL)
    english_footer = add_footer(english_content, 'en', footer_templates)
    
    with open(f'{output_dir}/README_en.md', 'w', encoding='utf-8') as f:
        f.write(english_footer)
    print("✅ Created English version")
    
    # Translate to other languages
    for lang_code in enabled_languages:
        if lang_code in languages_info:
            lang_info = languages_info[lang_code]
            file_suffix = lang_info['file_suffix']
            output_file = f'{output_dir}/README{file_suffix}.md'
            
            print(f"\n🌐 Translating to {lang_info['name']}...")
            
            # Translate content
            translated_content = translate_file(source_content, lang_code, api_key, protected_terms)
            
            # Add navigation for this language
            nav = create_navigation(lang_code)
            final_content = re.sub(r'## 🌍 Available Languages.*?(?=## |\Z)', nav, translated_content, flags=re.DOTALL)
            
            # Add footer
            final_content = add_footer(final_content, lang_code, footer_templates)
            
            # Write file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✅ Created {output_file}")
    
    print("\n🎉 Translation completed!")

if __name__ == "__main__":
    main()
