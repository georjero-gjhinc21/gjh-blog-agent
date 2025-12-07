import { notFound } from 'next/navigation'
import { format } from 'date-fns'
import { getAllPosts, getPostBySlug, markdownToHtml } from '@/lib/posts'
import type { Metadata } from 'next'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'

interface PostPageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  const posts = getAllPosts()
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  const post = getPostBySlug(params.slug)

  if (!post) {
    return {
      title: 'Post Not Found',
    }
  }

  return {
    title: `${post.title} - GJH Consulting`,
    description: post.description,
    keywords: post.keywords,
    alternates: {
      canonical: `/blog/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.description,
      type: 'article',
      publishedTime: post.date,
      authors: ['GJH Consulting'],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.description,
    },
  }
}

export default async function PostPage({ params }: PostPageProps) {
  const post = getPostBySlug(params.slug)

  if (!post) {
    notFound()
  }

  const contentHtml = await markdownToHtml(post.content)

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": post.title,
    "datePublished": post.date,
    "dateModified": post.date,
    "description": post.description,
    "author": {
      "@type": "Organization",
      "name": "GJH Consulting"
    },
    "publisher": {
      "@type": "Organization",
      "name": "GJH Consulting",
      "logo": {
        "@type": "ImageObject",
        "url": "https://gjhconsulting.net/logo.png"
      }
    }
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <article className="min-h-screen bg-background pt-24 pb-20 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute top-0 left-0 w-full h-[50vh] bg-gradient-to-b from-primary-900/10 to-transparent pointer-events-none" />
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto">
            {/* Breadcrumb */}
            <div className="mb-8 flex items-center gap-2 text-sm text-gray-400">
              <Link href="/" className="hover:text-primary-400 transition-colors">Home</Link>
              <span>/</span>
              <Link href="/blog" className="hover:text-primary-400 transition-colors">Blog</Link>
              <span>/</span>
              <span className="text-gray-500 truncate max-w-[200px]">{post.title}</span>
            </div>

            {/* Article Header */}
            <header className="mb-12 text-center">
              <div className="mb-6 flex justify-center flex-wrap gap-2">
                {post.keywords && post.keywords.length > 0 && (
                  post.keywords.slice(0, 3).map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-block bg-primary-500/10 border border-primary-500/20 text-primary-300 text-sm px-3 py-1 rounded-full backdrop-blur-sm"
                    >
                      {keyword}
                    </span>
                  ))
                )}
              </div>
              
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-white leading-tight font-heading">
                {post.title}
              </h1>
              
              <div className="flex items-center justify-center gap-6 text-gray-400 text-sm md:text-base border-y border-white/5 py-6">
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <time dateTime={post.date}>
                    {format(new Date(post.date), 'MMMM d, yyyy')}
                  </time>
                </div>
                <div className="w-1 h-1 rounded-full bg-gray-600" />
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{post.readingTime} min read</span>
                </div>
              </div>
            </header>

            {/* Article Content */}
            <div className="glass-panel rounded-3xl p-8 md:p-12 mb-12">
              <div
                className="prose-custom mx-auto"
                dangerouslySetInnerHTML={{ __html: contentHtml }}
              />
            </div>

            {/* Article Footer / CTA */}
            <footer className="border-t border-white/10 pt-12">
              <div className="bg-gradient-to-br from-surface-highlight to-surface border border-white/5 rounded-2xl p-8 md:p-12 text-center relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary-600/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
                
                <h3 className="text-2xl md:text-3xl font-bold mb-4 text-white relative z-10">Need Expert Guidance?</h3>
                <p className="text-gray-300 mb-8 max-w-2xl mx-auto relative z-10 text-lg">
                  Our team specializes in helping companies navigate government contracting successfully. Let's discuss your strategy.
                </p>
                <div className="relative z-10">
                  <Link href="/contact" className="btn-primary inline-flex items-center">
                    Schedule a Consultation
                    <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
              </div>
              
              <div className="mt-12 flex justify-between items-center">
                <Link href="/blog" className="text-gray-400 hover:text-white flex items-center transition-colors">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Articles
                </Link>
              </div>
            </footer>
          </div>
        </div>
      </article>
    </>
  )
}
