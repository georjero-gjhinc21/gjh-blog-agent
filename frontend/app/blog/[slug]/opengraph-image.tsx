import { ImageResponse } from 'next/og'
import { getPostBySlug } from '@/lib/posts'

export const runtime = 'nodejs'

export const alt = 'GJH Consulting Blog Post'
export const size = {
  width: 1200,
  height: 630,
}
export const contentType = 'image/png'

export default async function Image({ params }: { params: { slug: string } }) {
  const post = getPostBySlug(params.slug)
  const title = post?.title || 'GJH Consulting Insights'
  const date = post?.date ? new Date(post.date).toLocaleDateString('en-US', { dateStyle: 'long' }) : ''

  return new ImageResponse(
    (
      <div
        style={{
          background: '#030712',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          fontFamily: 'sans-serif',
          padding: '80px',
          position: 'relative',
        }}
      >
        {/* Background Elements */}
        <div
          style={{
            position: 'absolute',
            top: '-100px',
            right: '-100px',
            width: '600px',
            height: '600px',
            background: 'rgba(14, 165, 233, 0.1)',
            borderRadius: '100%',
            filter: 'blur(100px)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            bottom: '-100px',
            left: '-100px',
            width: '500px',
            height: '500px',
            background: 'rgba(139, 92, 246, 0.1)',
            borderRadius: '100%',
            filter: 'blur(100px)',
          }}
        />

        <div
          style={{
            fontSize: 24,
            color: '#38bdf8',
            marginBottom: 20,
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '2px',
          }}
        >
          GJH Consulting Insights
        </div>
        
        <div
          style={{
            fontSize: 64,
            fontWeight: 800,
            background: 'linear-gradient(to right, #ffffff, #e0f2fe)',
            backgroundClip: 'text',
            color: 'transparent',
            marginBottom: 40,
            lineHeight: 1.1,
            maxWidth: '1000px',
          }}
        >
          {title}
        </div>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 20,
          }}
        >
          {date && (
            <div
              style={{
                fontSize: 24,
                color: '#9ca3af',
              }}
            >
              {date}
            </div>
          )}
          {post?.readingTime && (
            <>
              <div style={{ color: '#4b5563' }}>•</div>
              <div
                style={{
                  fontSize: 24,
                  color: '#9ca3af',
                }}
              >
                {post.readingTime} min read
              </div>
            </>
          )}
        </div>
      </div>
    ),
    {
      ...size,
    }
  )
}
