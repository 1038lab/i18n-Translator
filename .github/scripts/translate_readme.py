#!/usr/bin/env python3
import os
import re
import requests
import json

# 配置
API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
SOURCE_FILE = 'README.md'

# 目标语言配置
LANGUAGES = {
    'zh': 'README_ZH.md',    # 中文
    'ja': 'README_JA.md',    # 日语
    'ko': 'README_KO.md',    # 韩语  
    'es': 'README_ES.md',    # 西班牙语
    # 'fr': 'README_FR.md',  # 法语 - 注释掉暂时不需要的语言
    # 'de': 'README_DE.md',  # 德语
}

# 不需要翻译的术语
PROTECTED_TERMS = [
    'GitHub', 'API', 'README', 'Markdown', 'Git',
    'ComfyUI', 'GGUF', 'JoyCaption', 'llama-cpp-python', 
    'HuggingFace', 'GPU', 'CPU', 'CUDA',
]

def protect_terms(text):
    """保护特定术语不被翻译"""
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
    """恢复保护的术语"""
    restored_text = text
    for placeholder, term in term_map.items():
        restored_text = restored_text.replace(placeholder, term)
    return restored_text

def preserve_markdown_structure(text):
    """保护 Markdown 结构不被翻译"""
    protected_text = text
    structure_map = {}
    
    # 保护代码块
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    for i, block in enumerate(code_blocks):
        placeholder = f"__CODE_BLOCK_{i}__"
        protected_text = protected_text.replace(block, placeholder, 1)
        structure_map[placeholder] = block
    
    # 保护内联代码
    inline_codes = re.findall(r'`[^`\n]+`', protected_text)
    for i, code in enumerate(inline_codes):
        placeholder = f"__INLINE_CODE_{i}__"
        protected_text = protected_text.replace(code, placeholder, 1)
        structure_map[placeholder] = code
    
    # 保护链接
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', protected_text)
    for i, (text_part, url) in enumerate(links):
        full_link = f'[{text_part}]({url})'
        placeholder = f"__LINK_{i}__"
        protected_text = protected_text.replace(full_link, placeholder, 1)
        structure_map[placeholder] = full_link
    
    return protected_text, structure_map

def translate_text_with_rest_api(text, target_language):
    """使用 REST API 翻译文本"""
    if not API_KEY:
        raise ValueError("Google Translate API key not found")
    
    print(f"Translating to {target_language} using REST API...")
    
    # Google Translate REST API endpoint
    url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
    
    # 保护术语和 Markdown 结构
    protected_text, term_map = protect_terms(text)
    protected_text, structure_map = preserve_markdown_structure(protected_text)
    
    # 分段翻译
    paragraphs = protected_text.split('\n\n')
    translated_paragraphs = []
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            try:
                print(f"  Translating paragraph {i+1}/{len(paragraphs)}")
                
                # 准备请求数据
                data = {
                    'q': paragraph,
                    'target': target_language,
                    'source': 'en',
                    'format': 'text'
                }
                
                # 发送请求
                response = requests.post(url, data=data)
                response.raise_for_status()
                
                # 解析响应
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                translated_paragraphs.append(translated_text)
                
            except Exception as e:
                print(f"  Warning: Translation error for paragraph {i+1}: {e}")
                translated_paragraphs.append(paragraph)  # 保留原文
        else:
            translated_paragraphs.append(paragraph)
    
    # 重新组合
    translated_text = '\n\n'.join(translated_paragraphs)
    
    # 恢复保护的内容
    translated_text = restore_terms(translated_text, structure_map)
    translated_text = restore_terms(translated_text, term_map)
    
    return translated_text

def add_translation_header(content, language_code):
    """添加翻译说明头部"""
    language_names = {
        'zh': 'Chinese (中文)',
        'ja': 'Japanese (日本語)',
        'ko': 'Korean (한국어)', 
        'es': 'Spanish (Español)',
        'fr': 'French (Français)',
        'de': 'German (Deutsch)'
    }
    
    # 获取原始标题
    title_match = re.match(r'^#\s+(.+)', content)
    title = title_match.group(1) if title_match else "README"
    
    header = f"""# {title}

> 🌐 This document was automatically translated to {language_names.get(language_code, language_code)} using Google Translate.
> 📝 For the most accurate and up-to-date information, please refer to the [English README](README.md).
> 🤝 Community contributions to improve translations are welcome!

---

"""
    
    # 移除原始标题，避免重复
    content_without_title = re.sub(r'^#\s+.+\n\n?', '', content)
    return header + content_without_title

def test_api_connection():
    """测试 API 连接"""
    if not API_KEY:
        print("❌ No API key found")
        return False
    
    try:
        print("🧪 Testing Google Translate API connection...")
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
        
        print(f"✅ API connection successful!")
        print(f"Test translation: Hello -> {translated}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Starting README translation process...")
    
    # 测试 API 连接
    if not test_api_connection():
        print("❌ API test failed, exiting...")
        return
    
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Source file {SOURCE_FILE} not found")
        return
    
    # 读取源文件
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    print(f"📄 Source content length: {len(source_content)} characters")
    
    # 翻译到各种语言
    for lang_code, output_file in LANGUAGES.items():
        try:
            print(f"\n🌐 Translating to {lang_code} ({output_file})...")
            
            # 翻译内容
            translated_content = translate_text_with_rest_api(source_content, lang_code)
            
            # 添加翻译说明头部
            final_content = add_translation_header(translated_content, lang_code)
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✅ Successfully created {output_file}")
            
        except Exception as e:
            print(f"❌ Error translating to {lang_code}: {e}")
    
    print("\n🎉 Translation process completed!")

if __name__ == "__main__":
    main()
