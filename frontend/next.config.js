/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['gjhconsulting.net'],
  },
  async rewrites() {
    return [
      {
        source: '/blog/:slug',
        destination: '/blog/:slug',
      },
    ]
  },
}

module.exports = nextConfig
