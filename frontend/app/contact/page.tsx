import type { Metadata } from 'next'
import StructuredData from '@/components/StructuredData'
import ContactForm from './ContactForm'

export const metadata: Metadata = {
  title: 'Contact - GJH Consulting',
  description: 'Get in touch with GJH Consulting for expert government contracting guidance.',
  alternates: {
    canonical: '/contact',
  },
}

export default function ContactPage() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    "name": "Contact GJH Consulting",
    "description": "Get in touch with GJH Consulting for expert government contracting guidance.",
    "url": "https://gjhconsulting.net/contact"
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <div className="min-h-screen bg-background pt-24 pb-20 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary-600/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-accent-purple/10 rounded-full blur-[100px] pointer-events-none" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 animate-fade-in">
              <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block">Get in Touch</span>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
                Let's Build Your <span className="text-gradient">Federal Strategy</span>
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Ready to win more government contracts? Our team of experts is here to guide you through every step of the process.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
              {/* Contact Form */}
              <div className="glass-panel rounded-3xl p-8 md:p-10 animate-slide-up">
                <h2 className="text-2xl font-bold mb-8 text-white">Send Us a Message</h2>
                <ContactForm />
              </div>

              {/* Contact Info */}
              <div className="space-y-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <div className="card-modern p-8 bg-gradient-to-br from-surface to-surface-highlight">
                  <div className="w-12 h-12 bg-primary-500/10 rounded-xl flex items-center justify-center mb-6 text-primary-400">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-white">Email Us</h3>
                  <p className="text-gray-400 mb-4">Direct line to our contracting experts.</p>
                  <a href="mailto:info@gjhconsulting.net" className="text-primary-400 hover:text-primary-300 font-medium text-lg transition-colors">
                    info@gjhconsulting.net
                  </a>
                </div>

                <div className="card-modern p-8">
                  <h3 className="text-xl font-bold mb-6 text-white">Our Services</h3>
                  <ul className="space-y-4">
                    {[
                      'Government Contracting Consulting',
                      'GSA Schedule Management',
                      'SBIR/STTR Grant Support',
                      'Cybersecurity Compliance',
                      'Technology Solutions'
                    ].map((item, index) => (
                      <li key={index} className="flex items-start text-gray-300">
                        <svg className="w-5 h-5 text-accent-cyan mr-3 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="p-8 rounded-3xl bg-primary-600/10 border border-primary-500/20 backdrop-blur-sm">
                  <h3 className="text-xl font-bold mb-3 text-white">Ready to Start?</h3>
                  <p className="text-gray-300 mb-0">
                    Most inquiries receive a response within 24 hours. We look forward to partnering with you.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
