import Link from 'next/link'
import { format } from 'date-fns'
import type { PostSummary } from '@/lib/posts'

interface BlogCardProps {
  post: PostSummary
}

export default function BlogCard({ post }: BlogCardProps) {
  return (
    <article className="card-modern group h-full flex flex-col relative">
      <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-purple/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <div className="p-8 flex-grow relative z-10">
        <div className="flex items-center gap-3 text-xs font-medium text-primary-400 mb-4">
          <time dateTime={post.date} className="bg-primary-900/30 px-2 py-1 rounded border border-primary-500/20">
            {format(new Date(post.date), 'MMM d, yyyy')}
          </time>
          <span className="w-1 h-1 rounded-full bg-gray-500" />
          <span className="text-gray-400">{post.readingTime} min read</span>
        </div>
        
        <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-primary-400 transition-colors line-clamp-2 font-heading leading-tight">
          <Link href={`/blog/${post.slug}`} className="before:absolute before:inset-0">
            {post.title}
          </Link>
        </h3>
        
        <p className="text-gray-400 mb-6 line-clamp-3 leading-relaxed">
          {post.excerpt}
        </p>
        
        {post.keywords && post.keywords.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4 relative z-20">
            {post.keywords.slice(0, 3).map((keyword, index) => (
              <span
                key={index}
                className="inline-block bg-surface border border-white/5 text-gray-300 text-xs px-2.5 py-1 rounded-full transition-colors hover:border-primary-500/50 hover:text-primary-300"
              >
                {keyword}
              </span>
            ))}
          </div>
        )}
      </div>
      
      <div className="px-8 pb-8 relative z-10 mt-auto">
        <div className="flex items-center text-primary-400 font-semibold text-sm group-hover:translate-x-2 transition-transform duration-300">
          Read Article
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </article>
  )
}
