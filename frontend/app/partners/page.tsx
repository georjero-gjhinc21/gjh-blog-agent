import { getAllPartners, getPartnersByPlatform, searchPartners } from '@/lib/partners'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Partner Programs - Trusted Tools & Platforms',
  description: 'Explore our curated partner programs featuring trusted tools for government contracting, project management, cybersecurity, and more.',
  alternates: {
    canonical: '/partners',
  },
}

function PartnerCard({ partner }: { partner: typeof import('@/lib/partners').partnerPrograms[number] }) {
  return (
    <div className="glass-panel rounded-2xl p-6 flex flex-col hover:border-primary-500/30 transition-all group">
      <div className="flex items-center justify-between mb-4">
        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
          partner.platform === 'PartnerStack'
            ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
            : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
        }`}>
          {partner.platform}
        </span>
        {partner.featured && (
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
            Featured
          </span>
        )}
      </div>
      
      <h3 className="text-xl font-bold mb-2 text-white group-hover:text-primary-400 transition-colors">
        {partner.name}
      </h3>
      
      <span className="text-sm text-gray-400 mb-3">{partner.category}</span>
      
      <p className="text-gray-300 text-sm leading-relaxed mb-6 flex-grow">
        {partner.excerpt}
      </p>
      
      <div className="flex flex-wrap gap-2 mb-6">
        {partner.keywords.slice(0, 3).map((k, i) => (
          <span key={i} className="text-xs px-2 py-1 rounded bg-white/5 text-gray-400">
            {k}
          </span>
        ))}
      </div>
      
      <Link
        href={`/partners/${partner.slug}`}
        className="inline-flex items-center text-primary-400 hover:text-primary-300 font-semibold text-sm transition-colors"
      >
        Learn more
        <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </Link>
    </div>
  )
}

export default async function PartnersPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; platform?: string; q?: string }>
}) {
  const params = await searchParams
  let partners = getAllPartners()
  
  if (params.platform) {
    partners = getPartnersByPlatform(params.platform)
  }
  if (params.category) {
    partners = getPartnersByPlatform(params.platform) || getAllPartners()
  }
  if (params.q) {
    partners = searchPartners(params.q)
  }

  const categories = Array.from(new Set(getAllPartners().map(p => p.category)))
  const platforms = ['PartnerStack', 'Impact', 'Impact.com']

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Partner Programs",
    "description": "Curated partner programs featuring trusted tools for government contracting.",
    "url": "https://gjhconsulting.net/partners",
    "numberOfItems": partners.length,
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <div className="bg-background min-h-screen pt-24 pb-20 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-accent-purple/10 rounded-full blur-[100px] pointer-events-none" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Partner Programs</span>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
                Trusted <span className="text-gradient">Tools & Platforms</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Explore curated partner programs featuring trusted tools for government contracting, cybersecurity, project management, and more.
              </p>
            </div>

            {/* Filters */}
            <div className="flex flex-wrap items-center justify-center gap-4 mb-12">
              <Link
                href="/partners"
                className={`px-4 py-2 rounded-full text-sm transition-all ${
                  !params.platform && !params.q
                    ? 'bg-primary-600 text-white'
                    : 'bg-surface-highlight border border-white/10 text-gray-300 hover:text-white'
                }`}
              >
                All
              </Link>
              {platforms.map(platform => (
                <Link
                  key={platform}
                  href={{ query: { platform } }}
                  className={`px-4 py-2 rounded-full text-sm transition-all ${
                    params.platform === platform
                      ? 'bg-primary-600 text-white'
                      : 'bg-surface-highlight border border-white/10 text-gray-300 hover:text-white'
                  }`}
                >
                  {platform}
                </Link>
              ))}
              {categories.map(cat => (
                <Link
                  key={cat}
                  href={{ query: { category: cat } }}
                  className={`px-4 py-2 rounded-full text-sm transition-all ${
                    params.category === cat
                      ? 'bg-primary-600 text-white'
                      : 'bg-surface-highlight border border-white/10 text-gray-300 hover:text-white'
                  }`}
                >
                  {cat}
                </Link>
              ))}
            </div>

            {partners.length === 0 ? (
              <div className="text-center py-20 glass-panel rounded-3xl">
                <div className="text-6xl mb-6">🔍</div>
                <p className="text-2xl text-gray-300 font-semibold mb-2">
                  No partner programs found
                </p>
                <p className="text-gray-500">
                  Try adjusting your search or filters.
                </p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {partners.map((partner) => (
                  <PartnerCard key={partner.slug} partner={partner} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
