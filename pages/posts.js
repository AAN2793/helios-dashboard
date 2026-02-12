import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: 'Evening - Feb 11, 2026',
      tickers: '$USO $CVX $XLE',
      content: 'Energy — China has already purchased some of the Venezuelan crude sold by the United States government, Energy Secretary Chris Wright confirmed. The development highlights the shifting dynamics in global energy markets as U.S. sanctions reshape oil trade routes. China buying Venezuelan oil sold by US - sanctions reshaping global flows.'
    },
    {
      time: 'Evening - Feb 11, 2026',
      tickers: '$BX $AI',
      content: 'Tech — Blackstone Group has deepened its stake in Anthropic, raising its investment to approximately $1 billion at a valuation of roughly $350 billion. The move underscores continued institutional appetite for artificial intelligence assets despite valuation concerns. AI remains hot with big money despite the high prices.'
    },
    {
      time: 'Evening - Feb 11, 2026',
      tickers: '$META $AMZN $NVDA',
      content: 'Global — The Vatican Bank\'s Catholic Values index reveals a distinctly tech-heavy portfolio. Top three holdings: Meta Platforms (META), Amazon (AMZN), and Nvidia (NVDA). Even the Vatican is buying the mega caps.'
    },
    {
      time: 'Evening - Feb 11, 2026',
      tickers: '$NCI',
      content: 'Market Moves — Small-cap alert on $NCI, which surged over 100% after being flagged at $1.00s with a $1.50++ price target. Traders advised raising stops to $1.20 to capture further upside. Small cap runner catching fire - tight stops required.'
    },
    {
      time: 'Evening - Feb 11, 2026',
      tickers: '$META $AI',
      content: 'Options Watch — Actor Alexander Skarsgard has confirmed that a viral advertisement featuring his likeness is authentic. The video, previously thought to be an AI-generated deepfake, was not produced by OpenAI. Deepfake concerns spreading as AI gets better at faking faces.'
    }
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
        <p className="text-slate-400 mt-2">Copy/paste ready for X and StockTwits</p>
      </header>

      <div className="grid gap-4">
        {posts.map((post, idx) => (
          <div key={idx} className="card p-4">
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs text-slate-500">{post.time}</span>
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
