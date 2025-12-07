import { ImageResponse } from 'next/og'

export const runtime = 'edge'

export const alt = 'GJH Consulting'
export const size = {
  width: 1200,
  height: 630,
}
export const contentType = 'image/png'

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: '#030712',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'sans-serif',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(to right bottom, #111827, #1f2937)',
            padding: '40px 80px',
            borderRadius: '24px',
            border: '1px solid rgba(255,255,255,0.1)',
            boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
          }}
        >
          <div
            style={{
              fontSize: 60,
              fontWeight: 800,
              background: 'linear-gradient(to right, #ffffff, #bae6fd, #38bdf8)',
              backgroundClip: 'text',
              color: 'transparent',
              marginBottom: 20,
            }}
          >
            GJH Consulting
          </div>
          <div
            style={{
              fontSize: 30,
              color: '#9ca3af',
              textAlign: 'center',
              maxWidth: 800,
            }}
          >
            Government Contracting • GSA Schedules • Technology
          </div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  )
}
