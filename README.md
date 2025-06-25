# 🌐 i18n - GitHub Actions Auto-Translation Tool

> **Automatically translate your README files into multiple languages using GitHub Actions**

A simple, powerful tool that automatically translates your project's README.md into multiple languages using GitHub Actions. Support both free translation (no API key required) and premium API translation for higher quality.

## 🚀 Features

- **🆓 Dual Translation Modes** - Free mode (no setup) and API mode (higher quality)
- **⚡ Zero Configuration** - Works out of the box with minimal setup
- **🤖 GitHub Actions Integration** - Automatic translation on README updates
- **🛡️ Smart Term Protection** - Protects technical terms and code from translation
- **📝 Markdown Preservation** - Maintains formatting, links, and code blocks
- **🔄 Incremental Translation** - Only translates when source files change
- **🌍 Multi-Language Support** - Supports 10+ languages including Chinese, Japanese, Korean
- **📁 Organized Output** - Clean file structure in `locales/` directory
- **🎛️ Flexible Control** - Manual triggers and overwrite protection

## 📦 Quick Start

### Prerequisites

- GitHub repository
- Basic knowledge of GitHub Actions
- Google Cloud API key (optional, for API mode only)

### Installation

#### 📦 **Method 1: Download Release Package (Recommended)**

1. **Download** the latest setup package:
   - Go to [Releases](https://github.com/1038lab/i18n/releases)
   - Download the latest `i18n-github-actions-setup-v*.zip` file

2. **Extract** the ZIP file to your repository root

3. **Commit** the files:
```bash
git add .github/
git commit -m "Add i18n auto-translation setup"
git push origin main
```

#### 📋 **Method 2: Manual Setup**

Copy these files from this repository to your project:
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

### First Run

After installation:
1. Go to your repository's **Actions** tab
2. Select **"Auto Translate README (Free)"**
3. Click **"Run workflow"**
4. Wait for completion and check the `locales/` folder

**🎉 That's it!** Your README is now available in multiple languages.

## 🔧 Configuration

Edit the `.github/i18n-config.yml` file to customize your translation settings:

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
|--------|-------------|---------|
| `enabled` | Enable/disable auto translation | `true` |
| `mode` | Translation mode: "free" or "api" | `"free"` |
| `source_file` | Source file to translate | `"README.md"` |
| `output_dir` | Output directory for translations | `"locales"` |
| `enabled_languages` | List of target languages | `["en", "zh"]` |
| `protected_terms` | Terms to protect from translation | See config file |

## 📚 Translation Modes

### 🆓 Free Mode (Recommended for Getting Started)

**Zero configuration required!** Uses Simple Google Translate service.

```yaml
translation:
  mode: "free"  # No API key needed
```

**Pros:**
- ✅ No API key required
- ✅ Completely free
- ✅ Zero setup time
- ✅ Good translation quality

**Cons:**
- ⚠️ Rate limited
- ⚠️ Slightly lower quality than API mode

### 💎 API Mode (Higher Quality)

Uses Google Cloud Translation API for professional-grade translations.

```yaml
translation:
  mode: "api"  # Requires Google Cloud API key
```

**Setup:**
1. Create a Google Cloud project
2. Enable Cloud Translation API
3. Create an API key
4. Add `GOOGLE_TRANSLATE_API_KEY` to your repository secrets

**Pros:**
- ✅ Highest translation quality
- ✅ More stable and reliable
- ✅ Higher rate limits
- ✅ Professional support

**Cons:**
- 💰 Costs money (pay per character)
- ⚙️ Requires API setup

## 🧪 Usage Examples

### Manual Translation Trigger

Trigger translation manually from GitHub Actions:

```bash
# Go to your repository
# Click "Actions" tab
# Select "Auto Translate README (Free)" or "Auto Translate README (API)"
# Click "Run workflow"
# Select main branch
# Click "Run workflow" button
```

### Automatic Translation

Translation runs automatically when you update README.md:

```bash
# Edit your README.md
git add README.md
git commit -m "Update README"
git push origin main

# Translation will run automatically
# Check the 'locales/' folder for results
```

## 🚀 Advanced Features

### Smart Term Protection

Protect technical terms from being translated:

```yaml
protected_terms:
  - "GitHub Actions"
  - "API"
  - "Docker"
  - "Node.js"
  - "YourProjectName"
```

### Overwrite Protection

Control how existing translations are handled:

```yaml
translation:
  overwrite_mode: "auto"  # Options: "always", "never", "auto", "create_new"
```

### Manual Edit Protection

Add this comment to any translation file to prevent overwriting:

```html
<!-- MANUAL EDIT -->
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **🐛 Report Bugs** - Found an issue? Let us know!
2. **💡 Suggest Features** - Have ideas for improvements?
3. **📝 Improve Documentation** - Help make our docs better
4. **🔧 Submit Code** - Fix bugs or add features
5. **🌍 Add Language Support** - Help support more languages

### Development Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test them
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Testing Your Changes

```bash
# Test the free translation mode
python .github/scripts/translate_readme_free.py

# Test with your own README
# Make sure translations work correctly
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to Google Translate for providing translation services
- Special thanks to all contributors who help improve this tool
- Inspired by the need for accessible, multilingual documentation
- Built with ❤️ for the open source community

## 📞 Support & Help

If you need help or have questions:

- 🐛 **Issues**: [GitHub Issues](https://github.com/1038lab/i18n/issues)
- 📖 **Documentation**: [README_en.md](README_en.md) | [README_zh.md](README_zh.md)
- 💡 **Feature Requests**: Open an issue with the "enhancement" label
- 🤝 **Discussions**: Use GitHub Discussions for general questions

### Common Issues

- **Translation not working?** Check your configuration file
- **API errors?** Verify your Google Cloud API key
- **Files not updating?** Check the overwrite mode settings

---

🌐 **Making the world more accessible, one translation at a time** | Made with ❤️ by [1038lab](https://github.com/1038lab)
