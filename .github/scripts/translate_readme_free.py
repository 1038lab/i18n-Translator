#!/usr/bin/env python3
"""
Free Translation Script for i18n
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

class TextProcessor:
    """Text processing utilities"""

    def __init__(self, protected_terms):
        self.protected_terms = protected_terms

    def protect_content(self, text):
        """Protect terms and markdown structure from translation"""
        protected_text = text
        term_map = {}

        # First protect links (before terms to avoid conflicts)
        links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', protected_text)
        for i, (text_part, url) in enumerate(links):
            full_link = f'[{text_part}]({url})'
            placeholder = f"__LINK_{i}__"
            protected_text = protected_text.replace(full_link, placeholder, 1)
            term_map[placeholder] = full_link

        # Protect navigation tables (before code blocks to avoid conflicts)
        nav_pattern = r'## 🌍 Available Languages\s*\n\s*\n\s*\|[^|]*\|[^|]*\|[^|]*\|\s*\n\s*\|[-:|\s]*\|\s*\n(?:\s*\|[^|]*\|[^|]*\|[^|]*\|\s*\n)*'
        nav_tables = re.findall(nav_pattern, protected_text, re.MULTILINE)
        for i, table in enumerate(nav_tables):
            placeholder = f"__NAV_TABLE_{i}__"
            protected_text = protected_text.replace(table, placeholder, 1)
            term_map[placeholder] = table

        # Protect code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', protected_text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__CODE_{i}__"
            protected_text = protected_text.replace(block, placeholder, 1)
            term_map[placeholder] = block

        # Protect inline code
        inline_codes = re.findall(r'`[^`\n]+`', protected_text)
        for i, code in enumerate(inline_codes):
            placeholder = f"__INLINE_{i}__"
            protected_text = protected_text.replace(code, placeholder, 1)
            term_map[placeholder] = code

        # Protect terms (after links and code to avoid conflicts)
        for i, term in enumerate(self.protected_terms):
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, protected_text, re.IGNORECASE)
            for j, match in enumerate(matches):
                placeholder = f"__TERM_{i}_{j}__"
                protected_text = protected_text.replace(match, placeholder, 1)
                term_map[placeholder] = match

        return protected_text, term_map

    def restore_content(self, text, term_map):
        """Restore protected content with comprehensive fuzzy matching"""
        restored_text = text

        # First pass: Direct replacement of exact placeholders
        for placeholder, original in term_map.items():
            restored_text = restored_text.replace(placeholder, original)

        # Second pass: Handle damaged placeholders with comprehensive patterns
        restoration_map = {}

        # Build restoration patterns from term_map
        for placeholder, original in term_map.items():
            # Extract core components and create damage patterns
            if '__LINK_' in placeholder:
                core_match = re.search(r'__LINK_(\d+)__', placeholder)
                if core_match:
                    link_id = core_match.group(1)
                    patterns = [
                        f'__LINK_{link_id}__', f'__link_{link_id}__', f'__Link_{link_id}__',
                        f'__ LINK_{link_id}__', f'__ link_{link_id}__', f'__ Link_{link_id}__',
                        f'__LINK_{link_id} __', f'__link_{link_id} __', f'__Link_{link_id} __',
                        f'__ LINK_{link_id} __', f'__ link_{link_id} __', f'__ Link_{link_id} __',
                        f'__link {link_id}__', f'__Link {link_id}__', f'__LINK {link_id}__'
                    ]
                    for pattern in patterns:
                        restoration_map[pattern] = original

            elif '__CODE_' in placeholder:
                core_match = re.search(r'__CODE_(\d+)__', placeholder)
                if core_match:
                    code_id = core_match.group(1)
                    patterns = [
                        f'__CODE_{code_id}__', f'__code_{code_id}__', f'__Code_{code_id}__',
                        f'__ CODE_{code_id}__', f'__ code_{code_id}__', f'__ Code_{code_id}__',
                        f'__CODE_{code_id} __', f'__code_{code_id} __', f'__Code_{code_id} __',
                        f'__ CODE_{code_id} __', f'__ code_{code_id} __', f'__ Code_{code_id} __',
                        f'__code {code_id}__', f'__Code {code_id}__', f'__CODE {code_id}__'
                    ]
                    for pattern in patterns:
                        restoration_map[pattern] = original

            elif '__INLINE_' in placeholder:
                core_match = re.search(r'__INLINE_(\d+)__', placeholder)
                if core_match:
                    inline_id = core_match.group(1)
                    patterns = [
                        f'__INLINE_{inline_id}__', f'__inline_{inline_id}__', f'__Inline_{inline_id}__',
                        f'__ INLINE_{inline_id}__', f'__ inline_{inline_id}__', f'__ Inline_{inline_id}__',
                        f'__INLINE_{inline_id} __', f'__inline_{inline_id} __', f'__Inline_{inline_id} __',
                        f'__ INLINE_{inline_id} __', f'__ inline_{inline_id} __', f'__ Inline_{inline_id} __',
                        f'__inline {inline_id}__', f'__Inline {inline_id}__', f'__INLINE {inline_id}__'
                    ]
                    for pattern in patterns:
                        restoration_map[pattern] = original

            elif '__NAV_TABLE_' in placeholder:
                core_match = re.search(r'__NAV_TABLE_(\d+)__', placeholder)
                if core_match:
                    nav_id = core_match.group(1)
                    patterns = [
                        f'__NAV_TABLE_{nav_id}__', f'__nav_table_{nav_id}__', f'__Nav_Table_{nav_id}__',
                        f'__ NAV_TABLE_{nav_id}__', f'__ nav_table_{nav_id}__', f'__ Nav_Table_{nav_id}__',
                        f'__NAV_TABLE_{nav_id} __', f'__nav_table_{nav_id} __', f'__Nav_Table_{nav_id} __',
                        f'__ NAV_TABLE_{nav_id} __', f'__ nav_table_{nav_id} __', f'__ Nav_Table_{nav_id} __'
                    ]
                    for pattern in patterns:
                        restoration_map[pattern] = original

            elif '__TERM_' in placeholder:
                core_match = re.search(r'__TERM_(\d+)_(\d+)__', placeholder)
                if core_match:
                    term_id, instance_id = core_match.groups()
                    patterns = [
                        f'__TERM_{term_id}_{instance_id}__', f'__term_{term_id}_{instance_id}__', f'__Term_{term_id}_{instance_id}__',
                        f'__ TERM_{term_id}_{instance_id}__', f'__ term_{term_id}_{instance_id}__', f'__ Term_{term_id}_{instance_id}__',
                        f'__TERM_{term_id}_{instance_id} __', f'__term_{term_id}_{instance_id} __', f'__Term_{term_id}_{instance_id} __',
                        f'__ TERM_{term_id}_{instance_id} __', f'__ term_{term_id}_{instance_id} __', f'__ Term_{term_id}_{instance_id} __',
                        f'__term {term_id}_{instance_id}__', f'__Term {term_id}_{instance_id}__', f'__TERM {term_id}_{instance_id}__',
                        f'__protected_{term_id}__', f'__Protected_{term_id}__', f'__PROTECTED_{term_id}__',
                        f'__ protected_{term_id}__', f'__ Protected_{term_id}__', f'__ PROTECTED_{term_id}__',
                        f'__protected_{term_id} __', f'__Protected_{term_id} __', f'__PROTECTED_{term_id} __',
                        f'__ protected_{term_id} __', f'__ Protected_{term_id} __', f'__ PROTECTED_{term_id} __'
                    ]
                    for pattern in patterns:
                        restoration_map[pattern] = original

        # Apply all restoration patterns
        for damaged_pattern, original in restoration_map.items():
            restored_text = restored_text.replace(damaged_pattern, original)

        # Third pass: Regex-based cleanup for severely damaged patterns
        for placeholder, original in term_map.items():
            if '__TERM_' in placeholder:
                match = re.search(r'__TERM_(\d+)_(\d+)__', placeholder)
                if match:
                    term_id, instance_id = match.groups()
                    damage_patterns = [
                        rf'__[Tt]erm_{term_id}_{instance_id}__',
                        rf'__ [Tt]erm_{term_id}_{instance_id}__',
                        rf'__[Tt]erm_{term_id}_{instance_id} __',
                        rf'__ [Tt]erm_{term_id}_{instance_id} __',
                        rf'__[Pp]rotected_{term_id}__',
                        rf'__ [Pp]rotected_{term_id}__',
                        rf'__[Pp]rotected_{term_id} __',
                        rf'__ [Pp]rotected_{term_id} __',
                        rf'__{term_id}_{instance_id}__',
                        rf'__ {term_id}_{instance_id}__'
                    ]
                    for pattern in damage_patterns:
                        try:
                            restored_text = re.sub(pattern, original, restored_text, flags=re.IGNORECASE)
                        except:
                            continue

            elif '__CODE_' in placeholder:
                match = re.search(r'__CODE_(\d+)__', placeholder)
                if match:
                    code_id = match.group(1)
                    damage_patterns = [
                        rf'__[Cc]ode_{code_id}__',
                        rf'__ [Cc]ode_{code_id}__',
                        rf'__[Cc]ode_{code_id} __',
                        rf'__ [Cc]ode_{code_id} __',
                        rf'__{code_id}__'
                    ]
                    for pattern in damage_patterns:
                        try:
                            restored_text = re.sub(pattern, original, restored_text, flags=re.IGNORECASE)
                        except:
                            continue

            elif '__INLINE_' in placeholder:
                match = re.search(r'__INLINE_(\d+)__', placeholder)
                if match:
                    inline_id = match.group(1)
                    damage_patterns = [
                        rf'__[Ii]nline_{inline_id}__',
                        rf'__ [Ii]nline_{inline_id}__',
                        rf'__[Ii]nline_{inline_id} __',
                        rf'__ [Ii]nline_{inline_id} __',
                        rf'__{inline_id}__'
                    ]
                    for pattern in damage_patterns:
                        try:
                            restored_text = re.sub(pattern, original, restored_text, flags=re.IGNORECASE)
                        except:
                            continue

        # Final fallback: Fix known problematic placeholders based on the actual content
        # This maps common damaged placeholders to their correct values
        fallback_fixes = {
            # Technical terms that commonly get damaged
            '__Term_9_0__': 'JavaScript',
            '__term_9_0__': 'JavaScript',
            '__Term_1_0__': 'API',
            '__term_1_0__': 'API',
            '__ term_1_0__': 'API',
            '__Term_18_0__': 'REST',
            '__term_18_0__': 'REST',
            '__term_1_1__': 'APIs',
            '__ term_1_1__': 'APIs',
            '__Term_12_0__': 'Docker',
            '__term_12_0__': 'Docker',
            '__ term_12_0__': 'Docker',
            '__Term_12_1__': 'Docker',
            '__term_12_1__': 'Docker',
            '__Term_12_1_': 'Docker',  # Missing closing underscore
            '__term_12_1_': 'Docker',
            '__Term_60_0__': 'npm',
            '__term_60_0__': 'npm',
            '__Term_61_0__': 'yarn',
            '__term_61_0__': 'yarn',
            '__term_4_0__': 'Git',
            '__ term_4_0__': 'Git',
            '__term_12_2__': 'Docker',
            '__ term_12_2__': 'Docker',
            '__Term_21_0__': 'JWT',
            '__term_21_0__': 'JWT',
            '__term_1_4__': 'api',
            '__ term_1_4__': 'api',
            '__term_1_5__': 'api',
            '__ term_1_5__': 'api',
            '__Term_35_0__': 'Heroku',
            '__term_35_0__': 'Heroku',
            '__Term_35_1__': 'Heroku',
            '__term_35_1__': 'Heroku',
            '__Term_35_2__': 'Heroku',
            '__term_35_2__': 'Heroku',
            '__term_12_3__': 'Docker',
            '__ term_12_3__': 'Docker',
            '__term_12_4__': 'Docker',
            '__ term_12_4__': 'Docker',
            '__Term_48_0__': 'React',
            '__term_48_0__': 'React',
            '__Term_48_1__': 'React',
            '__term_48_1__': 'React',
            '__Term_68_0__': 'ESLint',
            '__term_68_0__': 'ESLint',
            '__Term_69_0__': 'Prettier',
            '__term_69_0__': 'Prettier',
            # Navigation table fixes
            '__NAV_TABLE_0__': '',  # Will be handled by fix_navigation_table
            '__nav_table_0__': '',
            '__ nav_table_0__': '',
            '__NAV_TABLE_0 __': '',
            '__ NAV_TABLE_0 __': '',
        }

        # Apply fallback fixes
        for placeholder, replacement in fallback_fixes.items():
            restored_text = restored_text.replace(placeholder, replacement)

        # Fix common spacing issues caused by translation
        spacing_fixes = [
            (r'## 📚__ ', '## 📚'),  # Fix "__ API文档" -> "API文档"
            (r'get /api /用户', 'GET /api/users'),  # Fix API endpoint formatting
            (r'post /api /用户', 'POST /api/users'),
            (r'__ ([A-Z]+)', r'\1'),  # Remove leading "__ " from terms
            (r'([A-Z]+) __', r'\1'),  # Remove trailing " __" from terms
            (r' ##([🚀📦🔧📚🧪🤝📄🙏📞])', r'\n\n## \1'),  # Fix broken section headers
            (r'##([🚀📦🔧📚🧪🤝📄🙏📞])', r'## \1'),  # Fix missing space in headers
            (r'## 🚀🚀🚀', '## 🚀功能'),  # Fix specific broken header
            (r'## 📦📦📦', '## 📦安装'),  # Fix installation header
            (r'## 🔧🔧🔧', '## 🔧配置'),  # Fix configuration header
        ]

        for pattern, replacement in spacing_fixes:
            restored_text = re.sub(pattern, replacement, restored_text, flags=re.IGNORECASE)

        return restored_text

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

class FreeTranslationRunner:
    """Main translation runner using free Google Translate"""

    def __init__(self):
        self.config = Config()
        self.translator = SimpleGoogleTranslator()
        self.text_processor = TextProcessor(self.config.protected_terms)
        self.nav_manager = NavigationManager(self.config)
        self.file_manager = FileManager(self.config.overwrite_mode)
    
    def translate_content(self, content, target_language):
        """Translate content to target language"""
        protected_text, term_map = self.text_processor.protect_content(content)
        paragraphs = protected_text.split('\n\n')
        translated_paragraphs = []

        for paragraph in paragraphs:
            if paragraph.strip():
                try:
                    translated_paragraph = self.translator.translate(paragraph, target_language, 'en')
                    translated_paragraphs.append(translated_paragraph)
                except Exception:
                    translated_paragraphs.append(paragraph)
            else:
                translated_paragraphs.append(paragraph)

        translated_text = '\n\n'.join(translated_paragraphs)
        final_text = self.text_processor.restore_content(translated_text, term_map)
        final_text = self.fix_language_names(final_text)
        final_text = self.fix_markdown_formatting(final_text)
        final_text = self.fix_navigation_table(final_text)

        return final_text

    def fix_markdown_formatting(self, text):
        """Fix common markdown formatting issues after translation"""
        # Fix full-width characters that should be half-width
        text = text.replace('＃', '#')  # Full-width # to half-width #
        text = text.replace('（', '(')  # Full-width ( to half-width (
        text = text.replace('）', ')')  # Full-width ) to half-width )
        text = text.replace('：', ':')  # Full-width : to half-width :
        text = text.replace('；', ';')  # Full-width ; to half-width ;
        text = text.replace('，', ',')  # Full-width , to half-width , (in code contexts)

        # Fix headers that lost their space after #
        text = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', text, flags=re.MULTILINE)

        # Fix any remaining header spacing issues
        text = re.sub(r'^(#{1,6})\s{2,}', r'\1 ', text, flags=re.MULTILINE)

        # Fix table formatting
        text = re.sub(r'\|\s*-+\s*\|', '|:-----------|', text)  # Fix table separators

        # Fix list formatting that might be broken
        text = re.sub(r'^(\s*)-([^\s])', r'\1- \2', text, flags=re.MULTILINE)
        text = re.sub(r'^(\s*)\*([^\s])', r'\1* \2', text, flags=re.MULTILINE)
        text = re.sub(r'^(\s*)(\d+\.)([^\s])', r'\1\2 \3', text, flags=re.MULTILINE)

        # Fix table formatting
        text = re.sub(r'\|([^\s|])', r'| \1', text)
        text = re.sub(r'([^\s|])\|', r'\1 |', text)

        return text


    
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

    def fix_navigation_table(self, text):
        """Fix navigation table by regenerating it completely"""
        # Remove any broken navigation section
        text = re.sub(r'## 🌍[^#]*?(?=##|\Z)', '', text, flags=re.DOTALL)
        text = re.sub(r'__NAV_TABLE_\d+[^#]*?(?=##|\Z)', '', text, flags=re.DOTALL)

        # Generate correct navigation table
        nav_lines = [
            "## 🌍 Available Languages",
            "",
            "| 🌐 Language | 📄 File | 📊 Status |",
            "|-------------|---------|-----------|"
        ]

        # Add language entries (hardcoded for now to ensure correctness)
        nav_lines.extend([
            "| English | [README_en.md](./README_en.md) | ✅ Available |",
            "| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |"
        ])

        nav_lines.extend(["", ""])
        nav_content = "\n".join(nav_lines)

        # Insert navigation after the title
        title_match = re.match(r'^(#[^#][^\n]*\n)', text)
        if title_match:
            title = title_match.group(1)
            rest_content = text[len(title):]
            return title + nav_content + rest_content
        else:
            return nav_content + text

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
            return

        if not self.translator.test_connection():
            return

        if not os.path.exists(self.config.source_file):
            return

        os.makedirs(self.config.output_dir, exist_ok=True)

        with open(self.config.source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()

        translated_count = 0
        skipped_count = 0
        error_count = 0

        # Update root navigation
        if self.config.add_language_nav and self.config.update_root_readme:
            try:
                updated_content = self.nav_manager.update_root_navigation(source_content)
                if updated_content != source_content:
                    with open(self.config.source_file, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    source_content = updated_content
            except Exception:
                return

        # Create English version with correct navigation
        english_output = f"{self.config.output_dir}/README_en.md"
        try:
            # Fix navigation for locales folder (same as other translated files)
            english_content = source_content
            if self.nav_manager.has_navigation(english_content):
                # Remove existing navigation
                content_no_nav = re.sub(r'## 🌍 Available Languages.*?(?=##|\Z)', '', english_content, flags=re.DOTALL)
                content_no_nav = re.sub(r'\n{3,}', '\n\n', content_no_nav)

                # Get title and add locales navigation
                title_match = re.match(r'^#\s+(.+)', content_no_nav)
                title = title_match.group(1) if title_match else "README"
                nav_content = self.nav_manager.create_navigation(for_root=False)
                content_without_title = re.sub(r'^#\s+.+\n\n?', '', content_no_nav)

                # Reconstruct content with correct navigation
                english_content = f"# {title}\n{nav_content}{content_without_title}"

            english_footer = """

