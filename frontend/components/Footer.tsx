'use client'

import { useState } from 'react'
import Link from 'next/link'

const exploreLinks = [
  { name: 'Home', href: '/' },
  { name: 'Insights', href: '/blog' },
  { name: 'Case Studies', href: '/cases' },
  { name: 'Partners', href: '/partners' },
  { name: 'About', href: '/about' },
  { name: 'Contact', href: '/contact' },
]

const socialLinks = [
  { name: 'Twitter', href: 'https://twitter.com/GJHConsulting' },
  { name: 'LinkedIn', href: 'https://www.linkedin.com/company/gjh-consulting' },
  { name: 'GitHub', href: 'https://github.com/georjero-gjhinc21' },
]

const topicLinks = [
  { name: 'AI Strategy', slug: 'ai-strategy' },
  { name: 'Data Foundations', slug: 'data-foundations' },
  { name: 'AI in Production', slug: 'ai-in-production' },
  { name: 'Working With Us', slug: 'working-with-us' },
]

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

type NewsletterStatus = 'idle' | 'sending' | 'success' | 'error'

export default function Footer() {
  const currentYear = new Date().getFullYear()
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<NewsletterStatus>('idle')
  const [message, setMessage] = useState('')

  async function handleSubscribe(e: React.FormEvent) {
    e.preventDefault()
    if (!EMAIL_RE.test(email.trim())) {
      setStatus('error')
      setMessage('Please enter a valid email address.')
      return
    }
    setStatus('sending')
    setMessage('')
    try {
      const res = await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim() }),
      })
      const data = await res.json().catch(() => ({}))
      if (res.ok) {
        setStatus('success')
        setMessage("You're subscribed.")
        setEmail('')
      } else {
        setStatus('error')
        setMessage(typeof data.error === 'string' ? data.error : 'Subscription failed. Please try again.')
      }
    } catch {
      setStatus('error')
      setMessage('Subscription failed. Please try again.')
    }
  }

  return (
    <footer className="bg-surface border-t border-white/5 pt-20 pb-10">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-1 md:col-span-1">
            <Link href="/" className="text-2xl font-bold font-heading text-gradient mb-6 block">
              GJH Consulting
            </Link>
            <p className="text-gray-400 leading-relaxed mb-6">
              An AI-first partner helping teams put AI to work \u2014 honest advice, systems that hold up, data in good order.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => (
                <a key={social.name} href={social.href} target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-surface-highlight flex items-center justify-center text-gray-400 hover:text-white hover:bg-primary-600 transition-all duration-300">
                  <span className="sr-only">{social.name}</span>
                  <div className="w-5 h-5 bg-current opacity-50" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6">Explore</h4>
            <ul className="space-y-4">
              {exploreLinks.map((item) => (
                <li key={item.name}>
                  <Link href={item.href} className="text-gray-400 hover:text-primary-400 transition-colors">
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6">Topics</h4>
            <ul className="space-y-4">
              {topicLinks.map((item) => (
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
            <p className="text-gray-400 mb-4">Short notes from the work. Useful, no noise.</p>
            <form className="space-y-4" onSubmit={handleSubscribe}>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={status === 'sending'}
                className="w-full bg-background border border-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-all"
              />
              <button type="submit" disabled={status === 'sending'} className="w-full btn-primary disabled:opacity-50">
                {status === 'sending' ? 'Subscribing…' : 'Subscribe'}
              </button>
              {status === 'success' && <p className="text-sm text-emerald-400">{message}</p>}
              {status === 'error' && <p className="text-sm text-red-400">{message}</p>}
            </form>
          </div>
        </div>

        <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
          <p>&copy; {currentYear} GJH Consulting. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
            <a href="https://gjh-inc.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">Part of GJH Inc</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
