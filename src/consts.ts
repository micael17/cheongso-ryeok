// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

export const SITE_NAME = '청소력';
export const SITE_TITLE = '청소력 - 청소기 리뷰 전문 블로그';
export const SITE_DESCRIPTION = '무선청소기, 로봇청소기, 물걸레청소기 리뷰 및 비교 분석';
export const SITE_URL = 'https://cheongso-ryeok.pages.dev';
export const SITE_LOCALE = 'ko_KR';
export const SITE_AUTHOR = '청소력';

// Content Categories
export const CATEGORIES = {
  REVIEW: 'review',
  COMPARE: 'compare',
  GUIDE: 'guide',
} as const;

// 청소기 타입
export const VACUUM_TYPES = {
  WIRELESS: '무선청소기',
  ROBOT: '로봇청소기',
  MOP: '물걸레청소기',
  HANDHELD: '핸디청소기',
  STICK: '스틱청소기',
} as const;

// 브랜드
export const BRANDS = [
  '다이슨',
  'LG',
  '삼성',
  '샤오미',
  '로보락',
  '에코백스',
  '드리미',
  '일렉트로룩스',
  '테팔',
  '발뮤다',
] as const;
