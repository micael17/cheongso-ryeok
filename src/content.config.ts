import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const review = defineCollection({
	loader: glob({ base: './src/content/review', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			product: z.string(), // 제품명
			brand: z.string(), // 브랜드
			type: z.enum(['무선청소기', '로봇청소기', '물걸레청소기', '핸디청소기', '스틱청소기']),
			rating: z.number().min(1).max(5), // 평점
			price: z.string(), // 가격대
			pros: z.array(z.string()).optional(), // 장점
			cons: z.array(z.string()).optional(), // 단점
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: image().optional(),
			coupangUrl: z.string().optional(), // 쿠팡 파트너스 링크
		}),
});

const compare = defineCollection({
	loader: glob({ base: './src/content/compare', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			products: z.array(z.string()), // 비교 제품들
			type: z.enum(['무선청소기', '로봇청소기', '물걸레청소기', '핸디청소기', '스틱청소기']),
			winner: z.string().optional(), // 추천 제품
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: image().optional(),
		}),
});

const guide = defineCollection({
	loader: glob({ base: './src/content/guide', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			category: z.enum(['구매가이드', '사용팁', '관리방법', '기타']),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: image().optional(),
		}),
});

export const collections = { review, compare, guide };
