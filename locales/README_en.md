# GitHub i18n Actions Auto-Translation

## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|:-----------|:--------|:----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |
| Korean (한국어) | [README_ko.md](./README_ko.md) | ✅ Available |
| Spanish (Español) | [README_es.md](./README_es.md) | ✅ Available |
| French (Français) | [README_fr.md](./README_fr.md) | ✅ Available |
| Russian (Русский) | [README_ru.md](./README_ru.md) | ✅ Available |

## 📋 **Overview**

This guide will help you quickly set up a GitHub Actions auto-translation system using our provided tools to automatically translate English README.md files into multiple languages.

**🆓 We now offer TWO translation modes:**
- **Free Mode** (Recommended) - Zero configuration, no API key needed
- **API Mode** - Higher accuracy with Google Translate API (requires API key)

### **Features**
- ✅ **Two translation modes**: Free (zero-config) and API (high-quality)
- ✅ Automatically detects README.md updates and triggers translation
- ✅ Supports multiple target languages (Chinese, Japanese, Korean, Spanish, etc.)
- ✅ Protects technical terms from being translated
- ✅ Maintains complete Markdown formatting
- ✅ Secure API key management (API mode only)
- ✅ Incremental translation (only translates updated content)
- ✅ Beautiful language navigation
- ✅ On/off switch to save API costs
- ✅ Smart overwrite protection (4 modes)
- ✅ Manual edit detection and protection
- ✅ Manual workflow trigger with force options

---

## 🆓 **Quick Start (Free Mode - Recommended)**

