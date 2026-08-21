import { getAllCases } from '@/lib/cases'
import CaseCard from '@/components/CaseCard'
import StructuredData from '@/components/StructuredData'
import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Case Studies - GJH Consulting',
  description: 'Real results from government contracting projects. See how we help agencies and contractors succeed.',
  alternates: {
    canonical: '/cases',
  },
}

export default function CasesPage() {
  const allCases = getAllCases()

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "GJH Consulting Case Studies",
    "description": "Real results from government contracting projects.",
    "url": "https://gjhconsulting.net/cases",
    "numberOfItems": allCases.length,
    "itemListElement": allCases.map((caseStudy, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "url": `https://gjhconsulting.net/cases/${caseStudy.slug}`,
      "name": caseStudy.title
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
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Proven Results</span>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
                Our <span className="text-gradient">Case Studies</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                See how we've helped government agencies and contractors achieve measurable success.
              </p>
            </div>

            {allCases.length === 0 ? (
              <div className="text-center py-20 glass-panel rounded-3xl">
                <div className="text-6xl mb-6">📊</div>
                <p className="text-2xl text-gray-300 font-semibold mb-2">
                  No case studies yet
                </p>
                <p className="text-gray-500">
                  We're working on showcasing our best projects.
                </p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {allCases.map((caseStudy) => (
                  <CaseCard key={caseStudy.slug} caseStudy={caseStudy} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
