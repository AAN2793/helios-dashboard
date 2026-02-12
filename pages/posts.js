import Head from 'next/head'
import { useState } from 'react'
import Layout from '../components/Layout'

export default function Posts() {
  const [copied, setCopied] = useState(null)

  const posts = [
    {
      time: 'Morning - Feb 12, 2026',
      category: 'MARKET NEWS',
      tickers: '$SPY $QQQ $DIA',
      content: 'US stock futures dip after Wall Street rally stalls on rate concerns. Strong January jobs data pushed Treasury yields higher, weighing on equity valuations. Market pricing in fewer Fed cuts than previously expected.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'MARKET NEWS',
      tickers: '$BTC $ETH $COIN',
      content: 'Bitcoin stabilizes above $96,000 as crypto markets digest Trump administration crypto reserve comments. Regulators still hashing out framework for digital assets. Volatility expected near key resistance levels.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'MARKET NEWS',
      tickers: '$NVDA $AMD $INTC',
      content: 'AI chip demand remains robust as enterprise spending accelerates. Nvidia continues to dominate data center GPU market with next-gen Blackwell chips shipping. AMD gaining traction in AI inference workloads.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'MARKET NEWS',
      tickers: '$AAPL $MSFT $GOOGL',
      content: 'Big tech earnings season winding down with most reports exceeding modest expectations. Focus shifts to consumer spending trends and cloud growth acceleration. Subscription revenue remains steady.'
    },
    {
      time: 'Morning - Feb 12, 2026',
      category: 'MARKET NEWS',
      tickers: '$USO $CVX $XLE',
      content: 'Oil markets volatile on shifting global trade dynamics. China reallocating energy purchases amid changing relationships. Energy sector remains sensitive to geopolitical developments.'
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
