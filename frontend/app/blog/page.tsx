import { getAllPosts } from '@/lib/posts'
import BlogCard from '@/components/BlogCard'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Blog - GJH Consulting',
  description: 'Expert insights on government contracting, federal procurement, GSA schedules, and more.',
}

export default function BlogPage() {
  const posts = getAllPosts()

  return (
    <div className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold mb-4">Blog</h1>
            <p className="text-xl text-gray-600">
              Insights and guidance on government contracting and federal procurement
            </p>
          </div>

          {posts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">
                No blog posts yet. Check back soon!
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {posts.map((post) => (
                <BlogCard key={post.slug} post={post} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
