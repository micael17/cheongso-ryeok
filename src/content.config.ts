import { defineCollection, z } from 'astro:content';

const review = defineCollection({
	type: 'content',
	schema: ({ image }) => z.object({
		title: z.string(),
		description: z.string(),
		product: z.string(),
		brand: z.string(),
		type: z.enum(['무선청소기', '로봇청소기', '물걸레청소기', '핸디청소기', '스틱청소기']),
		rating: z.number().min(1).max(5),
		price: z.string(),
		pros: z.array(z.string()).optional(),
		cons: z.array(z.string()).optional(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: image().optional(),
		coupangUrl: z.string().optional(),
		draft: z.boolean().optional(),
	}),
});

const compare = defineCollection({
	type: 'content',
	schema: ({ image }) => z.object({
		title: z.string(),
		description: z.string(),
		products: z.array(z.string()),
		type: z.enum(['무선청소기', '로봇청소기', '물걸레청소기', '핸디청소기', '스틱청소기']),
		winner: z.string().optional(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: image().optional(),
		draft: z.boolean().optional(),
	}),
});

const guide = defineCollection({
	type: 'content',
	schema: ({ image }) => z.object({
		title: z.string(),
		description: z.string(),
		category: z.enum(['구매가이드', '사용팁', '관리방법', '기타']),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: image().optional(),
		draft: z.boolean().optional(),
	}),
});

export const collections = { review, compare, guide };
