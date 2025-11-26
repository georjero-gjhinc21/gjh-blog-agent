import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About - GJH Consulting',
  description: 'Learn about GJH Consulting and our expertise in government contracting.',
}

export default function AboutPage() {
  return (
    <div className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold mb-6">About GJH Consulting</h1>
          <div className="prose prose-lg">
            <p className="text-xl text-gray-600 mb-6">
              Expert guidance in government contracting, federal procurement, and technology consulting.
            </p>

            <h2>Our Expertise</h2>
            <p>
              GJH Consulting specializes in helping businesses navigate the complex world of government contracting.
              Our team brings decades of combined experience in federal procurement, GSA schedules, and technology
              consulting to help you succeed in the government marketplace.
            </p>

            <h2>What We Cover</h2>
            <ul>
              <li>Government Contracting Strategy</li>
              <li>Federal Procurement Processes</li>
              <li>GSA Schedule Registration and Management</li>
              <li>SBIR/STTR Grant Applications</li>
              <li>Technology Consulting Services</li>
              <li>Data Analytics Solutions</li>
              <li>Cybersecurity Compliance (CMMC, NIST 800-171)</li>
            </ul>

            <h2>Our Mission</h2>
            <p>
              We're committed to providing actionable insights and practical guidance to help companies of all sizes
              successfully compete for and win government contracts. Through our blog and consulting services, we
              demystify the federal procurement process and empower businesses to grow their government contracting practice.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
