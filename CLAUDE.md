# 청소력 - 청소기 리뷰 전문 블로그

## 프로젝트 개요

- **사이트명**: 청소력
- **주제**: 청소기 전문 리뷰 블로그 (무선청소기, 로봇청소기, 물걸레청소기)
- **수익화**: 쿠팡 파트너스
- **URL**: https://cheongso-ryeok.pages.dev
- **스택**: Astro + TailwindCSS + MDX

## 콘텐츠 유형

### 1. 리뷰 (`/src/content/review/`)
- 개별 제품 심층 리뷰
- 필수 필드: product, brand, type, rating, price, pros, cons, coupangUrl

### 2. 비교 (`/src/content/compare/`)
- 2~4개 제품 비교 분석
- 필수 필드: products, type, winner

### 3. 가이드 (`/src/content/guide/`)
- 구매 가이드, 사용 팁, 관리 방법
- 필수 필드: category

---

## 자료 수집 방법

리뷰/비교 글 작성 시 아래 소스에서 자료를 수집합니다.

### 1. YouTube 자막 (필수!)

**YouTube 자막 수집은 필수입니다. 최소 2개 이상의 리뷰 영상 자막을 수집해야 합니다.**

**수집 방법**: Claude가 직접 Python으로 자막 추출

```bash
# Step 1: WebSearch로 YouTube 영상 찾기
검색어: "{제품명} 리뷰 site:youtube.com"

# Step 2: 검색 결과에서 video ID 추출
# youtube.com/watch?v=ABC123 → ABC123
# youtu.be/ABC123 → ABC123

# Step 3: 자막 추출 실행
python -c "
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ['VIDEO_ID_1', 'VIDEO_ID_2']

for vid in video_ids:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['ko', 'en'])
        text = ' '.join([t['text'] for t in transcript])
        print(f'\\n=== {vid} ===')
        print(text[:2000])
    except Exception as e:
        print(f'Error {vid}: {e}')
"
```

**자막에서 추출할 정보**:
- **장점**: 리뷰어가 칭찬하는 부분
- **단점**: 아쉬운 점, 불만 사항
- **실사용 팁**: 사용 노하우
- **비교 의견**: 다른 제품과의 비교

### 2. 쿠팡 리뷰

**수집 방법**: 사용자가 쿠팡 상품 페이지의 리뷰를 복사해서 제공

**Claude 활용법**:
- 긍정/부정 리뷰 분류
- 반복되는 불만 사항 파악
- 실사용자 관점의 장단점 추출

### 3. 네이버/구글 블로그

**수집 방법**:
- WebSearch로 "{제품명} 후기", "{제품명} 단점" 검색
- WebFetch로 주요 블로그 글 내용 가져오기

**Claude 활용법**:
- 장기 사용 후기 정보 수집
- A/S 경험담 파악
- 실제 사용 환경에서의 문제점 확인

### 4. 공식 스펙

**수집 방법**:
- 제조사 공식 사이트에서 스펙 확인
- WebFetch로 스펙 페이지 크롤링

**Claude 활용법**:
- 정확한 스펙 테이블 작성
- 경쟁 제품과 스펙 비교표 생성

### 5. 제품 이미지 (자동 수집)

**수집 방법**:
1. WebFetch로 공식몰/쿠팡 페이지에서 이미지 URL 추출
2. curl로 이미지 다운로드하여 `src/assets/`에 저장

**Claude 실행 명령어**:
```bash
# 이미지 URL 확인 후 다운로드
curl -L -o "src/assets/{브랜드}-{모델명}.jpg" "{이미지URL}"
```

**이미지 소스 우선순위**:
1. 제조사 공식몰 (저작권 가장 안전)
2. 공식 보도자료
3. 쿠팡/다나와 상품 이미지

**frontmatter 적용**:
```yaml
heroImage: "../../assets/{브랜드}-{모델명}.jpg"
```

---

## 리뷰 작성 가이드라인

### 구조 (권장)

```markdown
## {제품명}이란?
간단한 제품 소개 (1-2문단)

> **3줄 요약**
> 1. 핵심 장점
> 2. 주요 특징
> 3. 추천 대상 또는 주의점

## 주요 스펙
| 항목 | 스펙 |
테이블 형식으로 정리

## 실사용 후기
### 소제목 1 (질문 형식 권장: "흡입력은 어떤가?")
내용...

### 소제목 2
내용...

## 어떤 분께 추천하나요?
- 추천 대상 리스트

## 결론
최종 요약 (2-3문장)
```

### 톤앤매너

- **객관적**: 장점만 나열하지 말고 단점도 솔직하게
- **실용적**: 실제 사용 관점에서 유용한 정보 위주
- **비교 관점**: 경쟁 제품 대비 어떤 점이 다른지
- **구체적**: "좋다" 대신 "흡입력 230AW로 카펫 먼지도 제거"

### SEO 고려사항

- 제목에 핵심 키워드 포함 (제품명 + "리뷰" 또는 "후기")
- description 60자 내외로 핵심 요약
- H2/H3 소제목에 관련 키워드 자연스럽게 배치
- 비교 테이블 적극 활용

---

## 슬래시 커맨드

- `/write-review` - 새 리뷰 작성 워크플로우
- `/write-compare` - 비교 분석 글 작성 워크플로우
- `/collect-data` - 특정 제품 자료 수집 가이드

---

## 개발 명령어

```bash
bun run dev      # 개발 서버 (localhost:4321)
bun run build    # 프로덕션 빌드
bun run preview  # 빌드 미리보기
```

## 배포

- main 브랜치 푸시 → Cloudflare Pages 자동 배포 (설정 필요)
