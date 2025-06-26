# GitHub i18nアクション自動翻訳 
## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |

##📋**概要**

このガイドは、提供されたツールを使用してGitHubアクション自動翻訳システムをすばやく設定して、英語README.mdファイルを複数の言語に自動的に翻訳します。

* *🆓ここで2つの翻訳モードを提供しています:**
 -  **フリーモード**(推奨) - ゼロ構成、APIキーが必要です
 -  ** Therm_1_____モード**  -  Google Translateでより高い精度

### **特徴**
- ✅** 2つの翻訳モード**:free(zero-config)およびAPI(高品質)
- c README.mdの更新とトリガーの翻訳を自動的に検出します
- change複数のターゲット言語(中国語、日本、韓国語、スペイン語など)をサポートしています。
- cling技術用語が翻訳されないように保護します
- completion完全なMarkdownフォーマットを維持します
- ✅APIキー管理(APIモードのみ)
- ✅増分変換(更新されたコンテンツのみを翻訳)
 - ✅美しい言語ナビゲーション
 -  APIコストを節約するためのオン/オフスイッチ
- ✅スマートオーバーライティング保護(4モード)
- ✅手動編集の検出と保護
- ✅力オプションを備えた手動ワークフロートリガー

- --

## 🆓**クイックスタート(フリーモード - 推奨)**

