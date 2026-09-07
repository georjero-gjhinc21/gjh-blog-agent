import { NextResponse } from 'next/server'
import { z } from 'zod'
import { Resend } from 'resend'

const newsletterSchema = z.object({
  email: z.string().email('Invalid email format'),
})

export async function POST(request: Request) {
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: 'Invalid request body' }, { status: 400 })
  }

  const validation = newsletterSchema.safeParse(body)
  if (!validation.success) {
    return NextResponse.json({ error: 'Invalid email format' }, { status: 400 })
  }

  const apiKey = process.env.RESEND_API_KEY
  const audienceId = process.env.NEWSLETTER_AUDIENCE_ID
  if (!apiKey || !audienceId) {
    return NextResponse.json({ error: 'newsletter-not-configured' }, { status: 503 })
  }

  try {
    const resend = new Resend(apiKey)
    const { error } = await resend.contacts.create({
      email: validation.data.email,
      audienceId,
    })
    if (error) {
      return NextResponse.json({ error: 'newsletter-service-unavailable' }, { status: 503 })
    }
    return NextResponse.json({ status: 'success', message: "You're subscribed." })
  } catch {
    return NextResponse.json({ error: 'newsletter-service-unavailable' }, { status: 503 })
  }
}
