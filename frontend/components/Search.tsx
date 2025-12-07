'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { useState, useEffect, useTransition } from 'react'

export default function Search() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isPending, startTransition] = useTransition()
  const [term, setTerm] = useState(searchParams.get('query') || '')

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      const currentQuery = searchParams.get('query') || ''
      if (term === currentQuery) return

      const params = new URLSearchParams(searchParams)
      if (term) {
        params.set('query', term)
      } else {
        params.delete('query')
      }
      params.delete('page')
      
      startTransition(() => {
        router.replace(`/blog?${params.toString()}`)
      })
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [term, searchParams, router])

  return (
    <div className="relative mb-8 max-w-md mx-auto">
      <label htmlFor="search" className="sr-only">Search</label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <svg className="w-4 h-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
          </svg>
        </div>
        <input
          type="search"
          id="search"
          className="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-primary-500 focus:border-primary-500 shadow-sm"
          placeholder="Search articles..."
          value={term}
          onChange={(e) => setTerm(e.target.value)}
        />
        {isPending && (
          <div className="absolute inset-y-0 right-0 flex items-center pr-3">
             <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          </div>
        )}
      </div>
    </div>
  )
}
