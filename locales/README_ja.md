# GitHub i18n アクション自動翻訳

## 🌍 利用可能な言語

| 🌐 言語 | 📄 ファイル | 📊 ステータス |
|:-----------|:---------|:----------|
| 英語 | [README_en.md](./README_en.md) | ✅ 利用可能 |
| 英語 | [README_en.md](./README_en.md) | ✅ 利用可能 |
| 中国語 (中文) | [README_zh.md](./README_zh.md) | ✅ 利用可能 |
| 日本語 (日本語) | [README_ja.md](./README_ja.md) | ✅ 利用可能 |
| 韓国語 (한국어) | [README_ko.md](./README_ko.md) | ✅ 利用可能 |
| スペイン語 (Español) | [README_es.md](./README_es.md) | ✅ 利用可能 |
| フランス語 (Français) | [README_fr.md](./README_fr.md) | ✅ 利用可能 |
| ロシア語 (Русский) | [README_ru.md](./README_ru.md) | ✅ 利用可能 |

## 📋 **概要**

このガイドは、弊社が提供するツールを使用して、英語の README.md ファイルを複数の言語に自動的に翻訳する GitHub Actions 自動翻訳システムをすばやくセットアップするのに役立ちます。

**🆓 2つの翻訳モードをご用意しました:**
- **フリーモード** (推奨) - 設定不要、API キー不要
- **API モード** - Google Translate API でより高い精度を実現 (API キーが必要)

### **機能**
- ✅ **2つの翻訳モード**：無料（ゼロ設定）とAPI（高品質）
- ✅ README.mdの更新を自動検出し、翻訳を開始
- ✅ 複数のターゲット言語（中国語、日本語、韓国語、スペイン語など）をサポート
- ✅ 技術用語が翻訳されないように保護
- ✅ Markdownの完全なフォーマットを維持
- ✅ 安全なAPIキー管理（APIモードのみ）
- ✅ 増分翻訳（更新されたコンテンツのみを翻訳）
- ✅ 美しい言語ナビゲーション
- ✅ APIのコストを節約するためのオン/オフスイッチ
- ✅ スマートな上書き保護（4つのモード）
- ✅ 手動編集の検出と保護
- ✅ 強制オプション付きの手動ワークフロートリガー

---

## 🆓 **クイックスタート（無料モード - 推奨）**

