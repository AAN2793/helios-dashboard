import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export const dynamic = 'force-dynamic'

export default function Posts() {
  const [posts, setPosts] = useState([])
  const [copied, setCopied] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/generated-posts')
      .then(res => res.json())
      .then(data => {
        if (data.posts && data.posts.length > 0) {
          setPosts(data.posts)
        }
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading posts:', err)
        setLoading(false)
      })
  }, [])

  const copyToClipboard = (index, text) => {
    navigator.clipboard.writeText(text)
    setCopied(index)
    setTimeout(() => setCopied(null), 2000)
  }

  const getFullText = (post) => {
    return `${post.ticker}\n${post.headline}\n\n${post.body} - ${post.source}`
  }

  if (loading) {
    return (
      <Layout title="Posts | Braxton Helios">
        <div className="text-slate-400">Loading posts...</div>
      </Layout>
    )
  }

  return (
    <Layout title="Posts | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">Posts</h1>
        <p className="text-slate-400 mt-2">Market news posts - Copy/paste ready</p>
      </header>

      <div className="mb-4 text-sm text-slate-400">
        User does market moves. Helios does market news.
      </div>

      {posts.length === 0 ? (
        <div className="text-slate-400">No posts available. Run Allen to generate content.</div>
      ) : (
        <div className="grid gap-4">
          {posts.map((post, idx) => (
            <div key={idx} className="card p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <span className="text-xs text-cyan-400 uppercase tracking-wide">{post.ticker}</span>
                </div>
                <button
                  onClick={() => copyToClipboard(idx, getFullText(post))}
                  className={`px-3 py-1 text-xs rounded transition-colors ${
                    copied === idx 
                      ? 'bg-green-900 text-green-300' 
                      : 'bg-cyan-900 text-cyan-300 hover:bg-cyan-800'
                  }`}
                >
                  {copied === idx ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <div className="font-bold text-orange-400 mb-2">{post.headline}</div>
              <div className="text-slate-300 text-sm whitespace-pre-wrap">{post.body}</div>
              <div className="text-xs text-slate-500 mt-2">Source: {post.source}</div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}
