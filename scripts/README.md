# 자료 수집 스크립트

청소기 리뷰 작성에 필요한 자료를 수집하는 스크립트들입니다.

## 설치

```bash
cd scripts
pip install -r requirements.txt
```

## YouTube 자막 수집

### 기본 사용법

```bash
# 단일 영상 (URL)
python youtube_transcript.py --urls "https://www.youtube.com/watch?v=VIDEO_ID"

# 여러 영상 (URL)
python youtube_transcript.py --urls URL1 URL2 URL3

# Video ID로 직접 입력
python youtube_transcript.py --ids VIDEO_ID1 VIDEO_ID2
```

### 자막 목록 확인

영상에 어떤 자막이 있는지 먼저 확인할 수 있습니다.

```bash
python youtube_transcript.py --ids VIDEO_ID --list
```

출력 예시:
```
[자막 목록] https://youtube.com/watch?v=VIDEO_ID

언어             코드        유형             번역 가능
-------------------------------------------------------
Korean          ko         수동 작성         O
English         en         자동 생성         O
```

### 출력 형식

```bash
# 기본 텍스트 형식
python youtube_transcript.py --ids VIDEO_ID

# JSON 형식 (프로그램 처리용)
python youtube_transcript.py --ids VIDEO_ID --format json

# 마크다운 형식 (리뷰 작성용)
python youtube_transcript.py --ids VIDEO_ID --format markdown
```

### 파일로 저장

```bash
# 마크다운으로 저장 (리뷰 자료로 활용)
python youtube_transcript.py --ids VIDEO_ID --format markdown -o research.md

# JSON으로 저장
python youtube_transcript.py --ids VIDEO_ID --format json -o data.json
```

### 언어 설정

```bash
# 일본어 우선, 없으면 영어
python youtube_transcript.py --ids VIDEO_ID --languages ja en

# 영어 자막을 한국어로 번역
python youtube_transcript.py --ids VIDEO_ID --translate ko
```

### YouTube 검색으로 자동 수집 (API 키 필요)

```bash
# 환경변수에 API 키 설정 (Windows)
set YOUTUBE_API_KEY=your-api-key

# 환경변수에 API 키 설정 (Linux/Mac)
export YOUTUBE_API_KEY="your-api-key"

# 검색어로 상위 5개 영상 자막 수집
python youtube_transcript.py "다이슨 V15 리뷰" --count 5
```

## YouTube API 키 발급 (선택사항)

검색 기능을 사용하려면 API 키가 필요합니다. URL/ID 직접 입력은 API 키 없이 가능합니다.

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. YouTube Data API v3 활성화
4. 사용자 인증 정보 → API 키 생성

## 리뷰 작성 워크플로우

1. YouTube에서 제품 리뷰 영상 URL 수집
2. 자막 추출 및 마크다운 저장
   ```bash
   python youtube_transcript.py --urls URL1 URL2 --format markdown -o dyson-v15-research.md
   ```
3. 수집된 자료를 바탕으로 리뷰 작성

## 출력 형식 예시

### 텍스트 (기본)

```
============================================================
## Video dQw4w9WgXcQ
채널: Unknown
URL: https://youtube.com/watch?v=dQw4w9WgXcQ
자막: ko (수동)
============================================================

자막 내용이 여기에 출력됩니다...
```

### JSON

```json
[
  {
    "video_id": "dQw4w9WgXcQ",
    "title": "Video dQw4w9WgXcQ",
    "channel": "Unknown",
    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
    "language": "ko",
    "is_generated": false,
    "text": "자막 전체 텍스트...",
    "segments": [
      {"text": "첫 번째 자막", "start": 0.0, "duration": 2.5},
      {"text": "두 번째 자막", "start": 2.5, "duration": 3.0}
    ]
  }
]
```

## 주의사항

- 자막이 없는 영상은 수집 불가
- 연령 제한 영상은 자막 접근 제한
- API 키 없이는 검색 기능 사용 불가 (URL/ID 직접 입력은 가능)
- 대량 요청 시 IP 차단 가능성 있음
