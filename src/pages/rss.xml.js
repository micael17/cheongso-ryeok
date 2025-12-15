import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE_TITLE, SITE_DESCRIPTION } from '../consts';

export async function GET(context) {
	const reviews = await getCollection('review');
	const compares = await getCollection('compare');
	const guides = await getCollection('guide');

	const allPosts = [
		...reviews.map((post) => ({
			...post.data,
			link: `/review/${post.id}/`,
		})),
		...compares.map((post) => ({
			...post.data,
			link: `/compare/${post.id}/`,
		})),
		...guides.map((post) => ({
			...post.data,
			link: `/guide/${post.id}/`,
		})),
	].sort((a, b) => b.pubDate.valueOf() - a.pubDate.valueOf());

	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: allPosts,
	});
}
