#!/usr/bin/env python3
"""
Free Translation Script for i18n-Translator
Uses Simple Google Translate (no API key required)
Based on WebApp's simple_translator.py implementation
"""

import os
import re
import time
import random
import requests
import yaml
from datetime import datetime

class SimpleGoogleTranslator:
    """Free Google Translate implementation"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def translate(self, text, target_lang='zh', source_lang='en'):
        """Translate text using Google Translate free service"""
        try:
            text = text.strip()
            if not text:
                return text
                
            # Split long text into chunks
            if len(text) > 4000:
                return self._translate_long_text(text, target_lang, source_lang)
            
            # Use Google Translate free API
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(0.1, 0.3))
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract translated text
                if result and len(result) > 0 and result[0]:
                    translated_parts = []
                    for part in result[0]:
                        if part and len(part) > 0:
                            translated_parts.append(part[0])
                    
                    translated_text = ''.join(translated_parts)
                    return translated_text if translated_text else text
            
            return text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def _translate_long_text(self, text, target_lang, source_lang):
        """Handle long text by splitting into chunks"""
        try:
            # Split by paragraphs
            paragraphs = text.split('\n\n')
            translated_paragraphs = []
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Further split if paragraph is too long
                    if len(paragraph) > 4000:
                        sentences = self._split_by_sentences(paragraph)
                        translated_sentences = []
                        
                        for sentence in sentences:
                            if sentence.strip():
                                translated = self.translate(sentence, target_lang, source_lang)
                                translated_sentences.append(translated)
                                time.sleep(0.2)  # Rate limiting
                        
                        translated_paragraphs.append(' '.join(translated_sentences))
                    else:
                        translated = self.translate(paragraph, target_lang, source_lang)
                        translated_paragraphs.append(translated)
                        time.sleep(0.2)  # Rate limiting
                else:
                    translated_paragraphs.append(paragraph)
            
            return '\n\n'.join(translated_paragraphs)
            
        except Exception as e:
            print(f"Long text translation error: {e}")
            return text
    
    def _split_by_sentences(self, text, max_length=3000):
        """Split text by sentences"""
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def test_connection(self):
        """Test if the service is available"""
        try:
            test_result = self.translate("Hello", "zh")
            return test_result != "Hello" and test_result.strip() != ""
        except:
            return False

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path='.github/i18n-config.yml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
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
    """Text processing utilities"""
    
    def __init__(self, protected_terms):
        self.protected_terms = protected_terms
    
    def protect_content(self, text):
        """Protect terms and code blocks from translation"""
        protected_text = text
        term_map = {}
        
        # Protect code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', protected_text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            protected_text = protected_text.replace(block, placeholder, 1)
            term_map[placeholder] = block
        
        # Protect inline code
        inline_codes = re.findall(r'`[^`\n]+`', protected_text)
        for i, code in enumerate(inline_codes):
            placeholder = f"__INLINE_{i}__"
            protected_text = protected_text.replace(code, placeholder, 1)
            term_map[placeholder] = code
        
        # Protect terms
        for i, term in enumerate(self.protected_terms):
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, protected_text, re.IGNORECASE)
            for j, match in enumerate(matches):
                placeholder = f"__TERM_{i}_{j}__"
                protected_text = protected_text.replace(match, placeholder, 1)
                term_map[placeholder] = match
        
        return protected_text, term_map
    
    def restore_content(self, text, term_map):
        """Restore protected terms"""
        restored_text = text
        for placeholder, original in term_map.items():
            restored_text = restored_text.replace(placeholder, original)
        return restored_text

class NavigationManager:
    """Language navigation management"""
    
    def __init__(self, config):
        self.config = config
    
    def create_navigation(self, for_root=False):
        """Create language navigation table"""
        nav_lines = [
            "## 🌍 Available Languages",
            "",
            "| 🌐 Language | 📄 File | 📊 Status |",
            "|-------------|---------|-----------|"
        ]
        
        for lang_code in self.config.enabled_languages:
            if lang_code in self.config.languages_info:
                lang_info = self.config.languages_info[lang_code]
                name = lang_info['name']
                file_suffix = lang_info['file_suffix']
                
                if for_root:
                    filename = f"{self.config.output_dir}/README{file_suffix}.md"
                else:
                    filename = f"./README{file_suffix}.md"
                
                nav_lines.append(f"| {name} | [README{file_suffix}.md]({filename}) | ✅ Available |")
        
        nav_lines.extend(["", ""])
        return "\n".join(nav_lines)
    
    def has_navigation(self, content):
        """Check if content has navigation section"""
        return "## 🌍 Available Languages" in content

class FreeTranslationRunner:
    """Main translation runner using free Google Translate"""
    
    def __init__(self):
        self.config = Config()
        self.translator = SimpleGoogleTranslator()
        self.text_processor = TextProcessor(self.config.protected_terms)
        self.nav_manager = NavigationManager(self.config)
    
    def translate_content(self, content, target_language):
        """Translate content to target language"""
        # Protect content
        protected_text, term_map = self.text_processor.protect_content(content)
        
        # Translate
        translated_text = self.translator.translate(protected_text, target_language, 'en')
        
        # Restore protected content
        final_text = self.text_processor.restore_content(translated_text, term_map)
        
        # Fix language names in navigation
        final_text = self.fix_language_names(final_text)
        
        return final_text
    
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

    def add_footer(self, content, language_code):
        """Add translation footer"""
        footer_template = self.config.footer_templates.get(
            language_code,
            self.config.footer_templates.get('default', '')
        )

        footer = f"""

