import type { Metadata } from 'next'
import { Inter, Plus_Jakarta_Sans } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-heading',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'GJH Consulting - Government Contracting Insights',
  description: 'Expert insights on government contracting, federal procurement, GSA schedules, and technology consulting.',
  keywords: ['government contracting', 'federal procurement', 'GSA schedules', 'SBIR', 'STTR', 'cybersecurity compliance'],
  authors: [{ name: 'GJH Consulting' }],
  metadataBase: new URL('https://gjhconsulting.net'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'GJH Consulting - Government Contracting Insights',
    description: 'Expert insights on government contracting, federal procurement, and technology consulting.',
    url: 'https://gjhconsulting.net',
    siteName: 'GJH Consulting',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GJH Consulting',
    description: 'Expert insights on government contracting and federal procurement',
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
    <html lang="en" className={`${inter.variable} ${plusJakarta.variable}`}>
      <body className="font-sans min-h-screen flex flex-col bg-background text-gray-300">
        <Header />
        <main className="flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
