import Link from 'next/link'
import { getAllPosts, getFeaturedPosts } from '@/lib/posts'
import BlogCard from '@/components/BlogCard'
import { format } from 'date-fns'

export default function Home() {
  const featuredPosts = getFeaturedPosts(3)
  const allPosts = getAllPosts()

  return (
    <>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Government Contracting Insights
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Expert guidance on federal procurement, GSA schedules, and technology consulting
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/blog" className="btn-primary bg-white text-primary-600 hover:bg-gray-100">
                Browse Articles
              </Link>
              <Link href="/#featured" className="btn-secondary border-white text-white hover:bg-primary-700">
                Featured Posts
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      {featuredPosts.length > 0 && (
        <section id="featured" className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <h2 className="text-4xl font-bold mb-10 text-center">Featured Articles</h2>
              <div className="grid md:grid-cols-3 gap-8">
                {featuredPosts.map((post) => (
                  <BlogCard key={post.slug} post={post} />
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* All Posts */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-10">
              <h2 className="text-4xl font-bold">Latest Articles</h2>
              <Link href="/blog" className="text-primary-600 hover:text-primary-700 font-semibold">
                View All →
              </Link>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {allPosts.slice(0, 6).map((post) => (
                <BlogCard key={post.slug} post={post} />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-600 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">Stay Updated</h2>
            <p className="text-xl mb-8 text-primary-100">
              Get the latest insights on government contracting delivered to your inbox
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="px-4 py-3 rounded-lg text-gray-900 flex-grow"
              />
              <button className="btn-primary bg-white text-primary-600 hover:bg-gray-100 whitespace-nowrap">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
