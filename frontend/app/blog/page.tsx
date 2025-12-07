import { getAllPosts } from '@/lib/posts'
import BlogCard from '@/components/BlogCard'
import Search from '@/components/Search'
import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Blog - GJH Consulting',
  description: 'Expert insights on government contracting, federal procurement, GSA schedules, and more.',
}

interface BlogPageProps {
  searchParams: {
    topic?: string;
    page?: string;
    query?: string;
  }
}

export default function BlogPage({ searchParams }: BlogPageProps) {
  const allPosts = getAllPosts()
  const topic = searchParams.topic
  const query = searchParams.query
  const currentPage = Number(searchParams.page) || 1
  const postsPerPage = 9

  // Filter posts
  let filteredPosts = allPosts
  
  if (query) {
    const lowerQuery = query.toLowerCase()
    filteredPosts = filteredPosts.filter(post => 
      post.title.toLowerCase().includes(lowerQuery) ||
      post.description.toLowerCase().includes(lowerQuery) ||
      post.keywords?.some(k => k.toLowerCase().includes(lowerQuery))
    )
  }

  if (topic) {
    filteredPosts = filteredPosts.filter(post => 
      post.keywords?.some(k => k.toLowerCase().replace(/ /g, '-') === topic)
    )
  }

  // Pagination
  const totalPosts = filteredPosts.length
  const totalPages = Math.ceil(totalPosts / postsPerPage)
  const startIndex = (currentPage - 1) * postsPerPage
  const paginatedPosts = filteredPosts.slice(startIndex, startIndex + postsPerPage)

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

          <Search />

          {(topic || query) && (
             <div className="mb-8 flex flex-wrap items-center gap-4">
               <h2 className="text-2xl font-semibold">
                 Showing results
                 {query && <span> for "<span className="text-primary-600">{query}</span>"</span>}
                 {topic && <span> in <span className="text-primary-600">{topic.replace(/-/g, ' ')}</span></span>}
               </h2>
               <Link href="/blog" className="text-sm text-gray-500 hover:text-primary-600 hover:underline">
                 Clear filters
               </Link>
             </div>
           )}

          {paginatedPosts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">
                No blog posts found matching your criteria.
              </p>
              {(topic || query) && (
                <Link href="/blog" className="mt-4 inline-block text-primary-600 hover:underline">
                  View all posts
                </Link>
              )}
            </div>
          ) : (
            <>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {paginatedPosts.map((post) => (
                  <BlogCard key={post.slug} post={post} />
                ))}
              </div>

              {totalPages > 1 && (
                <div className="mt-12 flex justify-center gap-2">
                  {currentPage > 1 && (
                    <Link
                      href={{
                        pathname: '/blog',
                        query: { ...searchParams, page: currentPage - 1 }
                      }}
                      className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                    >
                      Previous
                    </Link>
                  )}
                  
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <Link
                      key={page}
                      href={{
                        pathname: '/blog',
                        query: { ...searchParams, page }
                      }}
                      className={`px-4 py-2 border rounded-md ${
                        currentPage === page
                          ? 'bg-primary-600 text-white border-primary-600'
                          : 'border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {page}
                    </Link>
                  ))}

                  {currentPage < totalPages && (
                    <Link
                      href={{
                        pathname: '/blog',
                        query: { ...searchParams, page: currentPage + 1 }
                      }}
                      className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                    >
                      Next
                    </Link>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
