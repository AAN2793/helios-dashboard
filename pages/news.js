import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export const dynamic = 'force-dynamic'

export default function News() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')
  const [copied, setCopied] = useState(null)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    setLoading(true)
    try {
      // Fetch AI-generated posts
      const res = await fetch('/api/generated-posts')
      const data = await res.json()
      
      // Combine with any other sources
      const allPosts = []
      
      if (data.posts && data.posts.length > 0) {
        data.posts.forEach((post, idx) => {
          allPosts.push({
            ...post,
            id: `ai-${idx}`,
            source: 'AI',
            timestamp: data.generated
          })
        })
      }
      
      setPosts(allPosts)
    } catch (err) {
      console.error('Error loading posts:', err)
    } finally {
      setLoading(false)
    }
  }

  const deletePost = async (id) => {
    if (!confirm('Delete this post?')) return
    
    // Extract index from id (e.g., "ai-0" -> 0)
    const index = parseInt(id.split('-')[1])
    
    try {
      const res = await fetch('/api/generated-posts', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index })
      })
      if (res.ok) {
        fetchPosts()
      }
    } catch (err) {
      alert('Failed to delete: ' + err.message)
    }
  }

  const copyToClipboard = (text, idx) => {
    navigator.clipboard.writeText(text)
    setCopied(idx)
    setTimeout(() => setCopied(null), 2000)
  }

  const getFullText = (post) => {
    return `${post.ticker || '$' + post.ticker}\n${post.headline}\n\n${post.body}${post.source ? '\n\n' + post.source : ''}`
  }

  const filteredPosts = filter === 'all' 
    ? posts 
    : posts.filter(p => p.source === filter)

  const sources = ['all', 'AI', 'Tom', 'Manual']

  return (
    <Layout title="News | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-orange-500">📰 News Feed</h1>
        <p className="text-slate-400 mt-2">All posts in one place - Copy & paste ready</p>
      </header>

      {/* Filters */}
      <div className="mb-6 flex gap-2 flex-wrap">
        {sources.map(source => (
          <button
            key={source}
            onClick={() => setFilter(source)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === source 
                ? 'bg-orange-500 text-white' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            {source === 'all' ? 'All Posts' : source}
          </button>
        ))}
        <button
          onClick={fetchPosts}
          className="px-4 py-2 bg-cyan-800 text-cyan-100 rounded-lg text-sm hover:bg-cyan-700"
        >
          ↻ Refresh
        </button>
      </div>

      {/* Stats */}
      <div className="mb-6 flex gap-4 text-sm">
        <span className="text-slate-400">Total: <span className="text-white">{posts.length}</span></span>
        <span className="text-slate-400">Filtered: <span className="text-white">{filteredPosts.length}</span></span>
      </div>

      {loading ? (
        <div className="text-slate-400">Loading posts...</div>
      ) : filteredPosts.length === 0 ? (
        <div className="text-slate-400">No posts found. Run Allen to generate content.</div>
      ) : (
        <div className="grid gap-4">
          {filteredPosts.map((post, idx) => (
            <div key={post.id} className="bg-slate-800 rounded-lg p-5 border-l-4 border-orange-500">
              <div className="flex justify-between items-start mb-3">
                <div className="flex gap-2 items-center">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    post.source === 'AI' ? 'bg-green-900 text-green-300' :
                    post.source === 'Tom' ? 'bg-cyan-900 text-cyan-300' :
                    'bg-slate-700 text-slate-300'
                  }`}>
                    {post.source}
                  </span>
                  <span className="text-cyan-400 font-mono text-sm">
                    {post.ticker || 'N/A'}
                  </span>
                </div>
                <div className="flex gap-2">
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
                  <button
                    onClick={() => deletePost(post.id)}
                    className="px-3 py-1 text-sm bg-red-900 text-red-300 rounded hover:bg-red-800"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
              
              <h3 className="text-lg font-bold text-white mb-2">{post.headline}</h3>
              <p className="text-slate-300 text-sm whitespace-pre-wrap">{post.body}</p>
              
              {post.source && (
                <div className="text-xs text-slate-500 mt-3">
                  {post.timestamp && <span>Generated: {post.timestamp}</span>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}
