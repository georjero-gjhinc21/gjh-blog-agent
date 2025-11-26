import { notFound } from 'next/navigation'
import { format } from 'date-fns'
import { getAllPosts, getPostBySlug, markdownToHtml } from '@/lib/posts'
import type { Metadata } from 'next'

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
    openGraph: {
      title: post.title,
      description: post.description,
      type: 'article',
      publishedTime: post.date,
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

  return (
    <article className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Article Header */}
          <header className="mb-8">
            <div className="mb-6">
              {post.keywords && post.keywords.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {post.keywords.slice(0, 5).map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-block bg-primary-50 text-primary-700 text-sm px-3 py-1 rounded-full"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
              {post.title}
            </h1>
            <div className="flex items-center gap-4 text-gray-600">
              <time dateTime={post.date}>
                {format(new Date(post.date), 'MMMM d, yyyy')}
              </time>
              <span>•</span>
              <span>{post.readingTime} min read</span>
            </div>
          </header>

          {/* Article Content */}
          <div
            className="prose-custom"
            dangerouslySetInnerHTML={{ __html: contentHtml }}
          />

          {/* Article Footer */}
          <footer className="mt-12 pt-8 border-t border-gray-200">
            <div className="bg-primary-50 rounded-lg p-6">
              <h3 className="text-xl font-bold mb-2">Need Expert Guidance?</h3>
              <p className="text-gray-700 mb-4">
                Our team specializes in helping companies navigate government contracting successfully.
              </p>
              <a
                href="/contact"
                className="inline-block bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                Contact Us Today
              </a>
            </div>
          </footer>

          {/* Share Section */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <p className="text-gray-600 text-sm">
              Found this article helpful? Share it with your network!
            </p>
          </div>
        </div>
      </div>
    </article>
  )
}
