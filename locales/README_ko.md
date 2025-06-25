# GitHub i18n 조치 자동 변환
## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |
| Korean (한국어) | [README_ko.md](./README_ko.md) | ✅ Available |

## 🌍 Available Languages

| 🌐 Language | 📄 File | 📊 Status |
|-------------|---------|-----------|
| English | [README_en.md](./README_en.md) | ✅ Available |
| Chinese (中文) | [README_zh.md](./README_zh.md) | ✅ Available |
| Japanese (日本語) | [README_ja.md](./README_ja.md) | ✅ Available |
| Korean (한국어) | [README_ko.md](./README_ko.md) | ✅ Available |

## 📋 ** 개요 **

이 안내서를 사용하면 제공된 도구를 사용하여 영어 README.md 파일을 여러 언어로 자동 번역하기 위해 GitHub 작업 자동 변환 시스템을 신속하게 설정하는 데 도움이됩니다.

* * 🆓 이제 우리는 이제 두 가지 번역 모드를 제공합니다. **
- ** 무료 모드 ** (권장) - 제로 구성, 없음 API 키 필요
- ** API 모드 ** - Google Translate API의 높은 정확도 (API 키 필요)

### **특징**
- ation ** 2 개의 번역 모드 ** : 무료 (Zero-Config) 및 API (고품질)
- s README.md 업데이트 및 변환을 트리거합니다
- langu 여러 대상 언어 (중국어, 일본, 한국, 스페인어 등)를 지원합니다.
- 기술 용어가 번역되지 않도록 보호합니다
- somplete Markdown 형식을 유지합니다
- _ 보안 API 키 관리 (API 모드 만 해당)
- ation 증분 번역 (업데이트 된 콘텐츠 만 번역)
- 아름다운 언어 탐색
- API 비용을 절약하기 위해 켜기/끄기 스위치
- 스마트 덮개 보호 (4 모드)
- 수동 편집 감지 및 보호
- 힘 옵션이있는 수동 워크 플로 트리거

- --

## 🆓 ** 빠른 시작 (무료 모드 - 권장) **

