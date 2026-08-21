import { getCaseBySlug } from '@/lib/cases'
import { markdownToHtml } from '@/lib/cases'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'
import type { Metadata } from 'next'

interface CasePageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  const cases = await import('@/lib/cases')
  const allCases = cases.getAllCases()
  return allCases.map((caseStudy) => ({
    slug: caseStudy.slug,
  }))
}

export async function generateMetadata({ params }: CasePageProps): Promise<Metadata> {
  const caseStudy = await getCaseBySlug(params.slug)
  if (!caseStudy) {
    return {
      title: 'Case Study Not Found',
    }
  }
  return {
    title: `${caseStudy.title} - GJH Consulting`,
    description: caseStudy.excerpt,
    alternates: {
      canonical: `/cases/${params.slug}`,
    },
  }
}

export default async function CasePage({ params }: CasePageProps) {
  const caseStudy = await getCaseBySlug(params.slug)
  
  if (!caseStudy) {
    notFound()
  }

  const htmlContent = await markdownToHtml(caseStudy.content)

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": caseStudy.title,
    "description": caseStudy.excerpt,
    "author": {
      "@type": "Organization",
      "name": "GJH Consulting"
    },
    "datePublished": caseStudy.date,
    "url": `https://gjhconsulting.net/cases/${params.slug}`,
    "keywords": caseStudy.keywords,
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <div className="bg-background min-h-screen pt-24 pb-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {/* Back button */}
            <Link 
              href="/cases" 
              className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-colors mb-8"
            >
              <span>←</span>
              <span>Back to Case Studies</span>
            </Link>

            {/* Case Study Header */}
            <div className="mb-12">
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">
                Case Study
              </span>
              <h1 className="text-4xl md:text-5xl font-bold mb-6 text-white">
                {caseStudy.title}
              </h1>
              <p className="text-xl text-gray-400 mb-8">
                {caseStudy.excerpt}
              </p>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                <div className="glass-panel p-6 rounded-2xl">
                  <div className="text-sm text-gray-400 mb-1">Client</div>
                  <div className="text-white font-semibold">{caseStudy.client}</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl">
                  <div className="text-sm text-gray-400 mb-1">Challenge</div>
                  <div className="text-white font-semibold">{caseStudy.challenge}</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl">
                  <div className="text-sm text-gray-400 mb-1">Solution</div>
                  <div className="text-white font-semibold">{caseStudy.solution}</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl">
                  <div className="text-sm text-gray-400 mb-1">Results</div>
                  <div className="text-white font-semibold">{caseStudy.results}</div>
                </div>
              </div>
            </div>

            {/* Case Study Content */}
            <div 
              className="prose prose-invert prose-lg max-w-none"
              dangerouslySetInnerHTML={{ __html: htmlContent }}
            />

            {/* Conclusion CTA */}
            <div className="mt-16 p-8 glass-panel rounded-3xl text-center">
              <h3 className="text-2xl font-bold text-white mb-4">
                Ready to See Results Like These?
              </h3>
              <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
                Let's discuss how we can help you achieve your government contracting goals.
              </p>
              <Link 
                href="/contact" 
                className="btn-primary inline-block"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
