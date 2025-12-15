# 청소기 리뷰 자료 수집 가이드

특정 제품에 대한 리뷰 자료를 수집하는 방법을 안내합니다.

## 수집할 제품 확인

사용자에게 물어보세요:
- 어떤 제품의 자료를 수집할까요? (예: 다이슨 V15 디텍트)

---

## 자료 수집 방법

### 1. YouTube 자막 수집 (사용자가 직접)

#### 방법 A: Python 스크립트 (추천)

```bash
pip install youtube-transcript-api
```

```python
from youtube_transcript_api import YouTubeTranscriptApi

# 비디오 ID는 YouTube URL에서 추출
# https://www.youtube.com/watch?v=VIDEO_ID
video_ids = [
    "VIDEO_ID_1",
    "VIDEO_ID_2",
    "VIDEO_ID_3"
]

for vid in video_ids:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['ko', 'en'])
        text = ' '.join([t['text'] for t in transcript])
        print(f"\n=== {vid} ===\n{text}\n")
    except Exception as e:
        print(f"Error {vid}: {e}")
```

#### 방법 B: 웹 서비스
- https://downsub.com - YouTube 자막 다운로드
- https://youtubetranscript.com - 자막 텍스트 추출

#### 추천 검색어
- "{제품명} 리뷰"
- "{제품명} 장단점"
- "{제품명} 1개월 사용후기"
- "{제품명} vs {경쟁제품}"

### 2. 쿠팡 리뷰 수집 (사용자가 직접)

1. 쿠팡에서 제품 검색
2. 상품 페이지 → 상품평 탭
3. "최신순" 또는 "베스트순" 정렬
4. 상위 20~30개 리뷰 텍스트 복사

**주의**: 별점 4-5점 리뷰만 보지 말고 1-3점 리뷰도 꼭 확인

### 3. 블로그/커뮤니티 검색 (Claude가 지원)

Claude가 WebSearch + WebFetch로 수집 가능:

```
검색 쿼리 예시:
- "{제품명} 후기 site:blog.naver.com"
- "{제품명} 단점 site:tistory.com"
- "{제품명} 실사용 site:clien.net"
- "{제품명} 리뷰 site:ppomppu.co.kr"
```

### 4. 공식 스펙 (Claude가 지원)

Claude가 WebFetch로 수집:
- 제조사 공식 홈페이지
- 다나와 스펙 페이지

---

## 자료 제공 형식

사용자가 자료를 제공할 때 권장하는 형식:

```
## YouTube 자막 1: [영상 제목]
[자막 텍스트]

## YouTube 자막 2: [영상 제목]
[자막 텍스트]

## 쿠팡 리뷰
### 긍정 리뷰
- [리뷰 1]
- [리뷰 2]

### 부정 리뷰
- [리뷰 1]
- [리뷰 2]
```

---

## Claude의 자동 수집

사용자가 제품명만 제공하면 Claude가 자동으로:

1. **WebSearch** 실행
   - "{제품명} 스펙"
   - "{제품명} 리뷰 블로그"
   - "{제품명} 장단점"

2. **WebFetch**로 주요 페이지 내용 수집

3. 수집된 내용 요약해서 사용자에게 확인 요청

---

## 예시: 다이슨 V15 디텍트 자료 수집

사용자에게 요청할 내용:

> 다이슨 V15 디텍트 리뷰를 작성하려고 합니다.
>
> 다음 자료를 수집해서 공유해주세요:
>
> 1. **YouTube**: "다이슨 V15 리뷰"로 검색해서 상위 3-5개 영상의 자막
> 2. **쿠팡**: 다이슨 V15 상품평에서 긍정/부정 리뷰 각 10개씩
>
> 공식 스펙과 블로그 후기는 제가 검색해서 보완하겠습니다.

---

## 자료 수집 완료 후

자료가 충분히 모이면:
- 리뷰 작성: `/write-review` 커맨드 실행
- 비교 분석: `/write-compare` 커맨드 실행
