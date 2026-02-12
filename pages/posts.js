import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: '5:41 AM - Feb 12, 2026',
      category: 'BREAKING',
      tickers: 'NOTE',
      content: 'FiscalNote $NOTE is moving into political prediction markets, launching a preview at PoliticalPredictions.com and signing an MOU with 365Prediction to build out market design and backend tech. Strategy discussion Feb 18 at 11AM ET.'
    },
    {
      time: '5:41 AM - Feb 12, 2026',
      category: 'EARNINGS',
      tickers: 'CROX',
      content: 'Crocs Q4 BEAT: Revenue $958M (est $916M), EPS $2.29 (est $1.91). Crocs brand +0.8% YoY, HEYDUDE -16.9% YoY. FY guidance raised.'
    },
    {
      time: '5:41 AM - Feb 12, 2026',
      category: 'EARNINGS',
      tickers: 'NBIS',
      content: 'NebuData Q4 MIXED: Revenue $227M miss, EPS -$0.68 miss. But ARR now $1.25B, targeting $7-9B by YE26. Contracted power raised to 3+ GW.'
    },
    {
      time: '5:41 AM - Feb 12, 2026',
      category: 'UPGRADE',
      tickers: 'SHOP',
      content: 'MoffettNathanson upgrades Shopify to Buy, PT $150 from $122. Analyst: "Software wipeout on vibe coding fears hit SHOP despite not being a traditional software company."'
    },
    {
      time: '5:41 AM - Feb 12, 2026',
      category: 'MACRO',
      tickers: 'US ECON',
      content: '26% of the 7.5 million unemployed Americans have been searching for work for more than 6 months, per Financial Times via @unusual_whales.'
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
