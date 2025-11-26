import Link from 'next/link'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-white text-xl font-bold mb-4">GJH Consulting</h3>
            <p className="text-sm">
              Expert guidance in government contracting, federal procurement, and technology consulting.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Topics</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/blog?topic=government-contracting" className="hover:text-white">Government Contracting</Link></li>
              <li><Link href="/blog?topic=gsa-schedules" className="hover:text-white">GSA Schedules</Link></li>
              <li><Link href="/blog?topic=sbir-sttr" className="hover:text-white">SBIR/STTR</Link></li>
              <li><Link href="/blog?topic=cybersecurity" className="hover:text-white">Cybersecurity</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="hover:text-white">About Us</Link></li>
              <li><Link href="/services" className="hover:text-white">Services</Link></li>
              <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
              <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Connect</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="hover:text-white">LinkedIn</a></li>
              <li><a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-white">Twitter</a></li>
              <li><a href="mailto:info@gjhconsulting.net" className="hover:text-white">Email</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
          <p>&copy; {currentYear} GJH Consulting. All rights reserved.</p>
          <p className="mt-2 text-gray-500">Powered by AI-driven content generation</p>
        </div>
      </div>
    </footer>
  )
}
