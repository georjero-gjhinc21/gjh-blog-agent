import { NextResponse } from 'next/server'
import { z } from 'zod'
import { Resend } from 'resend'

const contactSchema = z.object({
  name: z.string().trim().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  subject: z.string().trim().min(1, 'Subject is required'),
  message: z.string().trim().min(10, 'Message must be at least 10 characters'),
})

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

export async function POST(request: Request) {
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 })
  }

  const validation = contactSchema.safeParse(body)
  if (!validation.success) {
    return NextResponse.json({ error: 'Validation failed', details: validation.error.issues }, { status: 400 })
  }

  const apiKey = process.env.RESEND_API_KEY
  const to = process.env.CONTACT_TO_EMAIL
  const from = process.env.CONTACT_FROM_EMAIL ?? process.env.NEWSLETTER_FROM_EMAIL
  if (!apiKey || !to || !from) {
    return NextResponse.json({ error: 'contact-not-configured' }, { status: 503 })
  }

  const { name, email, subject, message } = validation.data

  try {
    const resend = new Resend(apiKey)
    const { error } = await resend.emails.send({
      from,
      to,
      replyTo: email,
      subject: `Website inquiry: ${subject}`,
      html: `<h3>New contact submission</h3><p><strong>Name:</strong> ${escapeHtml(name)}</p><p><strong>Email:</strong> ${escapeHtml(email)}</p><p><strong>Subject:</strong> ${escapeHtml(subject)}</p><p><strong>Message:</strong> ${escapeHtml(message)}</p>`,
    })
    if (error) {
      return NextResponse.json({ error: 'contact-service-unavailable' }, { status: 503 })
    }
    return NextResponse.json({ status: 'success', message: "Message sent. We’ll be in touch." })
  } catch {
    return NextResponse.json({ error: 'contact-service-unavailable' }, { status: 503 })
  }
}
