import type { Metadata } from 'next'
import StructuredData from '@/components/StructuredData'

export const metadata: Metadata = {
  title: 'Terms of Service — GJH Consulting',
  description: 'Our terms and conditions for using GJH Consulting services.',
  alternates: {
    canonical: '/terms',
  },
}

// Static Server Component
export default function TermsPage() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Terms of Service — GJH Consulting",
    "description": "Legal agreement outlining the use of GJH Consulting services.",
    "url": "https://gjhconsulting.net/terms"
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-20 overflow-hidden">
      <StructuredData data={structuredData} />
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          <header className="text-center mb-16 animate-fade-in">
            <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Legal Agreement</span>
            <h1 className="text-5xl md:text-6xl font-bold mb-4 text-white">
              Terms of Service
            </h1>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              By using our site and services, you agree to these terms. Please read carefully.
            </p>
          </header>

          <div className="space-y-12">
            {/* Services Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Scope of Services</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  GJH Consulting provides strategic guidance, data analysis, and consulting services related to government contracting. The scope of work is defined in separate contracts or proposals.
                </p>
              </div>
            </section>

            {/* Acceptable Use Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Acceptable Use Policy</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  Users must use our platform in a manner consistent with federal guidelines and ethical standards. Misuse, including spamming or unauthorized data scraping, is strictly prohibited.
                </p>
              </div>
            </section>

            {/* Intellectual Property Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Intellectual Property</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  All content, methodologies, and proprietary data presented by GJH Consulting remain the exclusive intellectual property of GJH Consulting unless explicitly transferred in writing.
                </p>
              </div>
            </section>

            {/* Limitation of Liability Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Limitation of Liability</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  In no event shall GJH Consulting be liable for any indirect, incidental, special, or consequential damages arising from the use or inability to use our services.
                </p>
              </div>
            </section>

            {/* Governing Law Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Governing Law</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  This agreement shall be governed by and construed in accordance with the laws of the jurisdiction where GJH Consulting is headquartered.
                </p>
              </div>
            </section>

            {/* Contact Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Questions?</h2>
              <div className="card-modern p-8 bg-surface border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  If you have questions regarding these terms, please contact us at: 
                  <a href="mailto:info@gjhconsulting.net" className="text-primary-400 hover:text-primary-300 ml-2">info@gjhconsulting.net</a>.
                </p>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}