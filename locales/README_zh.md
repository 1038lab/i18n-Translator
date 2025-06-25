# GitHub i18n 操作自动翻译

## 🌍 可用语言

| 🌐 Language | 📄 File | 📊 Status |
|:-----------|:--------|:----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| English | [README_en.md](./README_en.md) | ✅ Available |
| 中文 (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| 日语 (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |
| 韩语 (한국어) | [README_ko.md](./README_ko.md) | ✅ Available |
| Spanish (Español) | [README_es.md](./README_es.md) | ✅ Available |
| French (Français) | [README_fr.md](./README_fr.md) | ✅ Available |
| Russian (Русский) | [README_ru.md](./README_ru.md) | ✅ Available |

## 📋 **概述**

本指南将帮助您使用我们提供的工具快速设置GitHub Actions 自动翻译系统，以将英语README.md 文件自动翻译成多种语言。

**🆓 我们现在提供两种翻译模式：**
- **自由模式**（推荐） - 零配置，无需 API 键
- **API 模式** - 使用 Google Translate 和 API 可获得更高的准确率（需要 API 键）

### **功能**
- ✅ **两种翻译模式**：免费（零配置）和 API（高质量）
- ✅ 自动检测 README.md 更新并触发翻译
- ✅ 支持多种目标语言（中文、日语、韩语、西班牙语等）
- ✅ 保护技术术语免于翻译
- ✅ 维护完整的 Markdown 格式
- ✅ 安全的 API 密钥管理（仅限 API 模式）
- ✅ 增量翻译（仅翻译更新的内容）
- ✅ 美观的语言导航
- ✅ 开关以节省 API 成本
- ✅ 智能覆盖保护（4 种模式）
- ✅ 手动编辑检测和保护
- ✅ 带有强制选项的手动工作流触发器

---

## 🆓 **快速启动（免费模式 - 推荐）**

### **步骤 1：复制项目文件**
将以下文件从 [i18n](https://github.com/1038lab/i18n) 项目复制到您的项目中：

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

### **步骤 2：运行免费翻译**
1. 在您的 GitHub 代码库中，点击**“操作”**选项卡
2. 选择**“自动翻译 README（免费）”**工作流
3. 点击**“运行工作流”** → 选择 `main` 分支 → 点击**“运行工作流”**
4. 等待完成并检查 `locales/` 文件夹中是否有已翻译的文件

**🎉 就是这样！无需 API 键。**

---

## 💰 **升级到API模式（可选 - 更高质量）**

如果想要更高的翻译准确率，可以升级到API模式：

## 🚀 **步骤 1：设置 Google Cloud Translation API**

### **1.1 创建 Google Cloud 项目**
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击项目选择器并创建新项目
3. 输入项目名称（例如 `readme-translator`）
4. 点击“创建”

### **1.2 启用翻译 API**
1. 在 Google Cloud Console 中，确保您选择了正确的项目
2. 在搜索栏中搜索“Cloud Translation API”
3. 点击“Cloud Translation API”结果
4. 点击“启用”按钮
5. 等待 API 启用

### **1.3 创建 API 密钥**
1. 前往“APIs & Services” → “Credentials”
2. 点击“Create Credentials” → “API Key”
3. 复制生成的 API 密钥（格式如下：`AIzaSyC...`）
4. **重要提示**：请立即保存此密钥，稍后您将需要它

### **1.4 限制 API 密钥权限（推荐）**
1. 在“凭据”页面，点击您刚刚创建的 API 密钥
2. 在“API 限制”部分：
- 选择“限制密钥”
- 勾选“云翻译 API”
3. 点击“保存”

---

## 🔐 **步骤 2：设置 API 输入 GitHub**

### **2.1 设置仓库密钥**
1. 在您的 GitHub 仓库中，点击**“设置”**标签
2. 在左侧菜单中，选择**“密钥和变量”** → **“操作”**
3. 点击**“新建仓库密钥”**
4. 填写以下信息：
- **名称**：`GOOGLE_TRANSLATE_API_KEY`
- **密钥**：粘贴您在步骤 1.3 中获得的 API 密钥
5. 点击**“添加密钥”**

### **2.2 验证密钥设置**
设置完成后，您应该在密钥列表中看到：
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **步骤 3：切换到 API 模式**

### **3.1 更新配置**
打开 `.github/i18n-config.yml` 并更改模式：

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### **3.2 文件说明**
- **`i18n-config.yml`** - 翻译配置文件，用于控制语言、术语保护等。
- **`translate-readme-api.yml`** - API 模式 GitHub Actions 工作流文件
- **`translate-readme-free.yml`** - 自由模式 GitHub Actions 工作流文件
- **`translate_readme_api.py`** - API 翻译脚本
- **`translate_readme_free.py`** - 自由翻译脚本

---

## ⚙️ **步骤 4：配置翻译设置**

### **4.1 编辑配置文件**
打开 `.github/i18n-config.yml` 文件并根据需要进行修改：

#### **选择翻译模式**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **选择目标语言**
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

#### **添加项目特定术语**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **覆盖模式设置**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 配置说明**
- **`enabled`**：控制是否启用自动翻译
- **`mode`**：翻译模式 - `"free"`（无 API 键）或 `"api"`（更高质量）
- **`enabled_languages`**：需要翻译的目标语言列表
- **`protected_terms`**：不应翻译的术语列表
- **`output_dir`**：翻译文件的输出目录（默认：`locales`）
- **`overwrite_mode`**：覆盖模式
- `"always"`：始终覆盖现有翻译
- `"never"`：从不覆盖现有翻译
- `"auto"`：智能覆盖（推荐）
- `"create_new"`：创建带日期的新文件 后缀

### **4.3 模式比较**

| 功能 | 免费模式 | API 模式 |
|---------|-----------|----------|
| **API 密钥** | ❌ 不需要 | ✅ 需要 |
| **费用** | 🆓 完全免费 | 💰 按次付费 |
| **翻译质量** | ⭐⭐⭐⭐ 良好 | ⭐⭐⭐⭐⭐ 优秀 |
| **稳定性** | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 非常稳定 |
| **设置难度** | ⭐⭐⭐⭐⭐ 零配置 | ⭐⭐ 需要 API 设置 |

---

## 🧪 **步骤 5：测试翻译系统**

### **5.1 提交文件**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 手动触发测试**

**免费模式：**
1. 在您的 GitHub 代码库中，点击**“操作”**选项卡
2. 选择**“自动翻译 README（免费）”**工作流程
3. 点击**“运行工作流程”**按钮
4. 选择 `main` 分支
5. 点击绿色的**“运行工作流程”**按钮

**对于 API 模式：**
1. 选择**“自动翻译 README (API)”** 工作流程
2. 按照上述相同步骤操作

### **5.3 监控执行**
1. 点击正在运行的工作流实例
2. 点击 `translate` 作业
3. 展开每个步骤以查看执行日志
4. 检查是否有任何错误消息

### **5.4 验证结果**
成功执行后，您应该会在代码库中看到新生成的文件：
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**注意**：`locales/` 文件夹是在第一次翻译时自动创建的。

---

## 🔄 **步骤 6：自动化工作流程**

### **6.1 自动触发**
系统将在以下情况下自动运行翻译：
- 当您更新 `README.md` 文件并推送到 `main` 分支时
- 仅当源文件比翻译文件更新时才重新翻译（增量翻译）

### **6.2 翻译结果**
每个翻译文件包含：
- 🌍 **美观的语言导航表** - 带有旗帜图标，方便切换语言
- 📝 **翻译内容** - 保留原始格式和代码块
- 🔗 **本地化页脚信息** - 包含翻译注释和项目链接
- 🛡️ **手动编辑保护** - 自动检测并保护用户修改

---

## 💡 **使用技巧**

### **🎛️ 翻译控制**

#### **完全停止与覆盖控制**

有两种不同的方法来控制翻译系统：

**1. 完全停止自动翻译：**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ GitHub 操作将运行但立即退出
- ✅ 不会进行 API 调用（节省 API 模式的成本）
- ✅ 不会创建或更新任何文件

**2. 控制文件覆盖：**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub 操作仍将运行
- ✅ 如果翻译文件不存在，将创建新的翻译文件
- ❌ 不会更新现有的翻译文件

**3. 强制翻译（手动触发）：**
两种工作流程在手动触发时均支持 `force_translate` 选项：
- 设置为 `true` 可覆盖 `enabled: false` 设置
- 适用于无需更改配置的一次性翻译

#### **覆盖模式比较**

| 模式 | 自动触发 | 覆盖现有 | 创建新文件 |
|------|-------------|-------------------|-------------------|
| `enabled: false` | ❌ 脚本退出 | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ 运行 | ❌ 跳过现有 | ✅ 创建新的 |
| `overwrite_mode: "auto"` | ✅ 运行 | 🤔 智能检测 | ✅ 创建新的 |
| `overwrite_mode: "always"` | ✅ 运行 | ✅ 始终覆盖 | ✅ 创建新的 |

### **节省 API 费用（API 模式）**
1. **使用免费模式**：设置 `mode: "free"` 为零费用
2. **禁用翻译**：在 `i18n-config.yml` 中设置 `enabled: false`
3. **减少语言**：仅启用您真正需要的语言
4. **增量翻译**：系统自动仅翻译更新的内容

### **自定义术语保护**
添加到 `protected_terms`：
- 项目名称
- 特殊功能名称
- API 终端名称
- 品牌名称

### **保护手动编辑**
在翻译文件中添加标记以保护手动修改：
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **监控翻译质量**
- **免费模式**：适用于大多数用例，完全免费
- **API 模式**：为专业项目提供更高的准确率
- 定期检查翻译结果
- 根据需要调整受保护的术语
- 必要时手动更正翻译文件

---

## 🛠️ **故障排除**

### **常见问题**

#### **API 密钥错误**
```
Error: API connection failed: 403 Forbidden
```
**解决方案**：检查 API 密钥是否设置正确且是否具有足够的权限

#### **翻译已跳过**
```
Skipping zh: locales/README_zh.md is up to date
```
**解释**：这是正常的增量翻译行为，源文件尚未更新

#### **翻译已禁用**
```
Translation is disabled in configuration
```
**解决方案**：在 `i18n-config.yml` 中设置 `enabled: true` 或使用 `force_translate: true` 手动触发

#### **选择了错误的工作流程**
**问题**：使用 API 工作流程时没有使用 API 密钥，反之亦然
**解决方案**：
- 免费模式：使用“自动翻译 README（免费）”工作流程
- API 模式：使用“自动翻译 README（API）”工作流程，并确保已设置 API 密钥

### **获取帮助**
- 查看 [project documentation](https://github.com/1038lab/i18n)
- 提交 [Issue](https://github.com/1038lab/i18n/issues)
- 查看 Actions 执行日志

---

## 🎉 **完成！**

您的项目现在拥有自动翻译功能！每次更新 README.md 文件时，系统都会自动生成多语言版本，让您的项目更容易被全球用户访问。

---

> 🌐 本指南由 [i18n](https://github.com/1038lab/i18n) 项目提供


---
> 🌐 本文档由 Google Translate 自动翻译，如有错误请参考 [英文原版](./README_en.md) | 翻译工具: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->