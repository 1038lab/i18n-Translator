# GitHub i18n 작업 자동 번역

## 🌍 사용 가능한 언어

| 🌐 언어 | 📄 파일 | 📊 상태 |
|:-----------|:--------|:----------|
| 영어 | [README_en.md](./README_en.md) | ✅ 사용 가능 |
| 영어 | [README_en.md](./README_en.md) | ✅ 사용 가능 |
| 중국어(中文) | [README_zh.md](./README_zh.md) | ✅ 사용 가능 |
| 일본어(日本語) | [README_ja.md](./README_ja.md) | ✅ 사용 가능 |
| 한국어(한국어) | [README_ko.md](./README_ko.md) | ✅ 사용 가능 |
| 스페인어(Español) | [README_es.md](./README_es.md) | ✅ 사용 가능 |
| 프랑스어(Français) | [README_fr.md](./README_fr.md) | ✅ 사용 가능 |
| 러시아어(Русский) | [README_ru.md](./README_ru.md) | ✅ 사용 가능 |

## 📋 **개요**

이 가이드는 제공된 도구를 사용하여 영어 README.md 파일을 여러 언어로 자동 번역하는 GitHub Actions 자동 번역 시스템을 빠르게 설정하는 데 도움이 됩니다.

**🆓 이제 두 가지 번역 모드를 제공합니다.**
- **무료 모드** (권장) - 구성 없음, API 키 필요 없음
- **API 모드** - Google Translate API를 사용하여 더 높은 정확도 제공 (API 키 필요)

### **특징**
- ✅ **두 가지 번역 모드**: 무료(무설정) 및 API(고품질)
- ✅ README.md 업데이트를 자동으로 감지하고 번역을 트리거합니다.
- ✅ 여러 대상 언어(중국어, 일본어, 한국어, 스페인어 등)를 지원합니다.
- ✅ 기술 용어의 번역을 방지합니다.
- ✅ 완벽한 Markdown 서식을 유지합니다.
- ✅ 안전한 API 키 관리(API 모드만 해당)
- ✅ 증분 번역(업데이트된 콘텐츠만 번역)
- ✅ 아름다운 언어 탐색 기능
- ✅ API 비용 절감을 위한 켜기/끄기 스위치
- ✅ 스마트 덮어쓰기 보호(4가지 모드)
- ✅ 수동 편집 감지 및 보호
- ✅ 강제 옵션을 사용한 수동 워크플로 트리거

---

## 🆓 **빠른 시작(무료 모드 - 권장)**

