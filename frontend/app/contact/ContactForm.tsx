'use client'

import { useState } from 'react'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

type ContactStatus = 'idle' | 'sending' | 'success' | 'error'

const inputClass =
  'w-full bg-surface-highlight border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder-gray-600'

export default function ContactForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [subject, setSubject] = useState('')
  const [message, setMessage] = useState('')
  const [status, setStatus] = useState<ContactStatus>('idle')
  const [feedback, setFeedback] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim() || !subject.trim() || message.trim().length < 10) {
      setStatus('error')
      setFeedback('Please fill in all fields (message must be at least 10 characters).')
      return
    }
    if (!EMAIL_RE.test(email.trim())) {
      setStatus('error')
      setFeedback('Please enter a valid email address.')
      return
    }
    setStatus('sending')
    setFeedback('')
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim(), email: email.trim(), subject: subject.trim(), message: message.trim() }),
      })
      const data = await res.json().catch(() => ({}))
      if (res.ok) {
        setStatus('success')
        setFeedback("Message sent. We’ll be in touch.")
        setName('')
        setEmail('')
        setSubject('')
        setMessage('')
      } else {
        setStatus('error')
        setFeedback(typeof data.error === 'string' ? data.error : 'Message failed to send. Please try again.')
      }
    } catch {
      setStatus('error')
      setFeedback('Message failed to send. Please try again.')
    }
  }

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-400 mb-2">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            disabled={status === 'sending'}
            className={inputClass}
            placeholder="John Doe"
            required
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-400 mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={status === 'sending'}
            className={inputClass}
            placeholder="john@company.com"
            required
          />
        </div>
      </div>
      <div>
        <label htmlFor="subject" className="block text-sm font-medium text-gray-400 mb-2">
          Subject
        </label>
        <input
          type="text"
          id="subject"
          name="subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          disabled={status === 'sending'}
          className={inputClass}
          placeholder="How can we help?"
          required
        />
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-400 mb-2">
          Message
        </label>
        <textarea
          id="message"
          name="message"
          rows={5}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={status === 'sending'}
          className={`${inputClass} resize-none`}
          placeholder="Tell us about your project..."
          required
        ></textarea>
      </div>
      <button type="submit" disabled={status === 'sending'} className="btn-primary w-full group disabled:opacity-50">
        {status === 'sending' ? 'Sending…' : 'Send Message'}
        <svg className="w-5 h-5 ml-2 inline-block transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </button>
      {status === 'success' && <p className="text-sm text-emerald-400">{feedback}</p>}
      {status === 'error' && <p className="text-sm text-red-400">{feedback}</p>}
    </form>
  )
}
