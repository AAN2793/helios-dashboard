import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export const dynamic = 'force-dynamic'

export default function Tom() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [lastRun, setLastRun] = useState(null)
  const [copied, setCopied] = useState(null)

  useEffect(() => {
    fetchTomPosts()
  }, [])

  const fetchTomPosts = async () => {
    setLoading(true)
    try {
      // Fetch Tom's report if available
      const res = await fetch('/api/tom-report')
      const data = await res.json()
      
      if (data.posts && data.posts.length > 0) {
        setPosts(data.posts)
        setLastRun(data.lastRun)
      }
    } catch (err) {
      console.error('Error loading Tom posts:', err)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text, idx) => {
    navigator.clipboard.writeText(text)
    setCopied(idx)
    setTimeout(() => setCopied(null), 2000)
  }

  const getFullText = (post) => {
    return `${post.ticker || ''}\n${post.title || post.headline}\n\n${post.content || post.body}`
  }

  return (
    <Layout title="Tom Posts | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-cyan-500">🐦 Tom Posts</h1>
        <p className="text-slate-400 mt-2">AI-generated tweets from Tom - Copy & paste ready</p>
      </header>

      {/* Last Run Info */}
      {lastRun && (
        <div className="mb-6 p-4 bg-slate-800 rounded-lg">
          <p className="text-slate-400 text-sm">
            Last Run: <span className="text-cyan-400">{new Date(lastRun).toLocaleString()}</span>
          </p>
        </div>
      )}

      {/* Refresh Button */}
      <div className="mb-6">
        <button
          onClick={fetchTomPosts}
          className="px-4 py-2 bg-cyan-800 text-cyan-100 rounded-lg text-sm hover:bg-cyan-700"
        >
          ↻ Refresh Tom Posts
        </button>
      </div>

      {loading ? (
        <div className="text-slate-400">Loading Tom's posts...</div>
      ) : posts.length === 0 ? (
        <div className="text-slate-400">
          <p className="mb-4">No posts from Tom yet. Run Tom to generate content.</p>
          <div className="card p-6 bg-slate-800/50">
            <h3 className="font-semibold text-cyan-400 mb-2">How Tom Works</h3>
            <p className="text-slate-400 text-sm">
              Tom scans market news and generates tweets for AlertsAndNews. 
              Posts are saved to the news feed and can be copied directly to StockTwits or X.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid gap-4">
          {posts.map((post, idx) => (
            <div key={post.id || idx} className="bg-slate-800 rounded-lg p-5 border-l-4 border-cyan-500">
              <div className="flex justify-between items-start mb-3">
                <div className="flex gap-2 items-center">
                  <span className="px-2 py-1 text-xs rounded-full bg-cyan-900 text-cyan-300">
                    Tom
                  </span>
                  <span className="text-cyan-400 font-mono text-sm">
                    {post.ticker || 'N/A'}
                  </span>
                  {post.category && (
                    <span className="px-2 py-1 text-xs rounded-full bg-slate-700 text-slate-300">
                      {post.category}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => copyToClipboard(getFullText(post), idx)}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    copied === idx 
                      ? 'bg-green-900 text-green-300' 
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  {copied === idx ? '✓ Copied' : '📋 Copy'}
                </button>
              </div>
              
              <h3 className="text-lg font-bold text-white mb-2">
                {post.title || post.headline}
              </h3>
              <p className="text-slate-300 text-sm whitespace-pre-wrap">
                {post.content || post.body}
              </p>
              
              {post.hashtags && (
                <div className="flex gap-2 mt-3 flex-wrap">
                  {post.hashtags.map((tag, i) => (
                    <span key={i} className="text-xs text-slate-500">#{tag}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}