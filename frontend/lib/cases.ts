import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';

// Resolve paths relative to this file's location (lib/) for reliable builds
const casesDirectory = process.cwd() + '/cases';

export interface CaseSummary {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  keywords: string[];
  description: string;
  client: string;
  challenge: string;
  solution: string;
  results: string;
  readingTime: number;
}

export interface CaseStudy extends CaseSummary {
  content: string;
}

export function getAllCases(): CaseSummary[] {
  try {
    if (!fs.existsSync(casesDirectory)) {
      return [];
    }
    const fileNames = fs.readdirSync(casesDirectory);
    const allCasesData = fileNames
      .filter(fileName => fileName.endsWith('.md'))
      .map(fileName => {
        const slug = fileName.replace(/\.md$/, '');
        const fullPath = path.join(casesDirectory, fileName);
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
          client: data.client || '',
          challenge: data.challenge || '',
          solution: data.solution || '',
          results: data.results || '',
          readingTime,
        };
      });

    return allCasesData.sort((a, b) => {
      if (a.date < b.date) {
        return 1;
      } else {
        return -1;
      }
    });
  } catch (error) {
    console.error('Error reading case studies:', error);
    return [];
  }
}

export function getCaseBySlug(slug: string): CaseStudy | null {
  try {
    const fullPath = path.join(casesDirectory, `${slug}.md`);
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
      client: data.client || '',
      challenge: data.challenge || '',
      solution: data.solution || '',
      results: data.results || '',
      content,
      readingTime,
    };
  } catch (error) {
    console.error(`Error reading case study ${slug}:`, error);
    return null;
  }
}

export async function markdownToHtml(markdown: string): Promise<string> {
  const result = await marked(markdown);
  return result;
}