### **ステップ1:プロジェクトファイルをコピー**
[i18n](https://github.com/1038lab/i18n)プロジェクトからプロジェクトに次のファイルをコピーします。

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

### **ステップ2:無料翻訳を実行**
1。GitHubリポジトリで、[** "Actions" **タブをクリックします
2。** "Auto Translate README(free)" **ワークフローを選択します
3. [ワークフローを実行] **をクリックします**→[`main`ブランチ]→[ワークフローを実行] **をクリックします**
4. 完了を待って、翻訳されたファイルについて`locales/`フォルダーを確認してください

* *🎉それだけです！ APIキーが必要です。**

- --

## より高い翻訳の精度が必要な場合は、APIモードにアップグレードできます。

## ### ** 1.1グーグルクラウドプロジェクトの作成**
1。[Google Cloud Console](https://console.cloud.google.com/)にアクセスしてください
2。プロジェクトセレクターをクリックして、新しいプロジェクトを作成します
3. プロジェクト名を入力します(例:`readme-translator`)
4. 「作成」をクリックします

### ** 1.2翻訳を有効にするAPI **
1。Googleクラウドコンソールでは、正しいプロジェクトを選択したことを確認してください
2。検索バーで「クラウド翻訳API」を検索する
3. 「クラウド翻訳API」をクリックします。結果
4. [有効]ボタンをクリックします
5. APIが有効になるのを待ちます

### ** 1.3 Create APIキー**
1。「APIs＆services」→「資格情報」に移動します
2. 「資格情報の作成」→「APIキー」をクリックします
3. 生成されたAPIキーをコピーします(`AIzaSyC...`のような形式)
4。**重要**:このキーをすぐに保存すると、後で必要です

### ** 1.4制限APIキー許可(推奨)**
1. 資格情報ページで、作成したばかりのAPIキーをクリックします
2。「Them_1_22__制限」セクション:
    - 「キーを制限する」を選択します
    - 「クラウド翻訳API」を確認します
3. 「保存」をクリックします

- --

## ### ** 2.1リポジトリの秘密を設定**
1。GitHubリポジトリで、[[設定] ** "**タブをクリックします
2。左メニューで、**「秘密と変数」**→**「アクション」を選択します**
3. **「新しいリポジトリシークレット」**をクリックします**
4。情報を入力してください。
    -  **名前**:`GOOGLE_TRANSLATE_API_KEY`
    -  **秘密**:ステップ1.3で取得したAPIキーを貼り付けます
5. クリック**「秘密を追加」**

### ** 2.2秘密のセットアップを検証**
セットアップ後、秘密リストに表示されるはずです。
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

- --

## ### ** 3.1 Configuration **を更新する
`.github/i18n-config.yml`を開き、モードを変更します。

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### ** 3.2ファイルの説明**
 -  ** `i18n-config.yml` **  - 翻訳構成ファイル、言語、用語保護などを制御します。
 -  ** `translate-readme-api.yml` **  -  APIモード__term_0_5_アクションワークフローファイル
 -  ** `translate-readme-free.yml` **  - フリーモードGitHubアクションワークフローファイル
 -  ** `translate_readme_api.py` **  -  API翻訳スクリプト
 -  ** `translate_readme_free.py` **  - 無料翻訳スクリプト

- --

## ### ** 4.1構成ファイルの編集**
`.github/i18n-config.yml`ファイルを開き、必要に応じて変更します。

#### **翻訳モードを選択**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **ターゲット言語を選択**
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

#### **プロジェクト固有の用語を追加**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **モードの設定を上書き**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### ** 4.2構成の説明**
 -  ** `enabled` **:自動翻訳を有効にするかどうかを制御します
 -  ** `mode` **:翻訳モード-`"free"`(APIキーなし)または`"api"`(高品質)
 -  ** `enabled_languages` **:翻訳するターゲット言語のリスト
 -  ** `protected_terms` **:翻訳すべきではない用語のリスト
 -  ** `output_dir` **:翻訳ファイルの出力ディレクトリ(デフォルト:`locales`)
 -  ** `overwrite_mode` **:上書きモード
  - `"always"`:常に既存の翻訳を上書きします
  - `"never"`:既存の翻訳を上書きしないでください
   -  `"auto"`:スマートオーバーライト(推奨)
  - `"create_new"`:日付の接尾辞を使用して新しいファイルを作成します

### ** 4.3モード比較**

| 機能 | フリーモード | APIモード |
| :----------- | ---------- | :----------- |
| ** APIキー** | ❌必要ではありません | ✅必要 |
| **コスト** | 🆓完全に無料 | 💰使用ごとの支払い |
| **翻訳品質** | ⭐⭐⭐⭐良い | ⭐⭐⭐⭐⭐素晴らしい |
| **安定性** | ⭐⭐⭐程度 | ⭐⭐⭐⭐⭐非常に安定して |
| **難易度のセットアップ** | ⭐⭐⭐⭐⭐Zero Config | ⭐⭐APIセットアップが必要 |

- --

## 🧪**ステップ5:翻訳システムをテスト**

### ** 5.1コミットファイル**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### ** 5.2マニュアルトリガーテスト**

* *フリーモード用:**
1。__term_0_______リポジトリで、[** "Actions" **タブをクリックします
2. [** "自動翻訳README(free)" **ワークフローを選択します
3. **「ワークフローを実行する」**ボタンをクリックします
4. `main`ブランチを選択します
5。グリーン**「ワークフローを実行する」**ボタンをクリックします

* * APIモードの場合:**
1. ** "Auto Translate README(API)" **ワークフローを代わりに選択します
2。上記の同じ手順に従ってください

### ** 5.3モニター実行**
1. 実行中のワークフローインスタンスをクリックします
2。`translate`ジョブをクリックします
3. 各ステップを展開して、実行ログを表示します
4. エラーメッセージを確認してください

### ** 5.4結果を確認**
実行が成功した後、リポジトリに新しく生成されたファイルが表示されるはずです。
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

* *注**:`locales/`フォルダーは、最初の翻訳中に自動的に作成されます。

- --

## 🔄**ステップ6:自動ワークフロー**

### ** 6.1オートトリガー**
システムは、次の状況で翻訳を自動的に実行します。
 -  `README.md`ファイルを更新して`main`ブランチにプッシュすると
 - ソースファイルが翻訳ファイルよりも新しい場合にのみ再巻き戻す(インクリメンタル変換)

### ** 6.2翻訳結果**
各翻訳ファイルには以下が含まれます。
- 🌍**美しい言語ナビゲーションテーブル**  - 簡単な言語切り替えのためのフラグアイコン付き
- 📝**翻訳されたコンテンツ**  - 元のフォーマットとコードブロックを維持します
- 🔗**ローカライズされたフッター情報**  - 翻訳ノートとプロジェクトリンクが含まれています
- 🛡️**手動編集保護**  - ユーザーの変更を自動的に検出および保護する

- --

## 💡**使用のヒント**

### **🎛️翻訳コントロール**

#### **完全な停止vs上書きコントロール**

翻訳システムを制御するには2つの異なる方法があります。

* * 1。自動翻訳を完全に停止する:**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅GitHubアクションは実行されますが、すぐに終了します
 - ✅API通話は行われません(APIモードのコストを節約します)
- creativeファイルは作成または更新されません

* * 2。コントロールファイルの上書き:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅GitHubアクションは引き続き実行されます
- ✅が存在しないと新しい翻訳ファイルが作成されます
- ❌は既存の翻訳ファイルを更新しません

* * 3。フォース翻訳(マニュアルトリガー):**
両方のワークフローは、手動でトリガーされたときに`force_translate`オプションをサポートしています。
 -  `enabled: false`設定をオーバーライドするために`true`に設定します
 - 構成を変更せずに1回限りの翻訳に役立ちます

#### **上書きモードの比較**

| モード | 自動トリガー | 既存の上書き | 新しいファイルを作成 |
| :----------- | ------------- | :----------- | ------------------ |
| `enabled: false` | ❌スクリプト終了 | ❌ | ❌ |
| `overwrite_mode: "never"` | runs | cisting既存のスキップ | create new | を作成します
| `overwrite_mode: "auto"` | runs | 🤔スマート検出 | create new | を作成します
| `overwrite_mode: "always"` | runs | ✅常に上書き | create new | を作成します

### ** APIコストを節約(APIモード)**
1
2。
3。**言語を削減**:本当に必要な言語のみを有効にします
4。**インクリメンタル翻訳**:システムは自動的に更新されたコンテンツのみを翻訳します

### **カスタム用語保護**
`protected_terms`に追加します:
 - プロジェクト名
 - 特別な機能名
 -  APIエンドポイント名
 - ブランド名

### **マニュアルの編集を保護*
翻訳ファイルにマーカーを追加して、手動の変更を保護します。
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **翻訳品質を監視**
 -  **フリーモード**:ほとんどのユースケースに適しています、完全に無料
 -  ** APIモード**:専門プロジェクトの精度が高い
 - 翻訳結果を定期的に確認してください
 - 必要に応じて保護された用語を調整します
 - 必要に応じて、翻訳ファイルを手動で修正します

- --

## 🛠️**トラブルシューティング**

### **一般的な問題**

#### ** Therm_1_41__キーエラー**
```
Error: API connection failed: 403 Forbidden
```
* * solution **:APIキーが正しく設定されており、十分な権限があるかどうかを確認します

#### **翻訳スキップ**
```
Skipping zh: locales/README_zh.md is up to date
```
* *説明**:これは通常の増分変換動作です、ソースファイルは更新されていません

#### **翻訳無効**
```
Translation is disabled in configuration
```
* * solution **:`i18n-config.yml`に`enabled: true`を設定するか、`force_translate: true`で手動トリガーを使用します

#### **間違ったワークフロー選択**
* *発行**:__term_1_444_のないAPIワークフローを使用するキーまたはその逆
* *解決**:
 - フリーモードの場合:「auto translate README(free)」ワークフローを使用します
- for APIモード:「auto translate README(API)」を使用して、APIキーが設定されていることを確認します

### **ヘルプを取得**
 -  [project documentation](https://github.com/1038lab/i18n)を表示
 -  [Issue](https://github.com/1038lab/i18n/issues)を提出する
 - アクション実行ログを確認します

- --

## 🎉**完了！**

プロジェクトには自動翻訳機能があります！ README.mdを更新するたびに、システムは自動的に多言語バージョンを生成し、プロジェクトをグローバルユーザーがよりアクセスしやすくします。

- --

>🌐このガイドは[i18n](https://github.com/1038lab/i18n)プロジェクトによって提供されます

---
> 🌐 この文書は Google Translate で自動翻訳されています。[英語版](./README_en.md)もご確認ください | 翻訳ツール: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-TRANSLATED -->