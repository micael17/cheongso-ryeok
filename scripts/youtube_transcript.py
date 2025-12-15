#!/usr/bin/env python3
"""
YouTube 자막 수집 스크립트

사용법:
    python youtube_transcript.py --urls URL1 URL2 URL3
    python youtube_transcript.py --ids VIDEO_ID1 VIDEO_ID2
    python youtube_transcript.py --ids VIDEO_ID --list  # 사용 가능한 자막 확인
    python youtube_transcript.py "검색어" --count 5  # API 키 필요

설치:
    pip install -r requirements.txt
"""

import argparse
import json
import re
import sys
from typing import Optional


def extract_video_id(url: str) -> Optional[str]:
    """YouTube URL에서 video ID 추출"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # URL이 아닌 ID로 간주
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None


def list_transcripts(video_id: str) -> None:
    """비디오의 사용 가능한 자막 목록 출력"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        print(f"\n[자막 목록] https://youtube.com/watch?v={video_id}\n")
        print(f"{'언어':<15} {'코드':<10} {'유형':<15} {'번역 가능'}")
        print("-" * 55)

        for transcript in transcript_list:
            lang_type = "자동 생성" if transcript.is_generated else "수동 작성"
            translatable = "O" if transcript.is_translatable else "X"
            print(f"{transcript.language:<15} {transcript.language_code:<10} {lang_type:<15} {translatable}")

        print()
    except Exception as e:
        print(f"[ERROR] 자막 목록 조회 실패: {e}", file=sys.stderr)