### **ステップ 1: プロジェクト ファイルをコピーする**
[i18n](https://github.com/1038lab/i18n) プロジェクトから次のファイルをプロジェクトにコピーします。

__コード_0__

### **ステップ 2: 無料翻訳を実行する**
1. GitHub リポジトリで、**「アクション」** タブをクリックします。
2. **「Auto Translate README (Free)」** ワークフローを選択します。
3. **「ワークフローを実行」** をクリック → `main` ブランチを選択 → **「ワークフローを実行」** をクリック
4. 完了するまで待ち、`locales/` フォルダに翻訳済みファイルがあるか確認します。

**🎉 これで完了です！API キーは必要ありません。**

---

## 💰 **API モードへのアップグレード (オプション - 高品質)**

より高い翻訳精度が必要な場合は、API モードにアップグレードできます。

## 🚀 **ステップ 1: Google Cloud Translation を設定する API**

### **1.1 Google Cloud プロジェクトを作成する**
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスします
2. プロジェクトセレクターをクリックして新しいプロジェクトを作成します
3. プロジェクト名を入力します（例：`readme-translator`）
4. [作成] をクリックします

### **1.2 Translation API を有効にする**
1. Google Cloud Console で、正しいプロジェクトが選択されていることを確認します。
2. 検索バーで「Cloud Translation API」を検索します。
3. 「Cloud Translation API」の結果をクリックします。
4. [有効にする] ボタンをクリックします。
5. API が有効になるまで待ちます。

### **1.3 API キーの作成**
1. 「APIs & Services」→「Credentials」へ移動します。
2. 「Create Credentials」→「API Key」をクリックします。
3. 生成された API キー（形式：`AIzaSyC...`）をコピーします。
4. **重要**: このキーはすぐに保存してください。後で必要になります。

### **1.4 API キーの権限を制限する（推奨）**
1. 「認証情報」ページで、先ほど作成した API キーをクリックします。
2. 「API の制限」セクションで、以下の操作を行います。
- 「キーを制限する」を選択します。
- 「Cloud Translation API」にチェックを入れます。
3. 「保存」をクリックします。

---

## 🔐 **ステップ 2: API を設定し、GitHub を入力します**

### **2.1 リポジトリシークレットの設定**
1. GitHub リポジトリで、**「設定」** タブをクリックします。
2. 左側のメニューで、**「シークレットと変数」** → **「アクション」** を選択します。
3. **「新しいリポジトリシークレット」** をクリックします。
4. 以下の情報を入力します。
- **名前**: `GOOGLE_TRANSLATE_API_KEY`
- **シークレット**: 手順 1.3 で取得した API キーを貼り付けます。
5. **「シークレットを追加」** をクリックします。

### **2.2 シークレットの設定を確認する**
設定後、シークレットリストに次の情報が表示されます。
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **ステップ 3: API モードに切り替える**

### **3.1 構成の更新**
`.github/i18n-config.yml` を開いてモードを変更します。

__コード_2__

### **3.2 ファイルの説明**
- **`i18n-config.yml`** - 翻訳設定ファイル。言語制御、用語保護など。
- **`translate-readme-api.yml`** - API モード GitHub アクションワークフローファイル
- **`translate-readme-free.yml`** - フリーモード GitHub アクションワークフローファイル
- **`translate_readme_api.py`** - API 翻訳スクリプト
- **`translate_readme_free.py`** - フリー翻訳スクリプト

---

## ⚙️ **ステップ 4: 翻訳設定を構成する**

### **4.1 設定ファイルの編集**
`.github/i18n-config.yml` ファイルを開き、必要に応じて変更します。

#### **翻訳モードを選択**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **対象言語を選択**
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

#### **プロジェクト固有の用語を追加する**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **上書きモード設定**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 設定の説明**
- **`enabled`**: 自動翻訳を有効にするかどうかを制御します
- **`mode`**: 翻訳モード - `"free"` (API キーなし) または `"api"` (高品質)
- **`enabled_languages`**: 翻訳先の言語のリスト
- **`protected_terms`**: 翻訳対象外の用語のリスト
- **`output_dir`**: 翻訳ファイルの出力ディレクトリ (デフォルト: `locales`)
- **`overwrite_mode`**: 上書きモード
- `"always"`: 既存の翻訳を常に上書きする
- `"never"`: 既存の翻訳を上書きしない
- `"auto"`: スマート上書き (推奨)
- `"create_new"`: 日付付きで新しいファイルを作成する接尾辞

### **4.3 モードの比較**

| 機能 | 無料モード | API モード |
|---------|-----------|-----------|
| **API キー** | ❌ 不要 | ✅ 必須 |
| **費用** | 🆓 完全に無料 | 💰 使用量に応じて支払い |
| **翻訳品質** | ⭐⭐⭐⭐ 良好 | ⭐⭐⭐⭐⭐ 優秀 |
| **安定性** | ⭐⭐⭐ 中程度 | ⭐⭐⭐⭐⭐ 非常に安定 |
| **設定の難易度** | ⭐⭐⭐⭐⭐ 設定不要 | ⭐⭐ API の設定が必要 |

---

## 🧪 **ステップ 5: 翻訳システムをテストする**

### **5.1 コミットファイル**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 手動トリガーテスト**

**無料モードの場合:**
1. GitHub リポジトリで、**「アクション」** タブをクリックします。
2. **「Auto Translate README (Free)」** ワークフローを選択します。
3. **「ワークフローを実行」** ボタンをクリックします。
4. `main` ブランチを選択します。
5. 緑色の **「ワークフローを実行」** ボタンをクリックします。

**API モードの場合:**
1. **「README (API) を自動翻訳」** ワークフローを選択します。
2. 上記と同じ手順を繰り返します。

### **5.3 実行の監視**
1. 実行中のワークフローインスタンスをクリックします
2. `translate` ジョブをクリックします
3. 各ステップを展開して実行ログを表示します
4. エラーメッセージを確認します

### **5.4 結果の確認**
実行が成功すると、リポジトリに新しく生成されたファイルが表示されます。
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**注意**: `locales/` フォルダーは、最初の翻訳中に自動的に作成されます。

---

## 🔄 **ステップ 6: 自動化されたワークフロー**

### **6.1 自動トリガー**
システムは以下の状況で自動的に翻訳を実行します。
- `README.md` ファイルを更新し、`main` ブランチにプッシュした場合
- ソースファイルが翻訳ファイルよりも新しい場合にのみ再翻訳を実行（増分翻訳）

### **6.2 翻訳結果**
各翻訳ファイルには以下が含まれます。
- 🌍 **美しい言語ナビゲーションテーブル** - 言語切り替えを容易にするフラグアイコン付き
- 📝 **翻訳済みコンテンツ** - 元の書式とコードブロックを維持
- 🔗 **ローカライズされたフッター情報** - 翻訳メモとプロジェクトリンクを含む
- 🛡️ **手動編集保護** - ユーザーによる変更を自動的に検出し、保護します

---

## 💡 **使用上のヒント**

### **🎛️ 翻訳制御**

#### **完全停止と上書き制御**

翻訳システムを制御するには、次の 2 つの方法があります。

**1. 自動翻訳を完全に停止する:**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ GitHub アクションは実行されますが、すぐに終了します
- ✅ API 呼び出しは行われません (API モードのコストを節約します)
- ✅ ファイルは作成または更新されません

**2. 制御ファイルの上書き:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub アクションは引き続き実行されます
- ✅ 翻訳ファイルが存在しない場合は、新しい翻訳ファイルを作成します
- ❌ 既存の翻訳ファイルは更新されません

**3. 強制翻訳（手動トリガー）:**
どちらのワークフローも、手動でトリガーする場合に`force_translate`オプションをサポートします。
- `enabled: false`設定を上書きするには、`true`に設定します。
- 設定を変更せずに1回限りの翻訳を行う場合に便利です。

#### **上書きモードの比較**

| モード | 自動トリガー | 既存ファイルを上書き | 新しいファイルを作成 |
|------|------------|-------------------|------------------|
| `enabled: false` | ❌ スクリプト終了 | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ 実行 | ❌ 既存ファイルをスキップ | ✅ 新規作成 |
| `overwrite_mode: "auto"` | ✅ 実行 | 🤔 スマート検出 | ✅ 新規作成 |
| `overwrite_mode: "always"` | ✅ 実行 | ✅ 常に上書き | ✅ 新規作成 |

### **API コストを節約する (API モード)**
1. **無料モードを使用する**: `mode: "free"` をコストゼロに設定する
2. **翻訳を無効にする**: `enabled: false` を `i18n-config.yml` に設定する
3. **言語を減らす**: 本当に必要な言語のみを有効にする
4. **増分翻訳**: システムは更新されたコンテンツのみを自動的に翻訳します

### **カスタム用語保護**
`protected_terms` に追加:
- プロジェクト名
- 特別な機能名
- API エンドポイント名
- ブランド名

### **手動編集を保護する**
手動による変更を保護するために、翻訳ファイルにマーカーを追加します。
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **翻訳品質の監視**
- **無料モード**: ほとんどのユースケースに適しており、完全に無料です
- **API モード**: プロフェッショナルプロジェクト向けの高精度
- 翻訳結果を定期的に確認
- 必要に応じて保護用語を調整
- 必要に応じて翻訳ファイルを手動で修正

---

## 🛠️ **トラブルシューティング**

### **よくある問題**

#### **API キーエラー**
```
Error: API connection failed: 403 Forbidden
```
**解決策**: API キーが正しく設定され、十分な権限が付与されていることを確認してください

#### **翻訳をスキップしました**
```
Skipping zh: locales/README_zh.md is up to date
```
**説明**: これは通常の増分翻訳の動作であり、ソースファイルは更新されていません。

#### **翻訳が無効**
```
Translation is disabled in configuration
```
**解決策**: `i18n-config.yml` で `enabled: true` を設定するか、`force_translate: true` で手動トリガーを使用します

#### **間違ったワークフローが選択されています**
**問題**: API キーを使用せずに API ワークフローを使用している、またはその逆
**解決策**:
- 無料モードの場合: 「自動翻訳 README (無料)」ワークフローを使用してください
- API モードの場合: 「自動翻訳 README (API)」ワークフローを使用し、API キーが設定されていることを確認してください

### **ヘルプを見る**
- [project documentation](https://github.com/1038lab/i18n) を表示
- [Issue](https://github.com/1038lab/i18n/issues) を送信
- アクション実行ログを確認する

---

## 🎉 **完了しました!**

プロジェクトに自動翻訳機能が追加されました！README.md を更新するたびに、システムが自動的に多言語バージョンを生成するため、世界中のユーザーがプロジェクトにアクセスしやすくなります。

---

> 🌐 このガイドは[i18n](https://github.com/1038lab/i18n) プロジェクトによって提供されています


---
> 🌐 この文書は Google Translate で自動翻訳されています。[英語版](./README_en.md)もご確認ください | 翻訳ツール: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->