---
> {footer_template}

<!-- AUTO-TRANSLATED -->"""

        return content + footer

    def should_translate(self, source_file, output_file):
        """Check if file should be translated based on overwrite mode"""
        if not os.path.exists(output_file):
            return True, output_file, "new file"

        mode = self.config.overwrite_mode

        if mode == "always":
            return True, output_file, "always overwrite"
        elif mode == "never":
            return False, output_file, "never overwrite"
        elif mode == "create_new":
            # Create new file with date suffix
            date_suffix = datetime.now().strftime("%m%d%y")
            base_name = output_file.replace('.md', f'_{date_suffix}.md')
            return True, base_name, f"create new with date: {date_suffix}"
        else:  # auto mode
            # Check if file appears manually modified
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()

                # Skip if has manual edit marker
                if "<!-- MANUAL EDIT -->" in existing_content:
                    return False, output_file, "manual edit marker found"

                # Skip if doesn't have our footer (likely manually modified)
                if "<!-- AUTO-TRANSLATED -->" not in existing_content:
                    return False, output_file, "no auto-translation marker"

                # Check if source is newer
                source_mtime = os.path.getmtime(source_file)
                output_mtime = os.path.getmtime(output_file)

                if source_mtime <= output_mtime:
                    return False, output_file, "source not newer"

                return True, output_file, "source is newer"

            except Exception:
                return True, output_file, "error reading existing file"

    def run(self):
        """Main translation process"""
        force_translate = os.environ.get('FORCE_TRANSLATE', 'false').lower() == 'true'

        if not self.config.enabled and not force_translate:
            print("Translation disabled in configuration")
            print("To enable: set 'translation.enabled: true' in config or use manual trigger with force option")
            return

        # Test connection
        print("Testing free Google Translate connection...")
        if not self.translator.test_connection():
            print("❌ Free Google Translate service is not available")
            print("This might be due to network restrictions or rate limiting")
            return

        print("✅ Free Google Translate service is available")

        if not os.path.exists(self.config.source_file):
            print(f"Source file {self.config.source_file} not found")
            return

        os.makedirs(self.config.output_dir, exist_ok=True)

        with open(self.config.source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()

        # Update root README with navigation if enabled
        if self.config.update_root_readme:
            try:
                if not self.nav_manager.has_navigation(source_content):
                    # Add navigation to root README
                    title_match = re.match(r'^#\s+(.+)', source_content)
                    title = title_match.group(1) if title_match else "README"
                    nav_content = self.nav_manager.create_navigation(for_root=True)
                    content_without_title = re.sub(r'^#\s+.+\n\n?', '', source_content)

                    updated_content = f"# {title}\n{nav_content}{content_without_title}"

                    with open(self.config.source_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)

                    source_content = updated_content
                    print("✅ Added language navigation to root README.md")
            except Exception as e:
                print(f"Warning: Could not update root README navigation: {e}")

        translated_count = 0
        skipped_count = 0
        error_count = 0

        # Create English version
        english_output = f"{self.config.output_dir}/README_en.md"
        try:
            should_create, actual_file, reason = self.should_translate(
                self.config.source_file, english_output)

            if should_create:
                # Fix navigation for locales folder
                english_content = source_content
                if self.nav_manager.has_navigation(english_content):
                    # Remove existing navigation and add locales navigation
                    content_no_nav = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', english_content, flags=re.DOTALL)
                    content_no_nav = re.sub(r'\n{3,}', '\n\n', content_no_nav)

                    title_match = re.match(r'^#\s+(.+)', content_no_nav)
                    title = title_match.group(1) if title_match else "README"
                    nav_content = self.nav_manager.create_navigation(for_root=False)
                    content_without_title = re.sub(r'^#\s+.+\n\n?', '', content_no_nav)

                    english_content = f"# {title}\n{nav_content}{content_without_title}"

                english_footer = """

