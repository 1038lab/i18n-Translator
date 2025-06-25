# 🌐i18n- GitHub动作自动转移工具
## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |



## 🚀功能

 -  **🆓双翻译模式**  - 免费模式(无设置)和API模式(质量更高)
 -  **⚡零配置**  - 用最小设置开箱即用
 -  **🤖GitHub操作集成**  -  README更新上的自动翻译
 -  **🛡️智能术语保护**  - 保护技术术语和代码免受翻译
 -  **📝Markdown保护**  - 维护格式,链接和代码块
 -  **🔄增量翻译**  - 仅在源文件更改时翻译
 -  **🌍多语言支持**  - 支持10多种语言,包括中文,日语,韩语
 -  **📁有组织的输出**  -  `locales/`目录中的清洁文件结构
 -  **🎛️灵活控制**  - 手动触发和覆盖保护

## 📦快速开始

### 先决条件

- GitHub存储库
 -  GitHub动作的基本知识
- Google Cloud API键(可选,仅适用于API模式)

### 安装

#### 📦**方法1:下载版本包(推荐)**

1。**下载**最新设置软件包:
    - 转到[Releases](https://github.com/1038lab/i18n/releases)
    - 下载最新的`i18n-github-actions-setup-v*.zip`文件

2。**提取** zip文件到您的存储库根

3。**提交**文件:
```bash
git add .github/
git commit -m "Add i18n auto-translation setup"
git push origin main
```

#### 📋**方法2:手动设置**

将这些文件从此存储库复制到您的项目:
```
.github/
├── i18n-config.yml              # Configuration file
├── workflows/
│   ├── translate-readme-api.yml # API mode workflow
│   └── translate-readme-free.yml # Free mode workflow
└── scripts/
    ├── translate_readme_api.py  # API translation script
    └── translate_readme_free.py # Free translation script
```

### 第一次运行

安装后:
1。转到您的存储库的**操作**选项卡
2。选择**“自动翻译README(免费)” **
3。单击**“运行工作流” **
4。等待完成并检查`locales/`文件夹

* *🎉就是这样！**您的README现在有多种语言可用。

## 🔧配置

编辑`.github/i18n-config.yml`文件以自定义您的翻译设置:

```yaml
# Translation settings
translation:
  enabled: true                  # Enable/disable auto translation
  mode: "free"                  # "free" (no API key) or "api" (higher quality)
  source_file: "README.md"      # Source file to translate
  output_dir: "locales"         # Output directory

# Languages to translate to
enabled_languages:
  - en    # English (always enabled)
  - zh    # Chinese (Simplified)
  - ja    # Japanese
  - ko    # Korean
  # Add more languages as needed

# Terms that should not be translated
protected_terms:
  ["GitHub", "API", "README", "Markdown", "i18n", "Docker", "Node.js"]
```

### Configuration Options

| Option | Description | Default |
| :----------- | ------------- | :----------- |
| `enabled` | Enable/disable auto translation | `true` |
| `mode` | Translation mode: "free" or "api" | `"free"` |
| `source_file` | Source file to translate | `"README.md"` |
| `output_dir` | Output directory for translations | `"locales"` |
| `enabled_languages` | List of target languages | `["en", "zh"]` |
| `protected_terms` | Terms to protect from translation | See config file |



## 📚📚翻译模式

### 🆓免费模式(建议入门)

* *需要零配置！**使用简单的Google Translate服务。

```yaml
translation:
  mode: "free"  # No API key needed
```

* *优点:**
 -  no no API键需要
 - 完全免费
 - 零设置时间
 - ✅良好的翻译质量

* *缺点:**
 - ⚠️利率有限公司
 - ⚠️质量略低于API模式

### __API模式(更高质量)

使用Google Cloud Translation API用于专业级翻译。

```yaml
translation:
  mode: "api"  # Requires Google Cloud API key
```

* *设置:**
1。创建一个Google云项目
2。启用云翻译API
3。创建API密钥
4。将`GOOGLE_TRANSLATE_API_KEY`添加到您的存储库秘密

* *优点:**
 - ✅最高翻译质量
 - 更稳定和可靠
 - ✅更高的速率限制
 - 专业支持

* *缺点:**
 - 💰花钱(每字符支付)
 - ⚙️需要API设置

## 🧪用法示例

### 手动翻译触发器

从GitHub手动触发翻译:

```bash
# Go to your repository
# Click "Actions" tab
# Select "Auto Translate README (Free)" or "Auto Translate README (API)"
# Click "Run workflow"
# Select main branch
# Click "Run workflow" button
```

### 自动翻译

更新README.MD时,翻译自动运行:

```bash
# Edit your README.md
git add README.md
git commit -m "Update README"
git push origin main

# Translation will run automatically
# Check the 'locales/' folder for results
```

## 🚀高级功能

### 智能定期保护

保护技术术语免于翻译:

```yaml
protected_terms:
  - "GitHub Actions"
  - "API"
  - "Docker"
  - "Node.js"
  - "YourProjectName"
```

### 覆盖保护

控制现有翻译的处理方式:

```yaml
translation:
  overwrite_mode: "auto"  # Options: "always", "never", "auto", "create_new"
```

### 手动编辑保护

将此注释添加到任何翻译文件中,以防止覆盖:

```html
<!-- MANUAL EDIT -->
```

## 🤝贡献

我们欢迎捐款！这是您可以提供帮助的方式:

### 贡献方式

1。**🐛报告错误**  - 找到问题了吗？让我们知道！
2。**💡建议功能**  - 有改进的想法吗？
3。**📝改进文档**  - 帮助我们的文档更好
4。**🔧提交代码**  - 修复错误或添加功能
5。**🌍添加语言支持**  - 帮助支持更多语言

### 开发过程

1。叉子存储库
2。创建功能分支:`git checkout -b feature/amazing-feature`
3。进行更改并测试
4。提交您的更改:`git commit -m 'Add amazing feature'`
5。推到分支:`git push origin feature/amazing-feature`
6。打开拉请请求

### 测试您的更改

```bash
# Test the free translation mode
python .github/scripts/translate_readme_free.py

# Test with your own README
# Make sure translations work correctly
```

## 📄许可证

该项目已根据MIT许可证获得许可 - 有关详细信息,请参见[LICENSE](LICENSE)文件。

## 🙏致谢

 - 感谢Google Translate提供翻译服务
 - 特别感谢所有有助于改善此工具的贡献者
 - 灵感来自需要可访问的多语言文档的启发
 - 为开源社区建造❤️

## 📞支持和帮助

如果您需要帮助或有疑问:

 - 🐛**问题**:[GitHub Issues](https://github.com/1038lab/i18n/issues)
 - 📖**文档**:[README_en.md](README_en.md) | [README_zh.md](README_zh.md)
 - 💡**功能请求**:打开“增强”标签的问题
 - 🤝**讨论**:使用GitHub讨论一般问题

### 常见问题

 -  **翻译不起作用？**检查您的配置文件
 -  ** API错误？**验证您的Google Cloudterm_1_11_密钥
 -  **文件不更新？**检查覆盖模式设置

- --

🌐**使世界更容易获得,一次翻译** | 由[1038lab](https://github.com/1038lab)用❤️制造

---
> 🌐 本文档由 Google Translate 自动翻译，如有错误请参考 [英文原版](./README_en.md) | 翻译工具: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-TRANSLATED -->