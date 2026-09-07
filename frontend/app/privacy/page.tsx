import type { Metadata } from 'next'
import StructuredData from '@/components/StructuredData'

export const metadata: Metadata = {
  title: 'Privacy Policy — GJH Consulting',
  description: 'Our commitment to your privacy.',
  alternates: {
    canonical: '/privacy',
  },
}

// Static Server Component
export default function PrivacyPage() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Privacy Policy — GJH Consulting",
    "description": "Detailed policy on data collection and usage by GJH Consulting.",
    "url": "https://gjhconsulting.net/privacy"
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-20 overflow-hidden">
      <StructuredData data={structuredData} />
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          <header className="text-center mb-16 animate-fade-in">
            <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Legal</span>
            <h1 className="text-5xl md:text-6xl font-bold mb-4 text-white">
              Privacy Policy
            </h1>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              This policy outlines how GJH Consulting collects, uses, and protects your personal information.
            </p>
          </header>

          <div className="space-y-12">
            {/* Collection Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Data Collection</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  We collect information that you voluntarily provide when you interact with our site, such as your name, email address, and professional details. This includes information submitted via contact or newsletter forms.
                </p>
                <p className="mt-4 text-sm text-gray-500">
                  We only collect data necessary for providing our services or responding to your inquiries.
                </p>
              </div>
            </section>

            {/* Use Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">How We Use Your Data</h2>
              <div className="space-y-6">
                <div className="card-modern p-6 bg-surface border border-white/10">
                  <h3 className="text-xl font-semibold text-primary-400">Service Provision</h3>
                  <p className="text-gray-300">
                    To deliver consulting services and manage client communications effectively.
                  </p>
                </div>
                <div className="card-modern p-6 bg-surface border border-white/10">
                  <h3 className="text-xl font-semibold text-primary-400">Marketing & Updates</h3>
                  <p className="text-gray-300">
                    If you subscribe to our newsletter, we use your email address to send relevant market insights and updates, respecting your opt-out preferences.
                  </p>
                </div>
              </div>
            </section>

            {/* Cookies Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Cookies Usage</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  We use necessary cookies to ensure the functionality of our website (e.g., session management, analytics). We do not use tracking cookies for profiling.
                </p>
              </div>
            </section>

            {/* Data Retention Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Data Retention Policy</h2>
              <div className="card-modern p-8 bg-surface-highlight border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  Personal data is retained only as long as necessary to fulfill the purpose for which it was collected, or as required by law. We automatically purge non-essential data after 24 months.
                </p>
              </div>
            </section>

            {/* Contact Section */}
            <section>
              <h2 className="text-3xl font-bold text-white mb-4">Contact Us</h2>
              <div className="card-modern p-8 bg-surface border border-white/10">
                <p className="text-gray-300 leading-relaxed">
                  For specific privacy concerns, please reach out directly to our compliance team: 
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