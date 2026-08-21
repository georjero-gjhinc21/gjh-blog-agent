const nextConfig = {
  output: 'standalone',
  experimental: {
    turbo: { enabled: false },
  },
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
