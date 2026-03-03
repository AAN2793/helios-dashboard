import { useState, useEffect } from 'react'
import Layout from '../components/Layout'

export default function ContentStrategy() {
  const [strategy, setStrategy] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStrategy()
  }, [])

  const fetchStrategy = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/content-strategy')
      const data = await res.json()
      setStrategy(data)
    } catch (err) {
      console.error('Error loading strategy:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="p-8 text-center text-gray-400">Loading...</div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-white mb-2">Content Strategy</h1>
        <p className="text-gray-400 mb-8">Recommendations for growing AlertsAndNews</p>

        {strategy && (
          <div className="space-y-8">
            {/* Goal */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-green-400 mb-2">🎯 Goal</h2>
              <p className="text-white">{strategy.goal}</p>
            </div>

            {/* Data Analysis */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-blue-400 mb-4">📊 What the Data Shows</h2>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-bold text-white mb-2">Top Performing Posts</h3>
                  <ul className="text-gray-300 space-y-2">
                    {strategy.topPosts?.map((post, i) => (
                      <li key={i} className="border-l-2 border-green-500 pl-3">
                        <span className="text-green-400 font-mono">{post.engagement}</span> - {post.example}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="font-bold text-white mb-2">What Drives Views</h3>
                  <ul className="text-gray-300 space-y-2">
                    {strategy.drivesViews?.map((item, i) => (
                      <li key={i} className="border-l-2 border-blue-500 pl-3">{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-purple-400 mb-4">💡 Recommendations</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {strategy.recommendations?.map((rec, i) => (
                  <div key={i} className="bg-gray-700 rounded-lg p-4">
                    <h3 className="font-bold text-white mb-1">{rec.title}</h3>
                    <p className="text-gray-300 text-sm">{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Content Mix */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-yellow-400 mb-4">📅 Suggested Content Mix</h2>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-gray-700">
                      <th className="pb-2 text-gray-400">Post Type</th>
                      <th className="pb-2 text-gray-400">Frequency</th>
                      <th className="pb-2 text-gray-400">Purpose</th>
                    </tr>
                  </thead>
                  <tbody>
                    {strategy.contentMix?.map((item, i) => (
                      <tr key={i} className="border-b border-gray-700">
                        <td className="py-2 text-white">{item.type}</td>
                        <td className="py-2 text-gray-300">{item.frequency}</td>
                        <td className="py-2 text-gray-300">{item.purpose}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Algorithm Notes */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-bold text-red-400 mb-4">🔄 Algorithm Notes</h2>
              <ul className="text-gray-300 space-y-2">
                {strategy.algorithmNotes?.map((note, i) => (
                  <li key={i} className="border-l-2 border-red-500 pl-3">{note}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <div className="mt-8 text-gray-500 text-sm">
          Last updated: {strategy?.lastUpdated || 'March 3, 2026'}
        </div>
      </div>
    </Layout>
  )
}