#!/usr/bin/env python3

import os
import re
import yaml
import requests

class Config:
    def __init__(self, config_path='.github/i18n-config.yml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        translation = data.get('translation', {})
        self.enabled = translation.get('enabled', False)
        self.mode = translation.get('mode', 'free')
        self.source_file = translation.get('source_file', 'README.md')
        self.output_dir = translation.get('output_dir', 'locales')
        self.add_language_nav = translation.get('add_language_nav', True)
        self.update_root_readme = translation.get('update_root_readme', True)
        self.overwrite_mode = translation.get('overwrite_mode', 'auto')
        self.enabled_languages = translation.get('enabled_languages', ['en', 'zh'])
        
        self.languages_info = data.get('languages', {})
        self.protected_terms = data.get('protected_terms', [])
        self.footer_templates = data.get('footer_templates', {})

class GoogleTranslator:
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"

    def translate(self, text, target_lang, source_lang='auto'):
        if not text.strip():
            return text

        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': target_lang,
            'dt': 't',
            'q': text
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            result = response.json()
            if result and result[0]:
                translated_text = ''.join([item[0] for item in result[0] if item[0]])
                return translated_text
            return text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

class NavigationManager:
    def __init__(self, config):
        self.config = config

    def create_navigation(self, for_root=True):
        if not self.config.add_language_nav:
            return ""

        nav_lines = [
            "## 🌍 Available Languages",
            "",
            "| 🌐 Language | 📄 File | 📊 Status |",
            "|-------------|---------|-----------|"
        ]

        if for_root:
            nav_lines.append(f"| English | [README_en.md]({self.config.output_dir}/README_en.md) | ✅ Available |")
        else:
            nav_lines.append("| English | [README_en.md](./README_en.md) | ✅ Available |")

        for lang_code in self.config.enabled_languages:
            if lang_code != 'en' and lang_code in self.config.languages_info:
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
        return "## 🌍 Available Languages" in content

    def update_root_navigation(self, content):
        if not self.config.add_language_nav:
            return content

        if self.has_navigation(content):
            content = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', content, flags=re.DOTALL)
            content = re.sub(r'\n{3,}', '\n\n', content)

        title_match = re.match(r'^#\s+(.+)', content)
        title = title_match.group(1) if title_match else "README"
        nav_content = self.create_navigation(for_root=True)
        content_without_title = re.sub(r'^#\s+.+\n\n?', '', content)

        return f"# {title}\n{nav_content}{content_without_title}"

class FileManager:
    def __init__(self, overwrite_mode):
        self.overwrite_mode = overwrite_mode

    def should_translate(self, source_file, output_file):
        if not os.path.exists(output_file):
            return True, output_file, "new"

        if self.overwrite_mode == "always":
            return True, output_file, "overwrite"
        elif self.overwrite_mode == "never":
            return False, output_file, "skip"
        elif self.overwrite_mode == "create_new":
            from datetime import datetime
            timestamp = datetime.now().strftime("%m%d%y")
            base, ext = os.path.splitext(output_file)
            new_file = f"{base}_{timestamp}{ext}"
            return True, new_file, "create_new"
        else:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "<!-- MANUAL EDIT -->" in content:
                return False, output_file, "manual_edit"
            
            if not content.strip().endswith("Translation tool: [i18n](https://github.com/1038lab/i18n)"):
                return False, output_file, "no_footer"
            
            source_mtime = os.path.getmtime(source_file)
            output_mtime = os.path.getmtime(output_file)
            if source_mtime <= output_mtime:
                return False, output_file, "up_to_date"
            
            return True, output_file, "auto_update"

class ContentProcessor:
    def __init__(self, config):
        self.config = config
        self.translator = GoogleTranslator()
        self.nav_manager = NavigationManager(config)

    def protect_terms(self, text):
        term_map = {}
        protected_text = text

        for i, term in enumerate(self.config.protected_terms):
            placeholder = f"__PROTECTED_{i}__"
            protected_text = protected_text.replace(term, placeholder)
            term_map[placeholder] = term

        nav_pattern = r'## 🌍 Available Languages\s*\n\s*\n\s*\|[^|]*\|[^|]*\|[^|]*\|\s*\n\s*\|[-:|\s]*\|\s*\n(?:\s*\|[^|]*\|[^|]*\|[^|]*\|\s*\n)*'
        nav_tables = re.findall(nav_pattern, protected_text, re.MULTILINE)
        for i, table in enumerate(nav_tables):
            placeholder = f"__NAV_TABLE_{i}__"
            protected_text = protected_text.replace(table, placeholder, 1)
            term_map[placeholder] = table

        code_blocks = re.findall(r'```[\s\S]*?```', protected_text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__CODE_{i}__"
            protected_text = protected_text.replace(block, placeholder, 1)
            term_map[placeholder] = block

        inline_code = re.findall(r'`[^`]+`', protected_text)
        for i, code in enumerate(inline_code):
            placeholder = f"__INLINE_{i}__"
            protected_text = protected_text.replace(code, placeholder, 1)
            term_map[placeholder] = code

        return protected_text, term_map

    def restore_terms(self, text, term_map):
        for placeholder, original in term_map.items():
            text = text.replace(placeholder, original)
        return text

    def fix_translation_errors(self, text, language_code):
        """Fix common translation errors for free translation"""
        if language_code == 'zh':
            fixes = {
                r'\| 英语(?:\s*\([^)]*\))?': '| English',
                r'\| 中国人(?:\s*\([^)]*\))?': '| Chinese (中文)',
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
                r'✅ 可用的': '✅ Available',
                r'✅ 可得到': '✅ Available',
                r'## 🌍 可用语言': '## 🌍 Available Languages',
                r'## 🌍 可用的语言': '## 🌍 Available Languages',
                r'README_en\.md\]\(': 'README_en.md](',
                r'README_zh\.md\]\(': 'README_zh.md](',
                r'README_ja\.md\]\(': 'README_ja.md](',
                r'README_ko\.md\]\(': 'README_ko.md](',
            }
        elif language_code == 'ja':
            fixes = {
                r'\| 英語(?:\s*\([^)]*\))?': '| English',
                r'\| 中国語(?:\s*\([^)]*\))?': '| Chinese (中文)',
                r'\| 日本語(?:\s*\([^)]*\))?': '| Japanese (日本語)',
                r'\| 韓国語(?:\s*\([^)]*\))?': '| Korean (한국어)',
                r'\| スペイン語(?:\s*\([^)]*\))?': '| Spanish (Español)',
                r'\| フランス語(?:\s*\([^)]*\))?': '| French (Français)',
                r'\| ロシア語(?:\s*\([^)]*\))?': '| Russian (Русский)',
                r'\| ドイツ語(?:\s*\([^)]*\))?': '| German (Deutsch)',
                r'\| ポルトガル語(?:\s*\([^)]*\))?': '| Portuguese (Português)',
                r'\| アラビア語(?:\s*\([^)]*\))?': '| Arabic (العربية)',
                r'\| 🌐 言語': '| 🌐 Language',
                r'\| 📄 ファイル': '| 📄 File',
                r'\| 📊 状態': '| 📊 Status',
                r'✅ 利用可能': '✅ Available',
                r'## 🌍 利用可能な言語': '## 🌍 Available Languages',
                r'README_en\.md\]\(': 'README_en.md](',
                r'README_zh\.md\]\(': 'README_zh.md](',
                r'README_ja\.md\]\(': 'README_ja.md](',
                r'README_ko\.md\]\(': 'README_ko.md](',
            }
        elif language_code == 'ko':
            fixes = {
                r'\| 영어(?:\s*\([^)]*\))?': '| English',
                r'\| 중국어(?:\s*\([^)]*\))?': '| Chinese (中文)',
                r'\| 일본어(?:\s*\([^)]*\))?': '| Japanese (日本語)',
                r'\| 한국어(?:\s*\([^)]*\))?': '| Korean (한국어)',
                r'\| 스페인어(?:\s*\([^)]*\))?': '| Spanish (Español)',
                r'\| 프랑스어(?:\s*\([^)]*\))?': '| French (Français)',
                r'\| 러시아어(?:\s*\([^)]*\))?': '| Russian (Русский)',
                r'\| 독일어(?:\s*\([^)]*\))?': '| German (Deutsch)',
                r'\| 포르투갈어(?:\s*\([^)]*\))?': '| Portuguese (Português)',
                r'\| 아랍어(?:\s*\([^)]*\))?': '| Arabic (العربية)',
                r'\| 🌐 언어': '| 🌐 Language',
                r'\| 📄 파일': '| 📄 File',
                r'\| 📊 상태': '| 📊 Status',
                r'✅ 사용 가능': '✅ Available',
                r'## 🌍 사용 가능한 언어': '## 🌍 Available Languages',
                r'README_en\.md\]\(': 'README_en.md](',
                r'README_zh\.md\]\(': 'README_zh.md](',
                r'README_ja\.md\]\(': 'README_ja.md](',
                r'README_ko\.md\]\(': 'README_ko.md](',
            }
        else:
            fixes = {}

        for pattern, replacement in fixes.items():
            text = re.sub(pattern, replacement, text)

        return text

    def translate_content(self, content, language_code):
        if self.nav_manager.has_navigation(content):
            content_no_nav = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', content, flags=re.DOTALL)
            content_no_nav = re.sub(r'\n{3,}', '\n\n', content_no_nav)

            title_match = re.match(r'^#\s+(.+)', content_no_nav)
            title = title_match.group(1) if title_match else "README"
            nav_content = self.nav_manager.create_navigation(for_root=False)
            content_without_title = re.sub(r'^#\s+.+\n\n?', '', content_no_nav)

            content_to_translate = f"# {title}\n{content_without_title}"
        else:
            content_to_translate = content
            nav_content = ""

        protected_content, term_map = self.protect_terms(content_to_translate)
        translated_content = self.translator.translate(protected_content, language_code)
        restored_content = self.restore_terms(translated_content, term_map)
        fixed_content = self.fix_translation_errors(restored_content, language_code)

        if nav_content:
            title_match = re.match(r'^#\s+(.+)', fixed_content)
            title = title_match.group(1) if title_match else "README"
            content_without_title = re.sub(r'^#\s+.+\n\n?', '', fixed_content)
            final_content = f"# {title}\n{nav_content}{content_without_title}"
        else:
            final_content = fixed_content

        return final_content

    def add_footer(self, content, language_code):
        footer_template = self.config.footer_templates.get(language_code, 
                         self.config.footer_templates.get('default', 
                         "🌐 This document was automatically translated. Please refer to the [English README](./README_en.md) for accuracy | Translation tool: [i18n](https://github.com/1038lab/i18n)"))
        
        return f"{content}\n\n---\n\n{footer_template}\n"

class TranslationManager:
    def __init__(self, config):
        self.config = config
        self.processor = ContentProcessor(config)
        self.nav_manager = NavigationManager(config)
        self.file_manager = FileManager(config.overwrite_mode)

    def run(self):
        if not os.path.exists(self.config.source_file):
            print(f"Source file {self.config.source_file} not found")
            return

        os.makedirs(self.config.output_dir, exist_ok=True)

        with open(self.config.source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()

        if self.config.add_language_nav and self.config.update_root_readme:
            try:
                updated_content = self.nav_manager.update_root_navigation(source_content)
                if updated_content != source_content:
                    with open(self.config.source_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    source_content = updated_content
            except Exception as e:
                print(f"Error updating root README: {e}")
                return

        english_output = f"{self.config.output_dir}/README_en.md"
        try:
            english_content = source_content
            if self.nav_manager.has_navigation(english_content):
                content_no_nav = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', english_content, flags=re.DOTALL)
                content_no_nav = re.sub(r'\n{3,}', '\n\n', content_no_nav)

                title_match = re.match(r'^#\s+(.+)', content_no_nav)
                title = title_match.group(1) if title_match else "README"
                nav_content = self.nav_manager.create_navigation(for_root=False)
                content_without_title = re.sub(r'^#\s+.+\n\n?', '', content_no_nav)

                english_content = f"# {title}\n{nav_content}{content_without_title}"

            final_english_content = self.processor.add_footer(english_content, 'en')
            
            with open(english_output, 'w', encoding='utf-8') as f:
                f.write(final_english_content)

        except Exception as e:
            print(f"Error creating English version: {e}")

        for lang_code in self.config.enabled_languages:
            if lang_code == 'en' or lang_code not in self.config.languages_info:
                continue

            lang_info = self.config.languages_info[lang_code]
            file_suffix = lang_info['file_suffix']
            output_file = f"{self.config.output_dir}/README{file_suffix}.md"

            try:
                should_translate, actual_file, reason = self.file_manager.should_translate(
                    self.config.source_file, output_file)

                if not should_translate:
                    continue

                translated_content = self.processor.translate_content(source_content, lang_code)
                final_content = self.processor.add_footer(translated_content, lang_code)

                with open(actual_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)

            except Exception as e:
                print(f"Error translating to {lang_code}: {e}")

if __name__ == "__main__":
    config = Config()
    manager = TranslationManager(config)
    manager.run()
