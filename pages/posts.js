import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: 'Morning - Feb 12, 2026',
      category: 'TRENDING',
      tickers: 'NVCR',
      content: 'NVCR EXPLODES 30%+ overnight! FDA approves Optune Pax for locally advanced pancreatic cancer treatment. Major catalyst alert. Biotech magic at work.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'TRENDING',
      tickers: 'VKTX',
      content: 'VKTX rips +9% after-hours. Oral obesity drug heading to Phase 3 trials this quarter. The obesity drug trade is not done. Viking charging forward.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'RETAIL SENTIMENT',
      tickers: 'IGV',
      content: 'IGV sees RECORD retail buying: $176 million last month alone. Thats 12x higher than January. Retail going all-in on the software dip despite being in a bear market.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'RETAIL SENTIMENT',
      tickers: 'AMZN',
      content: 'Amazon is now the #1 most-purchased stock by RETAIL investors. Overtakes NVIDIA per The Kobeissi Letter. Post-earnings dip drawing buyers.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'TRENDING',
      tickers: 'MU',
      content: 'MU ripping +10%! Deutsche Bank raises PT to $500 (from $300). Samsung sees memory chip demand staying hot through 2026. Memory is the new oil.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'TRENDING',
      tickers: 'VRT',
      content: 'VRT EXPLODES 25%+ on guidance beat. AI data center infrastructure play crushing it. Q1 guidance absolutely on fire. Pickaxe play for the AI gold rush.'
    },
  ]

  const copyToClipboard = (index, text) => {
    navigator.clipboard.writeText(text)
    setCopied(index)
    setTimeout(() => setCopied(null), 2000)
  }

  const getFullText = (post) => {
    return `${post.tickers}\n${post.content}`
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

      <div className="grid gap-4">
        {posts.map((post, idx) => (
          <div key={idx} className="card p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <span className="text-xs text-cyan-400 uppercase tracking-wide">{post.category}</span>
                <span className="text-xs text-slate-500 ml-2">{post.time}</span>
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
            <div className="font-bold text-orange-400 mb-2">{post.tickers}</div>
            <div className="text-slate-300 text-sm whitespace-pre-wrap">{post.content}</div>
          </div>
        ))}
      </div>
    </Layout>
  )
}
