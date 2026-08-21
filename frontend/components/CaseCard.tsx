import Link from 'next/link'

interface CaseStudy {
  slug: string
  title: string
  excerpt: string
  client: string
  challenge: string
  solution: string
  results: string
}

export default function CaseCard({ caseStudy }: { caseStudy: CaseStudy }) {
  return (
    <Link href={`/cases/${caseStudy.slug}`}>
      <div className="glass-panel p-8 rounded-3xl hover:border-primary-500/30 transition-all duration-300 group cursor-pointer h-full flex flex-col">
        <div className="mb-4">
          <span className="text-primary-400 font-semibold tracking-wider text-xs uppercase">Case Study</span>
        </div>
        <h3 className="text-xl font-bold text-white mb-3 group-hover:text-primary-300 transition-colors line-clamp-2">
          {caseStudy.title}
        </h3>
        <p className="text-gray-400 text-sm mb-6 flex-grow">{caseStudy.excerpt}</p>

        {/* Quick Stats */}
        <div className="space-y-3 mb-6">
          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider">Client</span>
            <p className="text-sm text-white font-medium">{caseStudy.client}</p>
          </div>
          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider">Challenge</span>
            <p className="text-sm text-white line-clamp-1">{caseStudy.challenge}</p>
          </div>
          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider">Results</span>
            <p className="text-sm text-primary-400 font-semibold">{caseStudy.results}</p>
          </div>
        </div>

        <div className="pt-4 border-t border-white/10">
          <span className="text-primary-400 text-sm font-medium flex items-center gap-2 group-hover:gap-3 transition-all">
            Read Case Study
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </span>
        </div>
      </div>
    </Link>
  )
}
