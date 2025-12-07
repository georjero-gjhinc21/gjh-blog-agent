import { getAllPosts } from '@/lib/posts'
import BlogCard from '@/components/BlogCard'
import Search from '@/components/Search'
import type { Metadata } from 'next'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'

export const metadata: Metadata = {
  title: 'Insights - GJH Consulting',
  description: 'Expert insights on government contracting, federal procurement, GSA schedules, and more.',
  alternates: {
    canonical: '/blog',
  },
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

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "GJH Consulting Blog",
    "description": "Expert insights on government contracting and federal procurement.",
    "url": "https://gjhconsulting.net/blog",
    "numberOfItems": totalPosts,
    "itemListElement": paginatedPosts.map((post, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "url": `https://gjhconsulting.net/blog/${post.slug}`,
      "name": post.title
    }))
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <div className="bg-background min-h-screen pt-24 pb-20 relative overflow-hidden">
        {/* Decorative Background */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-accent-purple/10 rounded-full blur-[100px] pointer-events-none" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Knowledge Hub</span>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
                Government Contracting <span className="text-gradient">Insights</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Stay informed with the latest trends, strategies, and regulatory updates in the federal marketplace.
              </p>
            </div>

            <div className="mb-12">
              <Search />
            </div>

            {(topic || query) && (
               <div className="mb-10 flex flex-wrap items-center justify-center gap-4 animate-fade-in">
                 <h2 className="text-2xl font-semibold text-white">
                   Showing results
                   {query && <span> for "<span className="text-primary-400">{query}</span>"</span>}
                   {topic && <span> in <span className="text-primary-400">{topic.replace(/-/g, ' ')}</span></span>}
                 </h2>
                 <Link href="/blog" className="text-sm px-4 py-2 rounded-full bg-surface-highlight border border-white/10 text-gray-300 hover:text-white hover:border-primary-500/50 transition-colors">
                   Clear filters
                 </Link>
               </div>
             )}

            {paginatedPosts.length === 0 ? (
              <div className="text-center py-20 glass-panel rounded-3xl">
                <div className="text-6xl mb-6">🔍</div>
                <p className="text-2xl text-gray-300 font-semibold mb-2">
                  No articles found
                </p>
                <p className="text-gray-500 mb-8">
                  We couldn't find any posts matching your criteria.
                </p>
                <Link href="/blog" className="btn-primary">
                  View all posts
                </Link>
              </div>
            ) : (
              <>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
                  {paginatedPosts.map((post) => (
                    <BlogCard key={post.slug} post={post} />
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="flex justify-center gap-3">
                    {currentPage > 1 && (
                      <Link
                        href={{
                          pathname: '/blog',
                          query: { ...searchParams, page: currentPage - 1 }
                        }}
                        className="w-10 h-10 flex items-center justify-center rounded-full bg-surface-highlight border border-white/10 text-gray-300 hover:bg-primary-600 hover:text-white transition-all"
                      >
                        ←
                      </Link>
                    )}
                    
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                      <Link
                        key={page}
                        href={{
                          pathname: '/blog',
                          query: { ...searchParams, page }
                        }}
                        className={`w-10 h-10 flex items-center justify-center rounded-full border transition-all ${
                          currentPage === page
                            ? 'bg-primary-600 text-white border-primary-500 shadow-[0_0_15px_rgba(14,165,233,0.3)]'
                            : 'bg-surface-highlight border-white/10 text-gray-300 hover:bg-surface hover:border-white/20'
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
                        className="w-10 h-10 flex items-center justify-center rounded-full bg-surface-highlight border border-white/10 text-gray-300 hover:bg-primary-600 hover:text-white transition-all"
                      >
                        →
                      </Link>
                    )}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
