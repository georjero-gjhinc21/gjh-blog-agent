import { getPartnerBySlug, getAllPartners } from '@/lib/partners'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'
import type { Metadata } from 'next'

export async function generateStaticParams() {
  const allPartners = getAllPartners()
  return allPartners.map((partner) => ({
    slug: partner.slug,
  }))
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params
  if (!slug) return { title: 'Not Found' }
  const partner = await getPartnerBySlug(slug)
  if (!partner) {
    return { title: 'Partner Not Found' }
  }
  return {
    title: `${partner.name} - Partner Program`,
    description: partner.excerpt,
    alternates: { canonical: `/partners/${slug}` },
  }
}

export default async function PartnerPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const partner = await getPartnerBySlug(slug)
  if (!partner) {
    notFound()
  }

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": partner.name,
    "description": partner.description,
    "brand": { "@type": "Brand", "name": partner.name },
    "category": partner.category,
  }

  return (
    <>
      <StructuredData data={structuredData} />
      <article className="min-h-screen bg-background pt-24 pb-20 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[50vh] bg-gradient-to-b from-primary-900/10 to-transparent pointer-events-none" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto">
            {/* Breadcrumb */}
            <div className="mb-8 flex items-center gap-2 text-sm text-gray-400">
              <Link href="/" className="hover:text-primary-400 transition-colors">Home</Link>
              <span>/</span>
              <Link href="/partners" className="hover:text-primary-400 transition-colors">Partners</Link>
              <span>/</span>
              <span className="text-gray-500 truncate max-w-[200px]">{partner.name}</span>
            </div>

            {/* Header */}
            <header className="mb-12 text-center">
              <div className="mb-6 flex justify-center flex-wrap gap-2">
                <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                  partner.platform === 'PartnerStack'
                    ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                }`}>
                  {partner.platform}
                </span>
                <span className="text-xs font-semibold px-3 py-1 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
                  {partner.category}
                </span>
              </div>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-white leading-tight">
                {partner.name}
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                {partner.excerpt}
              </p>
            </header>

            {/* Content */}
            <div className="glass-panel rounded-3xl p-8 md:p-12 mb-12">
              <h2 className="text-2xl font-bold mb-4 text-white">Overview</h2>
              <p className="text-gray-300 leading-relaxed text-lg mb-8">
                {partner.description}
              </p>

              <h2 className="text-2xl font-bold mb-4 text-white">Key Details</h2>
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="bg-surface-highlight/50 border border-white/5 rounded-2xl p-6">
                  <span className="text-gray-400 text-sm">Platform</span>
                  <p className="text-white font-semibold mt-1">{partner.platform}</p>
                </div>
                <div className="bg-surface-highlight/50 border border-white/5 rounded-2xl p-6">
                  <span className="text-gray-400 text-sm">Category</span>
                  <p className="text-white font-semibold mt-1">{partner.category}</p>
                </div>
              </div>

              <h2 className="text-2xl font-bold mb-4 text-white">Related Keywords</h2>
              <div className="flex flex-wrap gap-2 mb-8">
                {partner.keywords.map((k, i) => (
                  <span key={i} className="inline-block bg-primary-500/10 border border-primary-500/20 text-primary-300 text-sm px-3 py-1 rounded-full">
                    {k}
                  </span>
                ))}
              </div>

              <div className="text-center">
                <a
                  href={partner.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary inline-flex items-center"
                >
                  {partner.cta}
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            </div>

            {/* Footer */}
            <footer className="border-t border-white/10 pt-12">
              <Link href="/partners" className="text-gray-400 hover:text-white flex items-center transition-colors">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Partner Programs
              </Link>
            </footer>
          </div>
        </div>
      </article>
    </>
  )
}
PARTNERPAGE
echo "Partner detail page created"