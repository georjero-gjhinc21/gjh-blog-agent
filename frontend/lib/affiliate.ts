/**
 * Central affiliate-link builder — the single place where tracking is applied.
 *
 * - Preserves any ref/sub_id already present on vendor URLs (never overwrites).
 * - Appends NEXT_PUBLIC_AFFILIATE_REF as `ref` when the URL has none and the
 *   env var is configured (no secrets in the repo; set it in Vercel).
 * - Always stamps utm_source/medium/content so clicks attribute in analytics.
 */
const AFFILIATE_REF = (process.env.NEXT_PUBLIC_AFFILIATE_REF ?? '').trim()

export function getAffiliateUrl(baseUrl: string, content: string): string {
  try {
    const url = new URL(baseUrl)
    if (AFFILIATE_REF && !url.searchParams.has('ref')) {
      url.searchParams.set('ref', AFFILIATE_REF)
    }
    url.searchParams.set('utm_source', 'gjhconsulting')
    url.searchParams.set('utm_medium', 'partners')
    url.searchParams.set('utm_content', content)
    return url.toString()
  } catch {
    return baseUrl
  }
}
