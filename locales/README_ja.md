# 🌐i18n- GitHubアクション自動翻訳ツール
## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |

## caveable言語

## 🚀機能

 -  **🆓デュアル翻訳モード**  - フリーモード(セットアップなし)およびAPIモード(高品質)
 -  **⚡ゼロ構成**  - 最小限のセットアップで箱から出して動作します
 -  **🤖GitHubアクション統合**  -  README更新の自動翻訳
 -  **🛡️スマート用語保護**  - 技術用語とコードを翻訳から保護する
 -  **📝Markdown保存**  - フォーマット、リンク、およびコードブロックを維持します
 -  **🔄インクリメンタル翻訳**  - ソースファイルが変更されたときにのみ翻訳
 -  **🌍多言語サポート**  - 中国語、日本、韓国語を含む10以上の言語をサポートしています
 -  **📁整理された出力**  -  `locales/`ディレクトリのファイル構造をクリーンにする
 -  **🎛️フレキシブルコントロール**  - 手動トリガーと保護を上書きする

## Quickクイックスタート

### 前提条件

 -  GitHubリポジトリ
 -  GitHubアクションの基本的な知識
- Google Cloud APIキー(オプション、APIモードのみ)

### インストール

#### 📦**方法1:リリースパッケージをダウンロード(推奨)

1。**ダウンロード**最新のセットアップパッケージ:
    -  [Releases](https://github.com/1038lab/i18n/releases)に移動します
    - 最新の`i18n-github-actions-setup-v*.zip`ファイルをダウンロードします

2。**抽出** zipファイルをリポジトリルートにします

3。**コミット**ファイル:
```bash
git add .github/
git commit -m "Add i18n auto-translation setup"
git push origin main
```

#### 📋**方法2:手動セットアップ**

これらのファイルをこのリポジトリからプロジェクトにコピーします。
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

### 最初の実行

インストール後:
1. リポジトリの**アクション**タブに移動します
2. 選択** "自動翻訳README(free)" **
3. [ワークフローを実行] **をクリックします**
4. 完了を待ち、`locales/`フォルダーを確認します

* *🎉**あなたのREADMEは複数の言語で利用可能になりました。

## configuration

`.github/i18n-config.yml`ファイルを編集して、翻訳設定をカスタマイズします。

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

### 構成オプション

| オプション | 説明 | デフォルト |
| :----------- | -------------- | :----------- |
| `enabled` | 自動翻訳を有効/無効にします | `true` |
| `mode` | 翻訳モード: "free"または "api" | `"free"` |
| `source_file` | 翻訳するソースファイル | `"README.md"` |
| `output_dir` | 翻訳の出力ディレクトリ | `"locales"` |
| `enabled_languages` | ターゲット言語のリスト | `["en", "zh"]` |
| `protected_terms` | 翻訳から保護する用語 | 構成ファイルを参照してください |

## 翻訳モード

### **ゼロ構成が必要です！

```yaml
translation:
  mode: "free"  # No API key needed
```

* *長所:**
- ✅APIキーが必要です
 - 完全に無料
 -  Zeroセットアップ時間ゼロ
 - ✅翻訳の品質が良好です

* * cons:**
- ⚠️レートリミテッド
- ⚠️APIモードよりもわずかに低い品質

### プロのグレードの翻訳にGoogle Cloud Translationterm_1___を使用します。

```yaml
translation:
  mode: "api"  # Requires Google Cloud API key
```

* *設定:**
1. Google Cloudプロジェクトを作成します
2. クラウド翻訳を有効にするAPI
3. APIキーを作成します
4. `GOOGLE_TRANSLATE_API_KEY`をリポジトリの秘密に追加します

* *長所:**
 - ✅翻訳最高の品質
 - より安定して信頼できる
 - ✅レート制限が高くなっています
 - ✅専門的なサポート

* * cons:**
 - 💰費用がかかる(文字ごとの支払い)
- ⚙️APIセットアップが必要です

## 🧪使用例

### マニュアル翻訳トリガー

GitHubアクションから手動で翻訳をトリガーします:

```bash
# Go to your repository
# Click "Actions" tab
# Select "Auto Translate README (Free)" or "Auto Translate README (API)"
# Click "Run workflow"
# Select main branch
# Click "Run workflow" button
```

### 自動翻訳

翻訳はREADME.mdを更新すると自動的に実行されます:

```bash
# Edit your README.md
git add README.md
git commit -m "Update README"
git push origin main

# Translation will run automatically
# Check the 'locales/' folder for results
```

## 🚀高度な機能

### スマート用語保護

技術用語を翻訳されないように保護します:

```yaml
protected_terms:
  - "GitHub Actions"
  - "API"
  - "Docker"
  - "Node.js"
  - "YourProjectName"
```

### 保護を上書きします

既存の翻訳がどのように処理されるかを制御します:

```yaml
translation:
  overwrite_mode: "auto"  # Options: "always", "never", "auto", "create_new"
```

### マニュアル編集保護

上書きを防ぐために、翻訳ファイルにこのコメントを追加します。

```html
<!-- MANUAL EDIT -->
```

## 貢献

貢献を歓迎します！これがあなたが助けることができる方法です:

### 貢献方法

1。**🐛レポートバグ**  - 問題を見つけましたか？教えてください！
2。
3。
4。**🔧コードを送信**  - バグを修正するか、機能を追加
5。**🌍言語サポートを追加**  - より多くの言語をサポートする

### 開発プロセス

1. リポジトリをフォークします
2。機能ブランチを作成:`git checkout -b feature/amazing-feature`
3. 変更を加えてテストします
4。変更をコミット:`git commit -m 'Add amazing feature'`
5。ブランチへのプッシュ:`git push origin feature/amazing-feature`
6. プルリクエストを開きます

### 変更をテストします

```bash
# Test the free translation mode
python .github/scripts/translate_readme_free.py

# Test with your own README
# Make sure translations work correctly
```

## 📄ライセンス

このプロジェクトは、MITライセンスに基づいてライセンスされています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## - 翻訳サービスを提供してくれたGoogle Translateに感謝します
 - このツールの改善を支援してくれたすべての貢献者に感謝します
 - アクセス可能な多言語ドキュメントの必要性に触発されました
 - オープンソースコミュニティ向けにbulitive❤️

## 📞サポートとヘルプ

助けが必要な場合、または質問がある場合:

- 🐛**問題**:[GitHub Issues](https://github.com/1038lab/i18n/issues)
- 📖**ドキュメント**:[README_en.md](README_en.md) | [README_zh.md](README_zh.md)
- 💡**機能リクエスト**:「拡張」ラベルで問題を開きます
- 🤝**ディスカッション**:一般的な質問にはGitHubディスカッションを使用します

### 一般的な問題

 -  **翻訳が機能していませんか？**構成ファイルを確認します
 -  ** Therm_1_11_エラー？
 -  **ファイルは更新されていませんか？**上書きモードの設定を確認します

- --

🌐**世界をよりアクセスしやすくする、一度に1つの翻訳** | [1038lab](https://github.com/1038lab)によって❤️で作られています

---
> 🌐 この文書は Google Translate で自動翻訳されています。[英語版](./README_en.md)もご確認ください | 翻訳ツール: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-TRANSLATED -->