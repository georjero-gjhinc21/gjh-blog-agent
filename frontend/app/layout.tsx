import type { Metadata } from 'next'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'GJH Consulting \u2014 AI-First Partner',
  description: 'Practical help putting AI to work: advisory, building, data foundations, and ongoing support.',
  keywords: ['AI consulting', 'AI partner', 'data foundations', 'AI assistants', 'automation', 'AI strategy'],
  authors: [{ name: 'GJH Consulting' }],
  metadataBase: new URL('https://gjhconsulting.net'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'GJH Consulting \u2014 AI-First Partner',
    description: 'Practical help putting AI to work: advisory, building, data foundations, and ongoing support.',
    url: 'https://gjhconsulting.net',
    siteName: 'GJH Consulting',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GJH Consulting',
    description: 'Practical help putting AI to work: advisory, building, and data foundations',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-background text-gray-300">
        <Header />
        <main className="flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