### **Step 1: Copy Project Files**
Copy the following files from the [i18n](https://github.com/1038lab/i18n) project to your project:

```
your-project/
├── .github/
│   ├── i18n-config.yml                    # Configuration file
│   ├── workflows/
│   │   ├── translate-readme-api.yml       # API mode workflow
│   │   └── translate-readme-free.yml      # Free mode workflow (default)
│   └── scripts/
│       ├── translate_readme_api.py        # API translation script
│       └── translate_readme_free.py       # Free translation script
└── README.md                              # Your English README
```

### **Step 2: Run Free Translation**
1. In your GitHub repository, click the **"Actions"** tab
2. Select the **"Auto Translate README (Free)"** workflow
3. Click **"Run workflow"** → Select `main` branch → Click **"Run workflow"**
4. Wait for completion and check the `locales/` folder for translated files

**🎉 That's it! No API key needed.**

---

## 💰 **Upgrade to API Mode (Optional - Higher Quality)**

If you want higher translation accuracy, you can upgrade to API mode:

## 🚀 **Step 1: Set up Google Cloud Translation API**

### **1.1 Create Google Cloud Project**
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project selector and create a new project
3. Enter project name (e.g., `readme-translator`)
4. Click "Create"

### **1.2 Enable Translation API**
1. In Google Cloud Console, ensure you've selected the correct project
2. Search for "Cloud Translation API" in the search bar
3. Click on "Cloud Translation API" result
4. Click the "Enable" button
5. Wait for API to be enabled

### **1.3 Create API Key**
1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the generated API key (format like: `AIzaSyC...`)
4. **Important**: Save this key immediately, you'll need it later

### **1.4 Restrict API Key Permissions (Recommended)**
1. On the Credentials page, click the API key you just created
2. In the "API restrictions" section:
   - Select "Restrict key"
   - Check "Cloud Translation API"
3. Click "Save"

---

## 🔐 **Step 2: Set up API Key in GitHub**

### **2.1 Set Repository Secret**
1. In your GitHub repository, click the **"Settings"** tab
2. In the left menu, select **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**
4. Fill in the information:
   - **Name**: `GOOGLE_TRANSLATE_API_KEY`
   - **Secret**: Paste the API key you obtained in step 1.3
5. Click **"Add secret"**

### **2.2 Verify Secret Setup**
After setup, you should see in the Secrets list:
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **Step 3: Switch to API Mode**

### **3.1 Update Configuration**
Open `.github/i18n-config.yml` and change the mode:

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### **3.2 File Descriptions**
- **`i18n-config.yml`** - Translation configuration file, controls languages, term protection, etc.
- **`translate-readme-api.yml`** - API mode GitHub Actions workflow file
- **`translate-readme-free.yml`** - Free mode GitHub Actions workflow file
- **`translate_readme_api.py`** - API translation script
- **`translate_readme_free.py`** - Free translation script

---

## ⚙️ **Step 4: Configure Translation Settings**

### **4.1 Edit Configuration File**
Open the `.github/i18n-config.yml` file and modify as needed:

#### **Choose Translation Mode**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **Select Target Languages**
```yaml
enabled_languages:
  - en    # English (always enabled)
  - zh    # Chinese
  - ja    # Japanese
  - ko    # Korean
  # - es  # Spanish - comment out languages you don't need
  # - fr  # French
  # - ru  # Russian
```

#### **Add Project-Specific Terms**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **Overwrite Mode Settings**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 Configuration Explanation**
- **`enabled`**: Controls whether to enable auto-translation
- **`mode`**: Translation mode - `"free"` (no API key) or `"api"` (higher quality)
- **`enabled_languages`**: List of target languages to translate to
- **`protected_terms`**: List of terms that should not be translated
- **`output_dir`**: Output directory for translation files (default: `locales`)
- **`overwrite_mode`**: Overwrite mode
  - `"always"`: Always overwrite existing translations
  - `"never"`: Never overwrite existing translations
  - `"auto"`: Smart overwrite (recommended)
  - `"create_new"`: Create new files with date suffix

### **4.3 Mode Comparison**

| Feature | Free Mode | API Mode |
|---------|-----------|----------|
| **API Key** | ❌ Not needed | ✅ Required |
| **Cost** | 🆓 Completely free | 💰 Pay per use |
| **Translation Quality** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Stability** | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Very stable |
| **Setup Difficulty** | ⭐⭐⭐⭐⭐ Zero config | ⭐⭐ API setup needed |

---

## 🧪 **Step 5: Test Translation System**

### **5.1 Commit Files**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 Manual Trigger Test**

**For Free Mode:**
1. In your GitHub repository, click the **"Actions"** tab
2. Select the **"Auto Translate README (Free)"** workflow
3. Click the **"Run workflow"** button
4. Select the `main` branch
5. Click the green **"Run workflow"** button

**For API Mode:**
1. Select the **"Auto Translate README (API)"** workflow instead
2. Follow the same steps above

### **5.3 Monitor Execution**
1. Click on the running workflow instance
2. Click the `translate` job
3. Expand each step to view execution logs
4. Check for any error messages

### **5.4 Verify Results**
After successful execution, you should see newly generated files in your repository:
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**Note**: The `locales/` folder is automatically created during the first translation.

---

## 🔄 **Step 6: Automated Workflow**

### **6.1 Auto Trigger**
The system will automatically run translation in the following situations:
- When you update the `README.md` file and push to the `main` branch
- Only retranslates when the source file is newer than translation files (incremental translation)

### **6.2 Translation Results**
Each translation file contains:
- 🌍 **Beautiful language navigation table** - With flag icons for easy language switching
- 📝 **Translated content** - Maintains original formatting and code blocks
- 🔗 **Localized footer information** - Contains translation notes and project links
- 🛡️ **Manual edit protection** - Automatically detects and protects user modifications

---

## 💡 **Usage Tips**

### **🎛️ Translation Control**

#### **Complete Stop vs Overwrite Control**

There are two different ways to control the translation system:

**1. Stop Auto-Translation Completely:**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ GitHub Actions will run but exit immediately
- ✅ No API calls made (saves costs for API mode)
- ✅ No files will be created or updated

**2. Control File Overwriting:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub Actions will still run
- ✅ Will create new translation files if they don't exist
- ❌ Will NOT update existing translation files

**3. Force Translation (Manual Trigger):**
Both workflows support a `force_translate` option when manually triggered:
- Set to `true` to override the `enabled: false` setting
- Useful for one-time translations without changing configuration

#### **Overwrite Mode Comparison**

| Mode | Auto Trigger | Overwrite Existing | Create New Files |
|------|-------------|-------------------|------------------|
| `enabled: false` | ❌ Script exits | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ Runs | ❌ Skip existing | ✅ Creates new |
| `overwrite_mode: "auto"` | ✅ Runs | 🤔 Smart detection | ✅ Creates new |
| `overwrite_mode: "always"` | ✅ Runs | ✅ Always overwrites | ✅ Creates new |

### **Save API Costs (API Mode)**
1. **Use free mode**: Set `mode: "free"` for zero cost
2. **Disable translation**: Set `enabled: false` in `i18n-config.yml`
3. **Reduce languages**: Only enable languages you really need
4. **Incremental translation**: System automatically only translates updated content

### **Custom Term Protection**
Add to `protected_terms`:
- Project names
- Special feature names
- API endpoint names
- Brand names

### **Protect Manual Edits**
Add markers in translation files to protect manual modifications:
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **Monitor Translation Quality**
- **Free mode**: Good for most use cases, completely free
- **API mode**: Higher accuracy for professional projects
- Regularly check translation results
- Adjust protected terms as needed
- Manually correct translation files when necessary

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **API Key Error**
```
Error: API connection failed: 403 Forbidden
```
**Solution**: Check if API key is correctly set and has sufficient permissions

#### **Translation Skipped**
```
Skipping zh: locales/README_zh.md is up to date
```
**Explanation**: This is normal incremental translation behavior, source file hasn't been updated

#### **Translation Disabled**
```
Translation is disabled in configuration
```
**Solution**: Set `enabled: true` in `i18n-config.yml` or use manual trigger with `force_translate: true`

#### **Wrong Workflow Selected**
**Issue**: Using API workflow without API key or vice versa
**Solution**:
- For free mode: Use "Auto Translate README (Free)" workflow
- For API mode: Use "Auto Translate README (API)" workflow and ensure API key is set

### **Get Help**
- View [project documentation](https://github.com/1038lab/i18n)
- Submit an [Issue](https://github.com/1038lab/i18n/issues)
- Check Actions execution logs

---

## 🎉 **Complete!**

Your project now has auto-translation functionality! Every time you update README.md, the system will automatically generate multi-language versions, making your project more accessible to global users.

---

> 🌐 This guide is provided by the [i18n](https://github.com/1038lab/i18n) project


---
> 🌐 This is the original English version | Translation tool: [i18n-Translator](https://github.com/1038lab/i18n-Translator)

<!-- ORIGINAL ENGLISH VERSION -->