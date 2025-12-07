import Link from 'next/link'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-surface border-t border-white/5 pt-20 pb-10">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-1 md:col-span-1">
            <Link href="/" className="text-2xl font-bold font-heading text-gradient mb-6 block">
              GJH Consulting
            </Link>
            <p className="text-gray-400 leading-relaxed mb-6">
              Empowering businesses to navigate the complexities of government contracting with next-generation insights and AI-driven strategies.
            </p>
            <div className="flex space-x-4">
              {/* Social Icons Placeholder */}
              {['Twitter', 'LinkedIn', 'GitHub'].map((social) => (
                <a key={social} href="#" className="w-10 h-10 rounded-full bg-surface-highlight flex items-center justify-center text-gray-400 hover:text-white hover:bg-primary-600 transition-all duration-300">
                  <span className="sr-only">{social}</span>
                  <div className="w-5 h-5 bg-current opacity-50" />
                </a>
              ))}
            </div>
          </div>
          
          <div>
            <h4 className="text-white font-bold mb-6">Explore</h4>
            <ul className="space-y-4">
              {['Home', 'About Us', 'Services', 'Case Studies', 'Contact'].map((item) => (
                <li key={item}>
                  <Link href={`/${item.toLowerCase().replace(' ', '-')}`} className="text-gray-400 hover:text-primary-400 transition-colors">
                    {item}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6">Topics</h4>
            <ul className="space-y-4">
              {[
                { name: 'Gov Contracting', slug: 'government-contracting' },
                { name: 'GSA Schedules', slug: 'gsa-schedules' },
                { name: 'Cybersecurity', slug: 'cybersecurity' },
                { name: 'AI Solutions', slug: 'ai-solutions' },
              ].map((item) => (
                <li key={item.slug}>
                  <Link href={`/blog?topic=${item.slug}`} className="text-gray-400 hover:text-primary-400 transition-colors">
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6">Newsletter</h4>
            <p className="text-gray-400 mb-4">Subscribe to our newsletter for the latest federal market insights.</p>
            <form className="space-y-4">
              <input 
                type="email" 
                placeholder="Enter your email" 
                className="w-full bg-background border border-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-all"
              />
              <button className="w-full btn-primary">
                Subscribe
              </button>
            </form>
          </div>
        </div>

        <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
          <p>&copy; {currentYear} GJH Consulting. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
