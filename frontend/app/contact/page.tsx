import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Contact - GJH Consulting',
  description: 'Get in touch with GJH Consulting for expert government contracting guidance.',
}

export default function ContactPage() {
  return (
    <div className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold mb-4">Contact Us</h1>
            <p className="text-xl text-gray-600">
              Let's discuss how we can help you succeed in government contracting
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Contact Form */}
            <div className="card p-8">
              <h2 className="text-2xl font-bold mb-6">Send Us a Message</h2>
              <form className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-1">
                    Subject
                  </label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={5}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    required
                  ></textarea>
                </div>
                <button type="submit" className="btn-primary w-full">
                  Send Message
                </button>
              </form>
            </div>

            {/* Contact Info */}
            <div className="space-y-6">
              <div className="card p-6">
                <h3 className="font-bold text-lg mb-2">Email</h3>
                <a href="mailto:info@gjhconsulting.net" className="text-primary-600 hover:text-primary-700">
                  info@gjhconsulting.net
                </a>
              </div>

              <div className="card p-6">
                <h3 className="font-bold text-lg mb-2">Services</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• Government Contracting Consulting</li>
                  <li>• GSA Schedule Management</li>
                  <li>• SBIR/STTR Grant Support</li>
                  <li>• Cybersecurity Compliance</li>
                  <li>• Technology Solutions</li>
                </ul>
              </div>

              <div className="card p-6 bg-primary-50">
                <h3 className="font-bold text-lg mb-2">Stay Connected</h3>
                <p className="text-gray-700 mb-4">
                  Follow us for the latest insights and updates
                </p>
                <div className="flex gap-4">
                  <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:text-primary-700">
                    LinkedIn
                  </a>
                  <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:text-primary-700">
                    Twitter
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
