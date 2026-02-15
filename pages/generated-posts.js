import Head from 'next/head'
import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function GeneratedPosts() {
  const [posts, setPosts] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const res = await fetch('/api/generated-posts')
      if (!res.ok) throw new Error('Failed to fetch')
      const data = await res.json()
      setPosts(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const deletePost = async (index) => {
    if (!confirm('Delete this post?')) return
    try {
      const res = await fetch('/api/generated-posts', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index })
      })
      if (res.ok) {
        const data = await res.json()
        setPosts({ ...posts, posts: data.posts })
      }
    } catch (err) {
      alert('Failed to delete: ' + err.message)
    }
  }

  const refreshPosts = () => {
    setLoading(true)
    fetchPosts()
  }

  return (
    <Layout title="Generated Posts | Braxton Helios">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-green-500">AI-Generated Posts</h1>
        <p className="text-slate-400 mt-2">Auto-generated social media content from Tom's feed</p>
      </header>

      <div className="mb-6 flex gap-4">
        <button
          onClick={refreshPosts}
          className="px-4 py-2 bg-cyan-700 text-cyan-100 rounded hover:bg-cyan-600"
        >
          Refresh Posts
        </button>
        <a
          href="/tom-feed"
          className="px-4 py-2 bg-slate-700 text-slate-200 rounded hover:bg-slate-600"
        >
          View Raw Feed
        </a>
      </div>

      {loading && <div className="text-cyan-400">Loading generated posts...</div>}
      {error && <div className="text-red-400">Error: {error}</div>}

      {posts && (
        <div className="space-y-6">
          <div className="bg-slate-800 p-4 rounded">
            <span className="text-slate-400">Last Generated:</span>
            <span className="text-green-400 ml-2">{posts.generated}</span>
          </div>

          {(!posts.posts || posts.posts.length === 0) ? (
            <div className="text-slate-400">No posts generated yet</div>
          ) : (
            <div className="grid gap-4">
              {posts.posts.map((post, idx) => (
                <div key={idx} className="bg-slate-900 rounded-lg p-6 border-l-4 border-green-500">
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-3 py-1 bg-green-900 text-green-300 text-sm rounded-full">
                      {post.category}
                    </span>
                    <button
                      onClick={() => deletePost(idx)}
                      className="px-3 py-1 bg-red-900 text-red-300 text-sm rounded hover:bg-red-800"
                    >
                      Delete
                    </button>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">
                    {post.headline}
                  </h3>
                  <p className="text-slate-300 leading-relaxed">
                    {post.body}
                  </p>
                  <div className="mt-4 flex gap-2">
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(`${post.headline}\n\n${post.body}`)
                        alert('Copied to clipboard!')
                      }}
                      className="px-3 py-1 bg-slate-700 text-slate-300 text-sm rounded hover:bg-slate-600"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Layout>
  )
}