def get_transcript(
    video_id: str,
    languages: list = ['ko', 'en'],
    translate_to: Optional[str] = None
) -> Optional[dict]:
    """비디오 자막 가져오기

    Returns:
        dict: {
            'video_id': str,
            'language': str,
            'is_generated': bool,
            'text': str,
            'segments': list
        }
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        ytt_api = YouTubeTranscriptApi()

        # 자막 목록에서 원하는 언어 찾기
        transcript_list = ytt_api.list(video_id)
        transcript = transcript_list.find_transcript(languages)

        # 번역 요청시
        if translate_to and transcript.is_translatable:
            transcript = transcript.translate(translate_to)

        # 자막 가져오기
        fetched = transcript.fetch()

        # 텍스트 합치기
        full_text = ' '.join([t.text for t in fetched])

        return {
            'video_id': video_id,
            'language': transcript.language_code,
            'is_generated': transcript.is_generated,
            'text': full_text,
            'segments': [{'text': t.text, 'start': t.start, 'duration': t.duration} for t in fetched]
        }
    except Exception as e:
        print(f"[ERROR] {video_id}: {e}", file=sys.stderr)
        return None


def search_videos(query: str, max_results: int = 5) -> list:
    """YouTube 검색 (API 키 필요)"""
    try:
        from googleapiclient.discovery import build
        import os

        api_key = os.environ.get('YOUTUBE_API_KEY')
        if not api_key:
            print("[WARNING] YOUTUBE_API_KEY 환경변수가 설정되지 않았습니다.", file=sys.stderr)
            print("API 키 없이는 검색이 불가능합니다. --urls 또는 --ids 옵션을 사용하세요.", file=sys.stderr)
            return []

        youtube = build('youtube', 'v3', developerKey=api_key)

        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=max_results,
            relevanceLanguage='ko'
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description']
            })
        return videos
    except ImportError:
        print("[ERROR] google-api-python-client가 설치되지 않았습니다.", file=sys.stderr)
        print("pip install google-api-python-client", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[ERROR] 검색 실패: {e}", file=sys.stderr)
        return []


def format_output_text(results: list, video_info: dict) -> str:
    """텍스트 형식 출력"""
    output_lines = []

    for result in results:
        vid = result['video_id']
        info = video_info.get(vid, {})
        title = info.get('title', f'Video {vid}')
        channel = info.get('channel', 'Unknown')

        lang_type = "자동 생성" if result['is_generated'] else "수동"

        output_lines.append(f"\n{'='*60}")
        output_lines.append(f"## {title}")
        output_lines.append(f"채널: {channel}")
        output_lines.append(f"URL: https://youtube.com/watch?v={vid}")
        output_lines.append(f"자막: {result['language']} ({lang_type})")
        output_lines.append(f"{'='*60}\n")
        output_lines.append(result['text'])
        output_lines.append("")

    return '\n'.join(output_lines)


def format_output_json(results: list, video_info: dict) -> str:
    """JSON 형식 출력"""
    output = []
    for result in results:
        vid = result['video_id']
        info = video_info.get(vid, {})
        output.append({
            'video_id': vid,
            'title': info.get('title', f'Video {vid}'),
            'channel': info.get('channel', 'Unknown'),
            'url': f'https://youtube.com/watch?v={vid}',
            'language': result['language'],
            'is_generated': result['is_generated'],
            'text': result['text'],
            'segments': result['segments']
        })
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_output_markdown(results: list, video_info: dict) -> str:
    """마크다운 형식 출력 (리뷰 작성용)"""
    output_lines = ["# YouTube 자막 수집 결과\n"]

    for i, result in enumerate(results, 1):
        vid = result['video_id']
        info = video_info.get(vid, {})
        title = info.get('title', f'Video {vid}')
        channel = info.get('channel', 'Unknown')

        output_lines.append(f"## {i}. {title}\n")
        output_lines.append(f"- **채널**: {channel}")
        output_lines.append(f"- **URL**: https://youtube.com/watch?v={vid}")
        output_lines.append(f"- **자막 언어**: {result['language']}")
        output_lines.append("")
        output_lines.append("### 내용")
        output_lines.append("")
        output_lines.append(result['text'])
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

    return '\n'.join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description='YouTube 자막 수집기 - 청소기 리뷰 자료 수집용',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # URL로 자막 수집
  python youtube_transcript.py --urls "https://youtube.com/watch?v=xxxxx"

  # 여러 영상 자막 수집
  python youtube_transcript.py --ids VIDEO_ID1 VIDEO_ID2 VIDEO_ID3

  # 사용 가능한 자막 목록 확인
  python youtube_transcript.py --ids VIDEO_ID --list

  # JSON 형식으로 출력
  python youtube_transcript.py --ids VIDEO_ID --format json

  # 마크다운으로 저장 (리뷰 작성용)
  python youtube_transcript.py --ids VIDEO_ID --format markdown -o research.md

  # 영어 자막을 한국어로 번역
  python youtube_transcript.py --ids VIDEO_ID --translate ko
        """
    )
    parser.add_argument('query', nargs='?', help='검색어 (YOUTUBE_API_KEY 환경변수 필요)')
    parser.add_argument('--count', '-c', type=int, default=5, help='검색 결과 수 (기본: 5)')
    parser.add_argument('--urls', '-u', nargs='+', help='YouTube URL 목록')
    parser.add_argument('--ids', '-i', nargs='+', help='Video ID 목록')
    parser.add_argument('--output', '-o', help='출력 파일 (기본: stdout)')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text',
                       help='출력 형식 (기본: text)')
    parser.add_argument('--list', '-l', action='store_true', help='사용 가능한 자막 목록 확인')
    parser.add_argument('--languages', nargs='+', default=['ko', 'en'],
                       help='자막 언어 우선순위 (기본: ko en)')
    parser.add_argument('--translate', '-t', help='자막을 지정 언어로 번역 (예: ko, en)')

    args = parser.parse_args()

    video_ids = []
    video_info = {}

    # URL에서 ID 추출
    if args.urls:
        for url in args.urls:
            vid = extract_video_id(url)
            if vid:
                video_ids.append(vid)
                video_info[vid] = {'title': f'Video {vid}', 'channel': 'Unknown'}
            else:
                print(f"[WARNING] 잘못된 URL: {url}", file=sys.stderr)

    # 직접 ID 입력
    if args.ids:
        for vid in args.ids:
            extracted = extract_video_id(vid)
            if extracted:
                video_ids.append(extracted)
                video_info[extracted] = {'title': f'Video {extracted}', 'channel': 'Unknown'}

    # 검색
    if args.query and not video_ids:
        print(f"[INFO] '{args.query}' 검색 중...", file=sys.stderr)
        videos = search_videos(args.query, args.count)
        for v in videos:
            video_ids.append(v['id'])
            video_info[v['id']] = {
                'title': v['title'],
                'channel': v['channel'],
                'description': v.get('description', '')
            }

    if not video_ids:
        print("[ERROR] 처리할 비디오가 없습니다.", file=sys.stderr)
        print("\n사용 예시:", file=sys.stderr)
        print("  python youtube_transcript.py --urls https://youtube.com/watch?v=xxxxx", file=sys.stderr)
        print("  python youtube_transcript.py --ids VIDEO_ID1 VIDEO_ID2", file=sys.stderr)
        print("  python youtube_transcript.py --ids VIDEO_ID --list", file=sys.stderr)
        sys.exit(1)

    # 자막 목록 확인 모드
    if args.list:
        for vid in video_ids:
            list_transcripts(vid)
        sys.exit(0)

    # 자막 수집
    results = []

    for vid in video_ids:
        info = video_info.get(vid, {})
        title = info.get('title', f'Video {vid}')

        print(f"[INFO] 자막 수집: {title}", file=sys.stderr)

        transcript = get_transcript(
            vid,
            languages=args.languages,
            translate_to=args.translate
        )

        if transcript:
            results.append(transcript)
            print(f"[OK] {vid}: {len(transcript['text'])} 글자 수집", file=sys.stderr)

    if not results:
        print("[ERROR] 수집된 자막이 없습니다.", file=sys.stderr)
        sys.exit(1)

    # 출력 형식 선택
    if args.format == 'json':
        output = format_output_json(results, video_info)
    elif args.format == 'markdown':
        output = format_output_markdown(results, video_info)
    else:
        output = format_output_text(results, video_info)

    # 출력
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"[INFO] 저장됨: {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"\n[완료] {len(results)}개 영상 자막 수집", file=sys.stderr)


if __name__ == '__main__':
    main()