---
> 🌐 This is the original English version | Translation tool: [i18n-Translator](https://github.com/1038lab/i18n-Translator)

<!-- ORIGINAL ENGLISH VERSION -->"""

                with open(actual_file, 'w', encoding='utf-8') as f:
                    f.write(english_content + english_footer)
                translated_count += 1
                print(f"✅ Created English version: {actual_file}")
            else:
                skipped_count += 1
                print(f"⏭️ Skipped English version: {reason}")
        except Exception as e:
            print(f"❌ Error creating English version: {e}")
            error_count += 1

        # Translate to other languages
        for lang_code in self.config.enabled_languages:
            if lang_code == 'en':  # Skip English as it's handled above
                continue

            if lang_code not in self.config.languages_info:
                print(f"⚠️ Language {lang_code} not found in configuration")
                continue

            lang_info = self.config.languages_info[lang_code]
            file_suffix = lang_info['file_suffix']
            output_file = f"{self.config.output_dir}/README{file_suffix}.md"

            try:
                should_create, actual_file, reason = self.should_translate(
                    self.config.source_file, output_file)

                if not should_create:
                    skipped_count += 1
                    print(f"⏭️ Skipped {lang_code}: {reason}")
                    continue

                print(f"🔄 Translating to {lang_info['name']}...")

                translated_content = self.translate_content(source_content, lang_code)
                final_content = self.add_footer(translated_content, lang_code)

                with open(actual_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)

                translated_count += 1
                print(f"✅ Translated to {lang_info['name']}: {actual_file}")

                # Add delay between translations to avoid rate limiting
                time.sleep(1)

            except Exception as e:
                print(f"❌ Error translating to {lang_code}: {e}")
                error_count += 1

        # Summary
        print(f"\n📊 Translation Summary:")
        print(f"✅ Translated: {translated_count}")
        print(f"⏭️ Skipped: {skipped_count}")
        print(f"❌ Errors: {error_count}")

        if translated_count > 0:
            print(f"\n🎉 Translation completed! Files saved to '{self.config.output_dir}/' folder")

        return translated_count > 0

if __name__ == "__main__":
    runner = FreeTranslationRunner()
    runner.run()
