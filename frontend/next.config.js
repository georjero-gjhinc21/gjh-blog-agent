const nextConfig = {
  output: 'standalone',
  images: {
    domains: ['gjhconsulting.net'],
  },
  webpack(config) {
    return config;
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