### ** 1 단계 : 프로젝트 파일 복사 **
[i18n](https://github.com/1038lab/i18n) 프로젝트에서 프로젝트에 다음 파일을 복사하십시오.

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

### ** 2 단계 : 무료 번역 실행 **
1. GitHub 저장소에서 ** "조치"** 탭을 클릭하십시오
2. ** "자동 번역 README (무료)"** 워크 플로를 선택하십시오
3. ** "워크 플로 실행"** → `main` branch → "Workflow 실행"** 클릭하십시오.
4. 완료를 기다리고 번역 된 파일의 `locales/` 폴더를 확인하십시오.

* * 🎉 그게 다야! 없음 API 키가 필요합니다. **

- --

## 💰 ** API 모드로 업그레이드 (선택 사항 - 고품질) **

더 높은 번역 정확도를 원한다면 API 모드로 업그레이드 할 수 있습니다.

## 🚀 ** 1 단계 : Google 클라우드 번역 설정 API **

### ** 1.1 Google 클라우드 프로젝트 생성 **
1. [Google Cloud Console](https://console.cloud.google.com/) 방문
2. 프로젝트 선택기를 클릭하고 새 프로젝트를 만듭니다.
3. 프로젝트 이름을 입력하십시오 (예 : `readme-translator`)
4. "Create"를 클릭합니다.

### ** 1.2 번역 활성화 API **
1. Google Cloud Console에서 올바른 프로젝트를 선택했는지 확인하십시오.
2. 검색 창에서 "클라우드 번역 API"검색
3. "클라우드 번역 API"결과를 클릭하십시오
4. "활성화"버튼을 클릭하십시오
5. API가 활성화 될 때까지 기다립니다

### ** 1.3 생성 API 키 **
1. "APIs 및 서비스"→ "자격 증명"으로 이동하십시오.
2. "자격 증명 만들기"→ "API 키"를 클릭하십시오.
3. 생성 된 API 키를 복사하십시오 (다음과 같은 형식 : `AIzaSyC...`)
4. ** 중요 ** :이 키를 즉시 저장하면 나중에 필요합니다.

### ** 1.4 제한 API 키 권한 (권장) **
1. 자격 증명 페이지에서 방금 만든 API 키를 클릭하십시오.
2. "API 제한"섹션에서 :
   - "제한 키"를 선택하십시오.
   - "클라우드 번역 API"확인
3. "저장"을 클릭하십시오.

- --

## 🔐 ** 2 단계 : API GitHub ** 설정 설정

### ** 2.1 세트 리포지토리 비밀 **
1. GitHub 저장소에서 ** "설정"** 탭을 클릭하십시오
2. 왼쪽 메뉴에서 ** "비밀 및 변수"** → ** "Action"**를 선택하십시오.
3. ** "새 저장소 비밀"** 클릭하십시오.
4. 정보 작성 :
   - ** 이름 ** : `GOOGLE_TRANSLATE_API_KEY`
   - ** 비밀 ** : 1.3 단계에서 얻은 API 키를 붙여 넣습니다.
5. ** "비밀 추가"를 클릭하십시오 **

### ** 2.2 비밀 설정 확인 **
설정 후 비밀 목록에 표시됩니다.
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

- --

## 📁 ** 3 단계 : API 모드로 전환 **

### ** 3.1 업데이트 구성 **
`.github/i18n-config.yml`을 열고 모드를 변경하십시오.

```yaml
translation:
  mode: "api"  # Change from "free" to "api"
```

### ** 3.2 파일 설명 **
- ** `i18n-config.yml` ** - 번역 구성 파일, 언어 제어, 용어 보호 등
- ** `translate-readme-api.yml` ** - API 모드 GitHub 작업 플로우 파일
- ** `translate-readme-free.yml` ** - 무료 모드 GitHub 작업 워크 플로 파일
- ** `translate_readme_api.py` ** - API 번역 스크립트
- ** `translate_readme_free.py` ** - 무료 번역 스크립트

- --

4 단계 : 번역 설정 구성 **

### ** 4.1 구성 파일 편집 **
`.github/i18n-config.yml` 파일을 열고 필요에 따라 수정하십시오.

#### ** 번역 모드 선택 **
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### ** 대상 언어 선택 **
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

#### ** 프로젝트 별 용어 추가 **
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### ** 모드 설정을 덮어 쓰기 **
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### ** 4.2 구성 설명 **
- ** `enabled` ** : 자동 변환 활성화 여부를 제어합니다
- ** `mode` ** : 번역 모드 -`"free"` (없음 API 키) 또는 `"api"` (고품질)
- ** `enabled_languages` ** : 번역 할 대상 언어 목록
- ** `protected_terms` ** : 번역되지 말아야 할 약관 목록
- ** `output_dir` ** : 번역 파일의 출력 디렉토리 (기본값 : `locales`)
- ** `overwrite_mode` ** : 덮어 쓰기 모드
  - `"always"` : 항상 기존 번역을 덮어 씁니다
  - `"never"` : 기존 번역을 덮어 쓰지 마십시오
  - `"auto"` : 스마트 덮어 쓰기 (권장)
  - `"create_new"` : 날짜 접미사로 새 파일을 만듭니다

### ** 4.3 모드 비교 **

| 기능 | 자유 모드 | API 모드 |
| :----------- | ---------- | :----------- |
| ** API 키 ** | ❌ 필요하지 | ✅ 필수 |
| ** 비용 ** | 🆓 완전 무료 | 💰 사용 당 급여 |
| ** 번역 품질 ** | ⭐⭐⭐⭐ good | ⭐⭐⭐⭐⭐ 우수 |
| ** 안정성 ** ⭐⭐⭐ 보통 | ⭐⭐⭐⭐⭐ 매우 안정적인 |
| ** 설정 난이도 ** | ⭐⭐⭐⭐⭐ 제로 구성 | ⭐⭐ __THERT_1_32__ 설정 필요 |

- --

## 🧪 ** 5 단계 : 테스트 번역 시스템 **

### ** 5.1 커밋 파일 **
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### ** 5.2 수동 트리거 테스트 **

* * 무료 모드 : **
1. GitHub 저장소에서 ** "작업"** 탭을 클릭하십시오
2. ** "자동 번역 README (무료)"** 워크 플로를 선택하십시오
3. ** "워크 플로 실행"** 버튼을 클릭하십시오
4. `main` 지점을 선택하십시오
5. 녹색 ** "워크 플로 실행"** 버튼을 클릭하십시오

* * API 모드 용 : **
1. ** "auto translate README (API)"** 워크 플로를 선택하십시오
2. 위의 동일한 단계를 따르십시오

### ** 5.3 모니터 실행 **
1. 실행중인 워크 플로 인스턴스를 클릭하십시오
2. `translate` 작업을 클릭하십시오
3. 각 단계를 확장하여 실행 로그를 볼 수 있습니다
4. 오류 메시지를 확인하십시오

### ** 5.4 결과 확인 **
성공적인 실행 후 리포지토리에 새로 생성 된 파일이 표시됩니다.
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

* * 참고 ** : `locales/` 폴더는 첫 번째 번역 중에 자동으로 작성됩니다.

- --

## 🔄 ** 6 단계 : 자동화 된 워크 플로 **

### ** 6.1 자동 트리거 **
시스템은 다음 상황에서 자동으로 번역을 실행합니다.
- `README.md` 파일을 업데이트하고 `main` 지점으로 푸시 할 때
- 소스 파일이 번역 파일보다 새롭고 재전송합니다 (증분 번역)

### ** 6.2 번역 결과 **
각 번역 파일에는 다음이 포함됩니다.
- nav ** 아름다운 언어 탐색 테이블 ** - 쉬운 언어 스위칭을위한 깃발 아이콘 포함
- content ** 번역 된 컨텐츠 ** - 원래 형식 및 코드 블록 유지 관리
- foot ** 현지 바닥 글 정보 ** - 번역 노트 및 프로젝트 링크 포함
- ual️ ** 수동 편집 보호 ** - 사용자 수정을 자동으로 감지하고 보호합니다.

- --

## 💡 ** 사용 팁 **

### ** *️ 번역 제어 **

#### ** Complete Stop vs Overwrite Control **

번역 시스템을 제어하는 ​​두 가지 방법이 있습니다.

* * 1. 자동 변환을 완전히 중지하십시오 : **
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- 0 GitHub 작업은 실행되지만 즉시 종료합니다
- sally 전화 통화 (API 모드에 대한 비용 절약)
- created 파일이 생성되거나 업데이트되지 않습니다

* * 2. 제어 파일 덮어 쓰기 : **
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- 0 __term_0___ 조치는 여전히 실행됩니다
- ation 존재하지 않으면 새 번역 파일을 생성합니다.
- ing 기존 번역 파일을 업데이트하지 않습니다

* * 3. 힘 번역 (수동 트리거) : **
두 워크 플로우는 수동으로 트리거 될 때 `force_translate` 옵션을 지원합니다.
- `true`로 설정하여 `enabled: false` 설정을 무시하십시오
- 구성을 변경하지 않고 일회성 번역에 유용합니다

#### ** 모드 비교를 덮어 쓰기 **

| 모드 | 자동 트리거 | 기존 | 새 파일 생성 |
| :----------- | ----------------------------------------------------------------------------------------------------------------- |
| `enabled: false` | ❌ 스크립트 출구 | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ 실행 | ❌ 기존 건너 뛰기 | new |
| `overwrite_mode: "auto"` | ✅ 실행 | 🤔 스마트 감지 | new |
| `overwrite_mode: "always"` | ✅ 실행 | ✅ 항상 덮어 | new |

### ** 저장 API 비용 (API 모드) **
1. ** 무료 모드 사용 ** : `mode: "free"`를 제로 비용으로 설정하십시오
2. ** 번역 비활성화 ** : `i18n-config.yml`에서 `enabled: false`를 설정하십시오.
3. ** 언어 감소 ** : 실제로 필요한 언어 만 가능합니다
4. ** 증분 번역 ** : 시스템은 자동으로 업데이트 된 컨텐츠 만 번역됩니다

### ** 맞춤형 용어 보호 **
`protected_terms`에 추가하십시오 :
- 프로젝트 이름
- 특별 기능 이름
- 1_Term_1_39__ 종말점 이름
- 브랜드 이름

### ** 수동 편집 보호 **
수동 수정을 보호하기 위해 번역 파일에 마커를 추가하십시오.
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### ** 모니터 번역 품질 **
- ** 무료 모드 ** : 대부분의 사용 사례에 적합합니다.
- ** API 모드 ** : 전문 프로젝트의 정확도가 높습니다
- 정기적으로 번역 결과를 확인하십시오
- 필요에 따라 보호 용어를 조정하십시오
- 필요한 경우 번역 파일을 수동으로 수정합니다

- --

## 🛠️ ** 문제 해결 **

### ** 일반적인 문제 **

#### ** API 키 오류 **
```
Error: API connection failed: 403 Forbidden
```
* * 솔루션 ** : API 키가 올바르게 설정되어 있고 충분한 권한이 있는지 확인하십시오.

#### ** 번역 건너 뛰기 **
```
Skipping zh: locales/README_zh.md is up to date
```
* * 설명 ** : 이것은 정상적인 증분 번역 동작입니다. 소스 파일이 업데이트되지 않았습니다.

#### ** 번역 장애 **
```
Translation is disabled in configuration
```
* * 솔루션 ** : `i18n-config.yml`로 `enabled: true`를 설정하거나 `force_translate: true`와 함께 수동 트리거를 사용하십시오.

#### ** 잘못된 워크 플로 선택 **
* * 문제 ** : API API 키 또는 그 반대의 워크 플로 사용
* *해결책**:
- 무료 모드 : "Auto Translate README (무료)"워크 플로 사용
- __RERT_1_45__ 모드의 경우 : "자동 번역 README (API)"워크 플로우를 사용하고 API 키가 설정되어 있는지 확인하십시오.

### ** 도움을 얻으십시오 **
- [project documentation](https://github.com/1038lab/i18n)보기
- [Issue](https://github.com/1038lab/i18n/issues) 제출
- 작업 실행 로그를 점검하십시오

- --

## 🎉 ** 완료! **

프로젝트에는 이제 자동 변환 기능이 있습니다! README.md를 업데이트 할 때마다 시스템은 자동으로 다중 언어 버전을 생성하여 전 세계 사용자가 더 액세스 할 수 있도록합니다.

- --

> by이 안내서는 [i18n](https://github.com/1038lab/i18n) 프로젝트에서 제공합니다.

---

🌐 이 문서는 Google Translate로 자동 번역되었습니다. [영문 원본](./README_en.md)도 확인해보세요 | 번역 도구: [i18n](https://github.com/1038lab/i18n)
