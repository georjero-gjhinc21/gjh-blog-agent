import { MetadataRoute } from 'next'
import { getAllPosts } from '@/lib/posts'
import { getAllCases } from '@/lib/cases'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://gjhconsulting.net'
  const posts = getAllPosts()
  const cases = getAllCases()

  const blogUrls = posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.date),
    changeFrequency: 'monthly' as const,
    priority: 0.8,
  }))

  const caseUrls = cases.map((caseStudy) => ({
    url: `${baseUrl}/cases/${caseStudy.slug}`,
    lastModified: new Date(caseStudy.date),
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }))

  const staticUrls = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 1.0,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.9,
    },
    {
      url: `${baseUrl}/cases`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    },
  ]

  return [...staticUrls, ...caseUrls, ...blogUrls]
}
