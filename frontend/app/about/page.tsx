import type { Metadata } from 'next'
import Link from 'next/link'
import StructuredData from '@/components/StructuredData'

export const metadata: Metadata = {
  title: 'About - GJH Consulting',
  description: 'Learn about GJH Consulting and our expertise in government contracting.',
}

export default function AboutPage() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "AboutPage",
    "name": "About GJH Consulting",
    "description": "Learn about GJH Consulting and our expertise in government contracting.",
    "url": "https://gjhconsulting.net/about"
  }

  return (
    <>
      <StructuredData data={structuredData} />
      
      <div className="bg-background min-h-screen pt-24 pb-20 overflow-hidden">
        {/* Hero Section */}
        <section className="relative mb-24">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary-600/10 rounded-full blur-[128px] pointer-events-none" />
          
          <div className="container mx-auto px-4 relative z-10 text-center">
            <span className="text-primary-400 font-semibold tracking-wider text-sm uppercase mb-4 block animate-fade-in">Our Story</span>
            <h1 className="text-5xl md:text-7xl font-bold mb-8 animate-slide-up leading-tight text-white">
              Bridging Innovation & <br />
              <span className="text-gradient">Federal Opportunity</span>
            </h1>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              We are a team of government contracting veterans and technology experts dedicated to democratizing access to the federal marketplace.
            </p>
          </div>
        </section>

        <div className="container mx-auto px-4">
          {/* Mission & Vision Bento Grid */}
          <section className="grid md:grid-cols-2 gap-8 mb-24">
            <div className="card-modern p-10 bg-gradient-to-br from-surface to-surface-highlight flex flex-col justify-center min-h-[400px]">
              <div className="w-16 h-16 bg-primary-500/10 rounded-2xl flex items-center justify-center mb-8 text-primary-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold mb-4 text-white">Our Mission</h2>
              <p className="text-lg text-gray-300 leading-relaxed">
                To empower businesses of all sizes to successfully compete for and win government contracts by providing actionable insights, data-driven strategies, and expert guidance that demystifies the federal procurement process.
              </p>
            </div>

            <div className="grid gap-8">
              <div className="card-modern p-10 flex flex-col justify-center h-full relative overflow-hidden">
                 <div className="absolute top-0 right-0 w-32 h-32 bg-accent-purple/10 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none" />
                <h3 className="text-2xl font-bold mb-3 text-white">Strategic Expertise</h3>
                <p className="text-gray-400">
                  Decades of combined experience in GSA schedules, proposal management, and compliance.
                </p>
              </div>
              <div className="card-modern p-10 flex flex-col justify-center h-full relative overflow-hidden">
                <div className="absolute bottom-0 left-0 w-32 h-32 bg-accent-cyan/10 rounded-full blur-2xl -ml-10 -mb-10 pointer-events-none" />
                <h3 className="text-2xl font-bold mb-3 text-white">Technology First</h3>
                <p className="text-gray-400">
                  Leveraging AI and data analytics to identify opportunities before the competition.
                </p>
              </div>
            </div>
          </section>

          {/* Capabilities Section */}
          <section className="mb-24">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-6 text-white">Our Capabilities</h2>
              <p className="text-gray-400 max-w-2xl mx-auto">
                Comprehensive solutions tailored for the modern federal contractor.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  title: "GovCon Strategy",
                  desc: "Market entry planning and competitive analysis.",
                  icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                },
                {
                  title: "GSA Schedules",
                  desc: "Full lifecycle management from submission to renewal.",
                  icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                },
                {
                  title: "Cyber Compliance",
                  desc: "CMMC and NIST 800-171 readiness assessments.",
                  icon: "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                },
                {
                  title: "Grant Support",
                  desc: "Expert writing for SBIR/STTR funding opportunities.",
                  icon: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                },
                {
                  title: "Data Analytics",
                  desc: "Custom dashboards for pipeline management.",
                  icon: "M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
                },
                {
                  title: "Proposal Mgmt",
                  desc: "Winning proposal development and color team reviews.",
                  icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                }
              ].map((item, index) => (
                <div key={index} className="glass-panel p-8 rounded-2xl hover:bg-surface-highlight/50 transition-colors">
                  <div className="w-10 h-10 bg-primary-500/20 rounded-lg flex items-center justify-center mb-4 text-primary-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-white">{item.title}</h3>
                  <p className="text-gray-400 text-sm">{item.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* CTA Section */}
          <section className="relative rounded-3xl overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-900 to-primary-800" />
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-20" />
            
            <div className="relative z-10 p-12 md:p-20 text-center">
              <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white">Ready to Scale Your Government Business?</h2>
              <p className="text-xl text-primary-100 mb-10 max-w-2xl mx-auto">
                Join the leading companies that trust GJH Consulting for their federal market strategy.
              </p>
              <Link href="/contact" className="btn-secondary bg-white text-primary-900 hover:bg-gray-100 border-transparent">
                Get Started Today
              </Link>
            </div>
          </section>
        </div>
      </div>
    </>
  )
}
