import { getAllPartners } from '@/lib/partners'
import { PARTNERS_PAGE_SIZE } from '@/lib/partner-taxonomy'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Partner Programs - Trusted Tools & Platforms',
  description: 'Software we use and recommend in client work: project tracking, data, security, and everyday operations.',
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
  searchParams: Promise<{ category?: string; platform?: string; q?: string; page?: string }>
}) {
  const params = await searchParams
  const allPartners = getAllPartners()

  // Intersecting filters (all three combine with AND).
  const q = (params.q ?? '').trim().toLowerCase()
  const partners = allPartners.filter((p) => {
    if (params.platform && p.platform !== params.platform) return false
    if (params.category && p.category !== params.category) return false
    if (q) {
      const hay = `${p.name} ${p.excerpt} ${p.description} ${p.category} ${p.keywords.join(' ')}`.toLowerCase()
      if (!hay.includes(q)) return false
    }
    return true
  })

  const categoryCounts = new Map<string, number>()
  for (const p of allPartners) {
    categoryCounts.set(p.category, (categoryCounts.get(p.category) ?? 0) + 1)
  }
  const categories = [...categoryCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  const platforms = Array.from(new Set(allPartners.map((p) => p.platform))).sort()

  const totalPages = Math.max(1, Math.ceil(partners.length / PARTNERS_PAGE_SIZE))
  const currentPage = Math.min(Math.max(1, Number(params.page) || 1), totalPages)
  const visiblePartners = partners.slice((currentPage - 1) * PARTNERS_PAGE_SIZE, currentPage * PARTNERS_PAGE_SIZE)

  const pageHref = (page: number) => ({
    pathname: '/partners',
    query: { ...(params.platform ? { platform: params.platform } : {}), ...(params.category ? { category: params.category } : {}), ...(params.q ? { q: params.q } : {}), ...(page > 1 ? { page: String(page) } : {}) },
  })

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Partner Programs",
    "description": "Software we use and recommend in client work.",
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
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Resources</span>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
                Trusted <span className="text-gradient">Tools & Platforms</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Software we use and recommend in client work — tracking, data, security, everyday operations. Some links earn us a commission; every page says so.
              </p>
            </div>

            {/* Filters */}
            <div className="flex flex-wrap items-center justify-center gap-4 mb-8">
              <Link
                href="/partners"
                className={`px-4 py-2 rounded-full text-sm transition-all ${
                  !params.platform && !params.q && !params.category
                    ? 'bg-primary-600 text-white'
                    : 'bg-surface-highlight border border-white/10 text-gray-300 hover:text-white'
                }`}
              >
                All ({allPartners.length})
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
              {categories.map(([cat, count]) => (
                <Link
                  key={cat}
                  href={{ query: { category: cat } }}
                  className={`px-4 py-2 rounded-full text-sm transition-all ${
                    params.category === cat
                      ? 'bg-primary-600 text-white'
                      : 'bg-surface-highlight border border-white/10 text-gray-300 hover:text-white'
                  }`}
                >
                  {cat} ({count})
                </Link>
              ))}
            </div>

            {/* Search (plain GET form — no JS needed, server filters) */}
            <form action="/partners" method="get" className="flex justify-center mb-4">
              {params.platform && <input type="hidden" name="platform" value={params.platform} />}
              {params.category && <input type="hidden" name="category" value={params.category} />}
              <input
                type="search"
                name="q"
                defaultValue={params.q ?? ''}
                placeholder="Search tools, e.g. payroll or SSO…"
                className="w-full max-w-md bg-surface-highlight border border-white/10 rounded-full px-5 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 transition-all"
              />
            </form>
            <p className="text-center text-sm text-gray-500 mb-12">
              Showing {visiblePartners.length} of {partners.length} programs{totalPages > 1 ? ` — page ${currentPage} of ${totalPages}` : ''}
            </p>

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
              <>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {visiblePartners.map((partner) => (
                    <PartnerCard key={partner.slug} partner={partner} />
                  ))}
                </div>
                {totalPages > 1 && (
                  <div className="flex items-center justify-center gap-4 mt-12">
                    {currentPage > 1 ? (
                      <Link href={pageHref(currentPage - 1)} className="px-5 py-2 rounded-full text-sm bg-surface-highlight border border-white/10 text-gray-300 hover:text-white transition-all">
                        ← Previous
                      </Link>
                    ) : (
                      <span className="px-5 py-2 rounded-full text-sm text-gray-600 border border-white/5">← Previous</span>
                    )}
                    <span className="text-sm text-gray-400">Page {currentPage} of {totalPages}</span>
                    {currentPage < totalPages ? (
                      <Link href={pageHref(currentPage + 1)} className="px-5 py-2 rounded-full text-sm bg-surface-highlight border border-white/10 text-gray-300 hover:text-white transition-all">
                        Next →
                      </Link>
                    ) : (
                      <span className="px-5 py-2 rounded-full text-sm text-gray-600 border border-white/5">Next →</span>
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
