import Link from 'next/link'
import { getFeaturedPosts } from '@/lib/posts'
import BlogCard from '@/components/BlogCard'
import StructuredData from '@/components/StructuredData'

export default function Home() {
  const featuredPosts = getFeaturedPosts(3)
  
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "GJH Consulting",
    "url": "https://gjhconsulting.net",
    "logo": "https://gjhconsulting.net/logo.png",
    "description": "Expert guidance on government contracting, federal procurement, GSA schedules, and technology consulting.",
    "sameAs": [
      "https://linkedin.com/company/gjh-consulting",
      "https://twitter.com/gjhconsulting"
    ]
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 bg-background">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-600/20 rounded-full blur-[128px] animate-pulse-glow" />
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent-purple/20 rounded-full blur-[128px] animate-pulse-glow" style={{ animationDelay: '1s' }} />
          <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
        </div>

        <div className="container mx-auto px-4 relative z-10 text-center">
          <div className="inline-block mb-6 animate-fade-in">
            <span className="bg-surface-highlight border border-primary-500/30 text-primary-300 text-sm font-semibold px-4 py-1.5 rounded-full backdrop-blur-md">
              Next-Gen Government Contracting
            </span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-8 animate-slide-up leading-tight">
            Navigate the Future of <br />
            <span className="text-gradient">Federal Procurement</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-400 mb-10 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Unlock opportunities with AI-driven insights, expert GSA schedule guidance, and cutting-edge compliance strategies.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <Link href="/blog" className="btn-primary group">
              Explore Insights
              <svg className="w-5 h-5 ml-2 inline-block transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link href="/contact" className="btn-secondary">
              Partner With Us
            </Link>
          </div>
        </div>
        
        {/* Scroll Indicator */}
        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce text-gray-500">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </section>

      {/* Stats/Features Section (Bento Grid Style) */}
      <section className="py-24 bg-surface relative overflow-hidden">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose GJH Consulting</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">We combine deep industry expertise with modern technology to deliver results.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card-modern p-8 md:col-span-2">
              <div className="w-12 h-12 bg-primary-500/10 rounded-xl flex items-center justify-center mb-6 text-primary-400">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-4">GSA Schedule Experts</h3>
              <p className="text-gray-400 text-lg">
                Streamline your path to a GSA Schedule. We handle the complexity so you can focus on delivery. 
                Our success rate for schedule awards is industry-leading.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card-modern p-8 bg-gradient-to-br from-surface to-surface-highlight">
              <div className="w-12 h-12 bg-accent-purple/10 rounded-xl flex items-center justify-center mb-6 text-accent-purple">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-4">AI-Powered Compliance</h3>
              <p className="text-gray-400">
                Stay ahead of regulations with our automated compliance monitoring tools.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card-modern p-8">
              <div className="w-12 h-12 bg-accent-cyan/10 rounded-xl flex items-center justify-center mb-6 text-accent-cyan">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-4">Market Intelligence</h3>
              <p className="text-gray-400">
                Data-driven identification of opportunities tailored to your capabilities.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="card-modern p-8 md:col-span-2 relative overflow-hidden">
               <div className="absolute right-0 top-0 w-64 h-64 bg-primary-600/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
              <div className="w-12 h-12 bg-accent-pink/10 rounded-xl flex items-center justify-center mb-6 text-accent-pink">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-4">Strategic Consulting</h3>
              <p className="text-gray-400 text-lg">
                From capture management to proposal writing, our team of veterans guides you through every step of the federal sales cycle.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      {featuredPosts.length > 0 && (
        <section id="featured" className="py-24 bg-background relative">
           <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary-500/20 to-transparent" />
           
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row justify-between items-end mb-12">
              <div className="max-w-2xl">
                <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-2 block">Latest Insights</span>
                <h2 className="text-3xl md:text-4xl font-bold">Stay Ahead of the Curve</h2>
              </div>
              <Link href="/blog" className="hidden md:inline-flex items-center text-primary-400 hover:text-primary-300 font-semibold transition-colors mt-4 md:mt-0">
                View All Articles
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8">
              {featuredPosts.map((post) => (
                <BlogCard key={post.slug} post={post} />
              ))}
            </div>

            <div className="mt-8 text-center md:hidden">
              <Link href="/blog" className="btn-secondary w-full">
                View All Articles
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-primary-900/20" />
        <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-30" />
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center p-12 glass-panel rounded-3xl">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">Ready to Win More Contracts?</h2>
            <p className="text-xl mb-10 text-gray-300">
              Join hundreds of successful contractors who trust GJH Consulting for their federal market strategy.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-lg mx-auto">
              <input
                type="email"
                placeholder="Enter your email address"
                className="px-6 py-4 rounded-full bg-surface-highlight border border-white/10 text-white placeholder-gray-500 flex-grow focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all"
              />
              <button className="btn-primary whitespace-nowrap">
                Get Started
              </button>
            </div>
            <p className="mt-4 text-sm text-gray-500">
              No spam. Unsubscribe anytime.
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
