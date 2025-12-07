import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';

const postsDirectory = path.join(process.cwd(), 'posts');

export interface PostSummary {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  keywords: string[];
  description: string;
  readingTime: number;
}

export interface Post extends PostSummary {
  content: string;
}

export function getAllPosts(): PostSummary[] {
  try {
    const fileNames = fs.readdirSync(postsDirectory);
    const allPostsData = fileNames
      .filter(fileName => fileName.endsWith('.md'))
      .map(fileName => {
        const slug = fileName.replace(/\.md$/, '');
        const fullPath = path.join(postsDirectory, fileName);
        const fileContents = fs.readFileSync(fullPath, 'utf8');
        const { data, content } = matter(fileContents);

        // Calculate reading time (average 200 words per minute)
        const wordCount = content.split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / 200);

        return {
          slug,
          title: data.title || slug,
          excerpt: data.excerpt || '',
          date: data.date || new Date().toISOString(),
          keywords: data.keywords || [],
          description: data.description || data.excerpt || '',
          readingTime,
        };
      });

    // Sort posts by date (newest first)
    return allPostsData.sort((a, b) => {
      if (a.date < b.date) {
        return 1;
      } else {
        return -1;
      }
    });
  } catch (error) {
    console.error('Error reading posts:', error);
    return [];
  }
}

export function getPostBySlug(slug: string): Post | null {
  try {
    const fullPath = path.join(postsDirectory, `${slug}.md`);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    const wordCount = content.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200);

    return {
      slug,
      title: data.title || slug,
      excerpt: data.excerpt || '',
      date: data.date || new Date().toISOString(),
      keywords: data.keywords || [],
      description: data.description || data.excerpt || '',
      content,
      readingTime,
    };
  } catch (error) {
    console.error(`Error reading post ${slug}:`, error);
    return null;
  }
}

export async function markdownToHtml(markdown: string): Promise<string> {
  const result = await marked(markdown);
  return result;
}

export function getFeaturedPosts(limit: number = 3): PostSummary[] {
  const allPosts = getAllPosts();
  return allPosts.slice(0, limit);
}
