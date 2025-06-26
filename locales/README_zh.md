# GitHub__i18n动作自动转移
## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |

##📋**概述**

本指南将帮助您快速设置GitHub操作自动翻译系统,使用我们提供的工具自动将英语README.md文件转换为多种语言。

* *🆓我们现在提供两种翻译模式:**
 -  **免费模式**(建议) - 零配置,无需API键
 -  ** API模式**  - 使用Google Translate API(需要API键)使用Google Translate Google Translate键)

### **特征**
 - ✅*两种翻译模式**:免费(零核)和API(高质量)
 - ✅自动检测README.md更新和触发转换
 - ✅支持多种目标语言(中文,日语,韩语,西班牙语等)
 - ✅保护技术术语免于翻译
 - ✅维护完整的Markdown格式化
 - 安全API密钥管理(API模式)
 - ✅增量翻译(仅翻译更新的内容)
 - ✅美丽的语言导航
 - ✅打开/关闭开关以保存API费用
 - ✅智能覆盖保护(4个模式)
 - ✅手动编辑检测和保护
 - ✅手动工作流触发带有力选项的触发器

- --

## 🆓**快速启动(免费模式 - 推荐)**

### **步骤1:复制项目文件**
将以下文件从[i18n](https://github.com/1038lab/i18n)项目复制到您的项目:

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

### **步骤2:自由翻译**
1。在您的GitHub存储库中,单击**“ action” **选项卡
2。选择**“自动翻译README(免费)” **工作流
3。单击**“运行工作流” **→选择`main`分支→单击**“运行工作流” **
4。等待完成,然后检查`locales/`文件夹中的翻译文件

* *🎉就是这样！无需API键。**

- --

## 💰**升级到API模式(可选 - 质量更高)**

如果您需要更高的翻译精度,则可以升级到API模式:

## 🚀**步骤1:设置Google Cloud Translation API **

### ** 1.1创建Google Cloud Project **
1。访问[Google Cloud Console](https://console.cloud.google.com/)
2。单击项目选择器并创建一个新项目
3。输入项目名称(例如`readme-translator`)
4。单击“创建”

### ** 1.2启用翻译API_ **
1。在Google Cloud Console中,确保您选择了正确的项目
2。在搜索栏中搜索“云翻译API”
3。单击“云翻译__term_1_1_14__”结果
4。单击“启用”按钮
5。等待启用API

### ** 1.3创建API键**
1。导航到“ __Term_1_1_17__＆Services”→“凭据”
2。单击“创建凭据”→“ __Term_1_1_18__密钥”
3。复制生成的__Term_1_1_19__键(格式如:`AIzaSyC...`)
4。**重要**:立即保存此键,稍后您需要它

### ** 1.4限制API密钥权限(建议)**
1。在凭据页面上,单击刚创建的API
2。在“ API限制”部分中:
    - 选择“限制密钥”
    - 检查“云翻译API”
3。单击“保存”

- --

## 🔐**步骤2:设置API键GitHub **

### ** 2.1设置存储库秘密**
1。在您的GitHub存储库中,单击**“设置” **选项卡
2。在左菜单中,选择**“秘密和变量” **→**“ Action” **
3。单击**“新存储库秘密” **
4。填写信息:
    -  **名称**:`GOOGLE_TRANSLATE_API_KEY`
    -  **秘密**:粘贴您在步骤1.3中获得的API键
5。单击**“添加秘密” **

### ** 2.2验证秘密设置**
设置后,您应该在秘密列表中看到:
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

- --

## 📁**步骤3:切换到API模式**

### ** 3.1更新配置**
打开`.github/i18n-config.yml`并更改模式:

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### ** 3.2文件说明**
 -  ** `i18n-config.yml` **  - 翻译配置文件,控制语言,定期保护等。
 -  ** `translate-readme-api.yml` **  -  API模式GitHub操作工作流量文件
 -  ** `translate-readme-free.yml` **  - 免费模式GitHub操作工作流量文件
 -  ** `translate_readme_api.py` **  -  API翻译脚本
 -  ** `translate_readme_free.py` **  - 免费翻译脚本

- --

## ⚙️**步骤4:配置翻译设置**

### ** 4.1编辑配置文件**
打开__inline_11_文件并根据需要进行修改:

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

#### **添加特定项目的术语**
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

### ** 4.2配置说明**
 -  ** `enabled` **:控制是否启用自动翻译
 -  ** `mode` **:翻译模式 -  `"free"`(no API键)或`"api"`(更高质量)
 -  ** `enabled_languages` **:要转化为目标语言列表
 -  ** `protected_terms` **:不应翻译的术语列表
 -  ** `output_dir` **:翻译文件的输出目录(默认值:`locales`)
 -  ** `overwrite_mode` **:覆盖模式
  - `"always"`:始终覆盖现有的翻译
  - `"never"`:永不覆盖现有的翻译
  - `"auto"`:智能覆盖(推荐)
  - `"create_new"`:使用日期后缀创建新文件

### ** 4.3模式比较**

| 功能 | 免费模式 | API模式 |
| :----------- | ------------- | :----------- |
| ** API键** | ❌不需要 | ✅必需 |
| **费用** | 🆓完全免费 | 💰按使用付款 |
| **翻译质量** | ⭐⭐⭐⭐好 | ⭐⭐⭐⭐⭐优秀 |
| **稳定性** | ⭐⭐⭐中度 | ⭐⭐⭐⭐⭐非常稳定 |
| **设置难度** | ⭐⭐⭐⭐⭐零配置 | ⭐⭐API需要设置 |

- --

## 🧪**步骤5:测试翻译系统**

### ** 5.1提交文件**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### ** 5.2手动触发测试**

* *免费模式:**
1。在您的GitHub存储库中,单击**“ action” **选项卡
2。选择**“自动翻译README(免费)” **工作流
3。单击**“运行工作流” **按钮
4。选择`main`分支
5。单击绿色**“运行工作流” **按钮

* *对于API模式:**
1。选择**“自动翻译README(API)” **工作流
2。按照上面的相同步骤

### ** 5.3监视器执行**
1。单击运行的工作流程实例
2。单击`translate`工作
3。扩展每个步骤以查看执行日志
4。检查任何错误消息

### ** 5.4验证结果**
成功执行后,您应该在存储库中查看新生成的文件:
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

* *注意**:`locales/`文件夹是在第一次翻译期间自动创建的。

- --

## 🔄**步骤6:自动化工作流**

### ** 6.1自动触发**
该系统将在以下情况下自动运行翻译:
 - 更新`README.md`文件并推到`main`分支时
 - 仅当源文件比翻译文件更新(增量翻译)时,仅重新翻译

### ** 6.2翻译结果**
每个翻译文件包含:
 - 🌍*美丽的语言导航表**  - 带有标志图标,可轻松进行语言切换
 - 📝**翻译内容**  - 维护原始格式和代码块
 -  **局部页脚信息**  - 包含翻译笔记和项目链接
 - 🛡️**手动编辑保护**  - 自动检测并保护用户修改

- --

## 💡**用法提示**

### **🎛第🎛️翻译控制**

#### **完整停止与覆盖控制**

控制翻译系统有两种不同的方法:

* * 1。完全停止自动翻译:**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
 - ✅GitHub动作将运行但立即退出
 -  no API拨打电话(为API模式节省成本)
 - ✅不会创建或更新文件

* * 2。控制文件覆盖:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
 - ✅GitHub动作仍将运行
 - ✅如果不存在,将创建新的翻译文件
 - ❌不会更新现有的翻译文件

* * 3。力翻译(手动触发):**
手动触发时,这两个工作流都支持`force_translate`选项:
 - 设置为`true`覆盖`enabled: false`设置
 - 用于一次性翻译而无需更改配置

#### **覆盖模式比较**

| 模式 | 自动触发器 | 覆盖现有 | 创建新文件 |
| :----------- | ------------------------------------------------------------------------ |
| `enabled: false` | ❌脚本退出 | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅运行 | ❌跳过现有 | ✅创建新 |
| `overwrite_mode: "auto"` | ✅运行 | 🤔智能检测 | ✅创建新 |
| `overwrite_mode: "always"` | ✅运行 | ✅总是覆盖 | ✅创建新 |

### **保存API费用(API模式)**
1。**使用免费模式**:设置`mode: "free"`零成本
2。**禁用翻译**:设置`enabled: false` in `i18n-config.yml`
3。**减少语言**:仅启用您真正需要的语言
4。**增量翻译**:系统自动仅翻译更新的内容

### **自定义保护**
添加到`protected_terms`:
 - 项目名称
 - 特殊功能名称
- API端点名称
 - 品牌名称

### **保护手册编辑**
在翻译文件中添加标记以保护手动修改:
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **监视器翻译质量**
 -  **免费模式**:适合大多数用例,完全免费
 -  ** API模式**:专业项目的较高精度
 - 定期检查翻译结果
 - 根据需要调整受保护的术语
 - 必要时手动纠正翻译文件

- --

## 🛠️**故障排除**

### **常见问题**

#### ** API键错误**
```
Error: API connection failed: 403 Forbidden
```
* *解决方案**:检查API键是否正确设置并具有足够的权限

#### **翻译跳过**
```
Skipping zh: locales/README_zh.md is up to date
```
* *说明**:这是正常的增量翻译行为,源文件尚未更新

#### **禁用翻译**
```
Translation is disabled in configuration
```
* *解决方案**:在`i18n-config.yml`中设置`enabled: true`或使用`force_translate: true`使用手动触发器

#### **选择错误的工作流**
* *问题**:使用API不用API键或vicea的工作流程
* *解决方案**:
 - 免费模式:使用“自动翻译README(免费)”工作流程
 - 对于API模式:使用“自动翻译README(API)”工作流程并确保设置API键

### **获得帮助**
 - 查看[project documentation](https://github.com/1038lab/i18n)
 - 提交[Issue](https://github.com/1038lab/i18n/issues)
 - 检查操作执行日志

- --

## 🎉**完成！**

您的项目现在具有自动翻译功能！每次您更新README.md时,系统都会自动生成多语言版本,从而使您的项目更易于全球用户访问。

- --

>🌐本指南由[i18n](https://github.com/1038lab/i18n)项目提供

---
> 🌐 本文档由 Google Translate 自动翻译，如有错误请参考 [英文原版](./README_en.md) | 翻译工具: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-TRANSLATED -->