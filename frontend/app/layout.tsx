import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'GJH Consulting - Government Contracting Insights',
  description: 'Expert insights on government contracting, federal procurement, GSA schedules, and technology consulting.',
  keywords: ['government contracting', 'federal procurement', 'GSA schedules', 'SBIR', 'STTR', 'cybersecurity compliance'],
  authors: [{ name: 'GJH Consulting' }],
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
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  )
}
