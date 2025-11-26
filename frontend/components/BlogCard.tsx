import Link from 'next/link'
import { format } from 'date-fns'
import type { Post } from '@/lib/posts'

interface BlogCardProps {
  post: Post
}

export default function BlogCard({ post }: BlogCardProps) {
  return (
    <article className="card overflow-hidden h-full flex flex-col">
      <div className="p-6 flex-grow">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
          <time dateTime={post.date}>
            {format(new Date(post.date), 'MMM d, yyyy')}
          </time>
          <span>•</span>
          <span>{post.readingTime} min read</span>
        </div>
        <h3 className="text-xl font-bold mb-3 text-gray-900 line-clamp-2">
          <Link href={`/blog/${post.slug}`} className="hover:text-primary-600 transition-colors">
            {post.title}
          </Link>
        </h3>
        <p className="text-gray-600 mb-4 line-clamp-3">
          {post.excerpt}
        </p>
        {post.keywords && post.keywords.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {post.keywords.slice(0, 3).map((keyword, index) => (
              <span
                key={index}
                className="inline-block bg-primary-50 text-primary-700 text-xs px-2 py-1 rounded-full"
              >
                {keyword}
              </span>
            ))}
          </div>
        )}
      </div>
      <div className="px-6 pb-6">
        <Link
          href={`/blog/${post.slug}`}
          className="inline-flex items-center text-primary-600 hover:text-primary-700 font-semibold"
        >
          Read More
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </article>
  )
}