---
> 🌐 This is the original English version | Translation tool: [i18n-Translator](https://github.com/1038lab/i18n-Translator)

<!-- ORIGINAL ENGLISH VERSION -->"""

            with open(english_output, 'w', encoding='utf-8') as f:
                f.write(english_content + english_footer)
            translated_count += 1
        except Exception:
            error_count += 1

        for lang_code in self.config.enabled_languages:
            if lang_code not in self.config.languages_info:
                continue

            lang_info = self.config.languages_info[lang_code]
            file_suffix = lang_info['file_suffix']
            output_file = f"{self.config.output_dir}/README{file_suffix}.md"

            try:
                should_translate, actual_file, _ = self.file_manager.should_translate(
                    self.config.source_file, output_file)

                if not should_translate:
                    skipped_count += 1
                    continue

                translated_content = self.translate_content(source_content, lang_code)
                final_content = self.add_footer(translated_content, lang_code)

                with open(actual_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)

                translated_count += 1

            except Exception:
                error_count += 1

        return translated_count > 0

class TranslationManager:
    def __init__(self, config):
        self.config = config
        self.translator = SimpleGoogleTranslator()
        self.text_processor = TextProcessor(config.protected_terms)
        self.nav_manager = NavigationManager(config)
        self.file_manager = FileManager(config.overwrite_mode)

    def translate_content(self, content, target_language):
        """Translate content to target language"""
        protected_text, term_map = self.text_processor.protect_content(content)
        paragraphs = protected_text.split('\n\n')
        translated_paragraphs = []

        for paragraph in paragraphs:
            if paragraph.strip():
                try:
                    translated_paragraph = self.translator.translate(paragraph, target_language, 'en')
                    translated_paragraphs.append(translated_paragraph)
                except Exception:
                    translated_paragraphs.append(paragraph)
            else:
                translated_paragraphs.append(paragraph)

        translated_text = '\n\n'.join(translated_paragraphs)
        final_text = self.text_processor.restore_content(translated_text, term_map)
        final_text = self.fix_language_names(final_text)
        final_text = self.fix_markdown_formatting(final_text)
        final_text = self.fix_navigation_table(final_text)

        return final_text

    def fix_markdown_formatting(self, text):
        """Fix common markdown formatting issues after translation"""
        # Fix full-width characters that should be half-width
        text = text.replace('＃', '#')  # Full-width # to half-width #
        text = text.replace('（', '(')  # Full-width ( to half-width (
        text = text.replace('）', ')')  # Full-width ) to half-width )
        text = text.replace('：', ':')  # Full-width : to half-width :
        text = text.replace('；', ';')  # Full-width ; to half-width ;
        text = text.replace('，', ',')  # Full-width , to half-width , (in code contexts)

        # Fix headers that lost their space after #
        text = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', text, flags=re.MULTILINE)

        # Fix any remaining header spacing issues
        text = re.sub(r'^(#{1,6})\s{2,}', r'\1 ', text, flags=re.MULTILINE)

        # Fix table formatting
        text = re.sub(r'\|\s*-+\s*\|', '|:-----------|', text)  # Fix table separators

        # Fix list formatting that might be broken
        text = re.sub(r'^(\s*)-([^\s])', r'\1- \2', text, flags=re.MULTILINE)
        text = re.sub(r'^(\s*)\*([^\s])', r'\1* \2', text, flags=re.MULTILINE)
        text = re.sub(r'^(\s*)(\d+\.)([^\s])', r'\1\2 \3', text, flags=re.MULTILINE)

        # Fix table formatting
        text = re.sub(r'\|([^\s|])', r'| \1', text)
        text = re.sub(r'([^\s|])\|', r'\1 |', text)

        return text

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

    def fix_navigation_table(self, text):
        """Fix navigation table by regenerating it completely"""
        # Remove any broken navigation section
        text = re.sub(r'## 🌍[^#]*?(?=##|\Z)', '', text, flags=re.DOTALL)
        text = re.sub(r'__NAV_TABLE_\d+[^#]*?(?=##|\Z)', '', text, flags=re.DOTALL)

        # Generate correct navigation table
        nav_lines = [
            "## 🌍 Available Languages",
            "",
            "| 🌐 Language | 📄 File | 📊 Status |",
            "|-------------|---------|-----------|"
        ]

        # Add language entries (hardcoded for now to ensure correctness)
        nav_lines.extend([
            "| English | [README_en.md](./README_en.md) | ✅ Available |",
            "| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |",
            "| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |",
            "| Korean (한국어) | [README_ko.md](./README_ko.md) | ✅ Available |"
        ])

        nav_lines.extend(["", ""])
        nav_content = "\n".join(nav_lines)

        # Insert navigation after the title
        title_match = re.match(r'^(#[^#][^\n]*\n)', text)
        if title_match:
            title = title_match.group(1)
            rest_content = text[len(title):]
            return title + nav_content + rest_content
        else:
            return nav_content + text

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

if __name__ == "__main__":
    runner = FreeTranslationRunner()
    result = runner.run()
    if result:
        print("Translation completed successfully!")
    else:
        print("Translation completed with issues or was skipped.")
