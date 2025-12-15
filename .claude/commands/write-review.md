# 청소기 리뷰 작성 워크플로우

제품명만 받으면 자료 수집부터 리뷰 작성까지 자동으로 진행합니다.

## Step 1: YouTube 자막 수집 (필수)

**반드시 YouTube 리뷰 영상 자막을 수집해야 합니다.**

### 1-1. YouTube 검색으로 영상 찾기

WebSearch로 리뷰 영상 검색:
```
검색어: "{제품명} 리뷰 site:youtube.com"
```

### 1-2. 자막 추출 (Python 실행)

검색 결과에서 video ID를 추출하고 자막 수집:

```bash
python -c "
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ['VIDEO_ID_1', 'VIDEO_ID_2', 'VIDEO_ID_3']

for vid in video_ids:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['ko', 'en'])
        text = ' '.join([t['text'] for t in transcript])
        print(f'\\n=== {vid} ===')
        print(text[:2000])  # 앞 2000자
    except Exception as e:
        print(f'Error {vid}: {e}')
"
```

### 1-3. Video ID 추출 방법

YouTube URL에서 ID 추출:
- `https://www.youtube.com/watch?v=ABC123` → `ABC123`
- `https://youtu.be/ABC123` → `ABC123`

### 1-4. 자막 분석 포인트

수집된 자막에서 추출할 정보:
- **장점**: 리뷰어가 칭찬하는 부분
- **단점**: 아쉬운 점, 불만 사항
- **실사용 팁**: 사용 노하우
- **비교 의견**: 다른 제품과의 비교

---

## Step 2: 웹 자료 수집

### 2-1. 공식 스펙 (WebSearch + WebFetch)

```
검색어: "{제품명} 스펙"
검색어: "{브랜드} 공식몰 {모델명}"
```

### 2-2. 블로그/커뮤니티 후기

```
검색어: "{제품명} 후기"
검색어: "{제품명} 단점"
검색어: "{제품명} 장기 사용"
```

### 2-3. 가격 정보

```
검색어: "{제품명} 최저가"
```

---

## Step 3: 제품 이미지 수집

### 3-1. 이미지 URL 찾기

WebFetch로 공식몰 페이지에서 메인 이미지 URL 추출:
```
WebFetch: {공식몰 URL}
프롬프트: "제품 메인 이미지 URL을 찾아주세요. img 태그의 src 속성 값을 추출해주세요."
```

### 3-2. 이미지 다운로드

```bash
curl -L -o "src/assets/{브랜드}-{모델명}.jpg" "{이미지URL}"
```

**파일명 규칙**: 소문자, 하이픈 구분
- 예: `shark-neo-plus.jpg`, `dyson-v15.jpg`

---

## Step 4: 자료 분석 및 정리

수집된 모든 자료에서 다음을 추출:

### 장점 (pros)
- YouTube 자막에서 공통으로 언급되는 장점
- 수치로 표현할 수 있는 장점 우선

### 단점 (cons)
- 여러 리뷰어가 공통으로 지적하는 문제
- 실사용에서 발견되는 문제점

### 핵심 스펙
- 흡입력 (W 또는 AW)
- 배터리 사용 시간
- 무게
- 먼지통 용량
- 특별한 기능

### 실사용 인사이트
- 리뷰어들이 강조하는 포인트
- 예상과 다른 점

---

## Step 5: 리뷰 작성

다음 형식으로 `/src/content/review/` 에 MDX 파일 생성:

```markdown
---
title: "{제품명} 완벽 리뷰 - {핵심 특징 한 줄}"
description: "{60자 내외 요약}"
product: "{제품명}"
brand: "{브랜드}"
type: "{무선청소기|로봇청소기|물걸레청소기}"
rating: {1-5}
price: "{가격대}"
pros:
  - "{장점1}"
  - "{장점2}"
  - "{장점3}"
cons:
  - "{단점1}"
  - "{단점2}"
pubDate: {오늘 날짜 YYYY-MM-DD}
heroImage: "../../assets/{브랜드}-{모델명}.jpg"
coupangUrl: "{쿠팡 파트너스 링크}"
---

## {제품명}이란?

{제품 소개 1-2문단}

> **3줄 요약**
> 1. {핵심 장점}
> 2. {주요 특징}
> 3. {추천 대상}

## 주요 스펙

| 항목 | 스펙 |
|-----|-----|
| 흡입력 | {값} |
| 배터리 | {값} |
| 무게 | {값} |
| 먼지통 | {값} |
| 특징 | {값} |

## 실사용 후기

### {질문형 소제목 1}

{내용 - YouTube 자막 기반}

### {질문형 소제목 2}

{내용}

## 어떤 분께 추천하나요?

- {추천 대상 1}
- {추천 대상 2}
- {추천 대상 3}

## 결론

{최종 요약 2-3문장}
```

---

## Step 6: 평점 기준

| 점수 | 기준 |
|-----|-----|
| 5점 | 가격 대비 최고 성능, 단점이 거의 없음 |
| 4점 | 우수한 제품, 사소한 단점 있음 |
| 3점 | 평균적인 제품, 장단점 명확 |
| 2점 | 단점이 장점보다 많음 |
| 1점 | 추천하기 어려움 |

---

## Step 7: 검수

작성 후 체크리스트:
- [ ] **YouTube 자막 최소 2개 이상 수집했는가?**
- [ ] frontmatter 모든 필드 작성 (heroImage 포함!)
- [ ] 이미지 파일 다운로드 완료
- [ ] 장단점 각 2개 이상
- [ ] 스펙 테이블 포함
- [ ] 3줄 요약 blockquote 포함
- [ ] "추천 대상" 섹션 포함
- [ ] 파일명: `{브랜드}-{모델명}.md`