### **1단계: 프로젝트 파일 복사**
[i18n](https://github.com/1038lab/i18n) 프로젝트에서 다음 파일을 프로젝트로 복사하세요.

__코드_0__

### **2단계: 무료 번역 실행**
1. GitHub 저장소에서 **"작업"** 탭을 클릭합니다.
2. **"README 자동 번역(무료)"** 워크플로를 선택합니다.
3. **"워크플로 실행"**을 클릭합니다. → `main` 브랜치를 선택합니다. → **"워크플로 실행"**을 클릭합니다.
4. 완료될 때까지 기다린 후 `locales/` 폴더에서 번역된 파일을 확인합니다.

**🎉 끝! API 키가 필요 없습니다.**

---

## 💰 **API 모드로 업그레이드(선택 사항 - 더 높은 품질)**

더 높은 번역 정확도를 원하시면 API 모드로 업그레이드하세요.

## 🚀 **1단계: Google Cloud Translation 설정 API**

### **1.1 Google Cloud 프로젝트 만들기**
1. [Google Cloud Console](https://console.cloud.google.com/) 페이지로 이동하세요.
2. 프로젝트 선택기를 클릭하고 새 프로젝트를 만드세요.
3. 프로젝트 이름을 입력하세요(예: `readme-translator`).
4. "만들기"를 클릭하세요.

### **1.2 번역 API 활성화**
1. Google Cloud Console에서 올바른 프로젝트를 선택했는지 확인하세요.
2. 검색창에서 "Cloud Translation API"을 검색하세요.
3. "Cloud Translation API" 결과를 클릭하세요.
4. "활성화" 버튼을 클릭하세요.
5. API가 활성화될 때까지 기다리세요.

### **1.3 API 키 생성**
1. "APIs & Services" → "Credentials"로 이동합니다.
2. "Create Credentials" → "API Key"를 클릭합니다.
3. 생성된 API 키를 복사합니다(형식: `AIzaSyC...`)
4. **중요**: 이 키는 나중에 필요하므로 즉시 저장하십시오.

### **1.4 API 키 권한 제한(권장)**
1. '사용자 인증 정보' 페이지에서 방금 생성한 API 키를 클릭합니다.
2. "API 제한" 섹션에서 다음을 수행합니다.
- "키 제한"을 선택합니다.
- "Cloud Translation API"을 선택합니다.
3. "저장"을 클릭합니다.

---

## 🔐 **2단계: API 설정 GitHub 입력**

### **2.1 저장소 비밀번호 설정**
1. GitHub 저장소에서 **"설정"** 탭을 클릭합니다.
2. 왼쪽 메뉴에서 **"비밀 및 변수"** → **"작업"**을 선택합니다.
3. **"새 저장소 비밀번호"**를 클릭합니다.
4. 다음 정보를 입력합니다.
- **이름**: `GOOGLE_TRANSLATE_API_KEY`
- **비밀**: 1.3단계에서 얻은 API 키를 붙여넣습니다.
5. **"비밀 추가"**를 클릭합니다.

### **2.2 비밀 설정 확인**
설정 후 비밀 목록에 다음이 표시됩니다.
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **3단계: API 모드로 전환**

### **3.1 구성 업데이트**
`.github/i18n-config.yml`를 열고 모드를 변경하세요.

__코드_2__

### **3.2 파일 설명**
- **`i18n-config.yml`** - 번역 구성 파일, 언어 제어, 용어 보호 등
- **`translate-readme-api.yml`** - API 모드 GitHub 작업 워크플로 파일
- **`translate-readme-free.yml`** - 무료 모드 GitHub 작업 워크플로 파일
- **`translate_readme_api.py`** - API 번역 스크립트
- **`translate_readme_free.py`** - 무료 번역 스크립트

---

## ⚙️ **4단계: 번역 설정 구성**

### **4.1 구성 파일 편집**
`.github/i18n-config.yml` 파일을 열고 필요에 따라 수정합니다.

#### **번역 모드 선택**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **대상 언어 선택**
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

#### **프로젝트별 용어 추가**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **덮어쓰기 모드 설정**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 구성 설명**
- **`enabled`**: 자동 번역 활성화 여부를 제어합니다.
- **`mode`**: 번역 모드 - `"free"` (API 키 없음) 또는 `"api"` (고품질)
- **`enabled_languages`**: 번역할 대상 언어 목록
- **`protected_terms`**: 번역하지 않을 용어 목록
- **`output_dir`**: 번역 파일 출력 디렉터리(기본값: `locales`)
- **`overwrite_mode`**: 덮어쓰기 모드
- `"always"`: 기존 번역 항상 덮어쓰기
- `"never"`: 기존 번역 절대 덮어쓰지 않음
- `"auto"`: 스마트 덮어쓰기(권장)
- `"create_new"`: 날짜 접미사가 있는 새 파일 생성

### **4.3 모드 비교**

| 기능 | 무료 모드 | API 모드 |
|---------|-----------|----------|
| **API 키** | ❌ 필요 없음 | ✅ 필수 |
| **비용** | 🆓 완전 무료 | 💰 사용량 기반 결제 |
| **번역 품질** | ⭐⭐⭐⭐ 좋음 | ⭐⭐⭐⭐⭐ 매우 좋음 |
| **안정성** | ⭐⭐⭐ 보통 | ⭐⭐⭐⭐⭐ 매우 안정적 |
| **설정 난이도** | ⭐⭐⭐⭐⭐ 구성 불필요 | ⭐⭐ API 설정 필요 |

---

## 🧪 **5단계: 번역 시스템 테스트**

### **5.1 커밋 파일**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 수동 트리거 테스트**

**무료 모드:**
1. GitHub 저장소에서 **"작업"** 탭을 클릭합니다.
2. **"README 자동 번역(무료)"** 워크플로를 선택합니다.
3. **"워크플로 실행"** 버튼을 클릭합니다.
4. `main` 브랜치를 선택합니다.
5. 녹색 **"워크플로 실행"** 버튼을 클릭합니다.

**API 모드의 경우:**
1. **"README (API) 자동 번역"** 워크플로를 대신 선택하세요.
2. 위와 동일한 단계를 따르세요.

### **5.3 실행 모니터링**
1. 실행 중인 워크플로 인스턴스를 클릭합니다.
2. `translate` 작업을 클릭합니다.
3. 각 단계를 확장하여 실행 로그를 확인합니다.
4. 오류 메시지가 있는지 확인합니다.

### **5.4 결과 확인**
실행이 성공적으로 완료되면 저장소에 새로 생성된 파일이 표시됩니다.
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**참고**: `locales/` 폴더는 첫 번째 번역 중에 자동으로 생성됩니다.

---

## 🔄 **6단계: 자동화된 워크플로**

### **6.1 자동 트리거**
시스템은 다음과 같은 상황에서 자동으로 번역을 실행합니다.
- `README.md` 파일을 업데이트하고 `main` 브랜치에 푸시하는 경우
- 소스 파일이 번역 파일보다 최신일 때만 재번역(증분 번역)

### **6.2 번역 결과**
각 번역 파일에는 다음이 포함됩니다.
- 🌍 **아름다운 언어 탐색 테이블** - 간편한 언어 전환을 위한 플래그 아이콘 포함
- 📝 **번역된 콘텐츠** - 원본 서식 및 코드 블록 유지
- 🔗 **현지화된 바닥글 정보** - 번역 노트 및 프로젝트 링크 포함
- 🛡️ **수동 편집 보호** - 사용자 수정 사항 자동 감지 및 보호

---

## 💡 **사용 팁**

### **🎛️ 번역 제어**

#### **완전 정지 대 덮어쓰기 제어**

번역 시스템을 제어하는 방법에는 두 가지가 있습니다.

**1. 자동 번역을 완전히 중지합니다.**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ GitHub 작업이 실행되지만 즉시 종료됩니다.
- ✅ API 호출이 수행되지 않습니다(API 모드 비용 절감).
- ✅ 파일이 생성되거나 업데이트되지 않습니다.

**2. 제어 파일 덮어쓰기:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub 작업은 계속 실행됩니다.
- ✅ 새 번역 파일이 없으면 생성합니다.
- ❌ 기존 번역 파일은 업데이트하지 않습니다.

**3. 강제 번역(수동 트리거):**
두 워크플로 모두 수동으로 트리거될 때 `force_translate` 옵션을 지원합니다.
- `enabled: false` 설정을 재정의하려면 `true`로 설정합니다.
- 구성을 변경하지 않고 한 번만 번역하는 데 유용합니다.

#### **덮어쓰기 모드 비교**

| 모드 | 자동 트리거 | 기존 파일 덮어쓰기 | 새 파일 만들기 |
|------|-------------|-------------------|------------------|
| `enabled: false` | ❌ 스크립트 종료 | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ 실행 | ❌ 기존 파일 건너뛰기 | ✅ 새로 만들기 |
| `overwrite_mode: "auto"` | ✅ 실행 | 🤔 스마트 감지 | ✅ 새로 만들기 |
| `overwrite_mode: "always"` | ✅ 실행 | ✅ 항상 덮어쓰기 | ✅ 새로 만들기 |

### **API 비용 절감(API 모드)**
1. **무료 모드 사용**: `mode: "free"`을 설정하여 비용을 절감합니다.
2. **번역 비활성화**: `i18n-config.yml`에 `enabled: false`을 설정합니다.
3. **언어 줄이기**: 실제로 필요한 언어만 활성화합니다.
4. **증분 번역**: 시스템이 업데이트된 콘텐츠만 자동으로 번역합니다.

### **사용자 지정 용어 보호**
`protected_terms`에 추가:
- 프로젝트 이름
- 특수 기능 이름
- API 엔드포인트 이름
- 브랜드 이름

### **수동 수정 보호**
번역 파일에 마커를 추가하여 수동 수정을 보호하세요.
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **번역 품질 모니터링**
- **무료 모드**: 대부분의 사용 사례에 적합하며 완전 무료입니다.
- **API 모드**: 전문 프로젝트의 정확도 향상
- 번역 결과를 정기적으로 확인합니다.
- 필요에 따라 보호된 용어를 조정합니다.
- 필요한 경우 번역 파일을 수동으로 수정합니다.

---

## 🛠️ **문제 해결**

### **일반적인 문제**

#### **API 키 오류**
```
Error: API connection failed: 403 Forbidden
```
**해결 방법**: API 키가 올바르게 설정되었고 충분한 권한이 있는지 확인하세요.

#### **번역 건너뜀**
```
Skipping zh: locales/README_zh.md is up to date
```
**설명**: 이는 정상적인 증분 번역 동작이며, 소스 파일이 업데이트되지 않았습니다.

#### **번역 비활성화**
```
Translation is disabled in configuration
```
**해결 방법**: `i18n-config.yml`에 `enabled: true`을 설정하거나 `force_translate: true`에 수동 트리거를 사용하세요.

#### **잘못된 워크플로 선택**
**문제**: API 키 없이 API 워크플로를 사용하거나 그 반대로 사용하는 경우
**해결 방법**:
- 무료 모드: "README 자동 번역(무료)" 워크플로를 사용하세요.
- API 모드: "README 자동 번역(API)" 워크플로를 사용하고 API 키가 설정되어 있는지 확인하세요.

### **도움말 받기**
- [project documentation](https://github.com/1038lab/i18n) 보기
- [Issue](https://github.com/1038lab/i18n/issues) 제출
- 작업 실행 로그 확인

---

## 🎉 **완료!**

이제 프로젝트에 자동 번역 기능이 추가되었습니다! README.md를 업데이트할 때마다 시스템이 자동으로 다국어 버전을 생성하여 전 세계 사용자가 프로젝트에 더 쉽게 접근할 수 있도록 지원합니다.

---

> 🌐 이 가이드는 [i18n](https://github.com/1038lab/i18n) 프로젝트에서 제공합니다.


---
> 🌐 이 문서는 Google Translate로 자동 번역되었습니다. [영문 원본](./README_en.md)도 확인해보세요 | 번역 도구: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->