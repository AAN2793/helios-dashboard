import { useState } from 'react'
import Layout from '../components/Layout'

export default function Marketing() {
  const [content, setContent] = useState([])
  const [loading, setLoading] = useState(false)
  const [generatingType, setGeneratingType] = useState(null)

  const contentTypes = [
    { id: 'trading-tips', label: '💡 Trading Tips', prompt: 'Generate 5 practical trading tips for day traders. Keep each under 280 characters. Punchy and actionable.' },
    { id: 'market-commentary', label: '📊 Market Commentary', prompt: 'Write a Brief market commentary (3-4 sentences) about current market sentiment. Include 1-2 stock examples.' },
    { id: 'strategy', label: '🎯 Strategy Ideas', prompt: 'Explain a trading strategy in simple terms. Include entry criteria, exit plan, and risk management. Keep it beginner-friendly.' },
    { id: 'stock-ideas', label: '🚀 Stock Ideas', prompt: 'Generate 3 swing trade ideas with: Ticker, Entry price, Target price, Stop loss, and Why it\'s interesting. Use realistic prices.' },
    { id: 'earnings', label: '📈 Earnings Preview', prompt: 'Preview 3 stocks reporting earnings this week. Include: Ticker, Expected EPS, Date, and one key metric to watch.' },
    { id: 'thread-starters', label: '🧵 Thread Starters', prompt: 'Create 3 Twitter thread starters about trading psychology. Hook readers in the first tweet.' },
  ]

  const generateContent = async (type) => {
    setLoading(true)
    setGeneratingType(type)
    const contentType = contentTypes.find(c => c.id === type)
    
    try {
      const res = await fetch('/api/generate-marketing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: contentType.prompt })
      })
      
      const data = await res.json()
      
      if (data.error) {
        throw new Error(data.error)
      }

      const newContent = {
        id: Date.now(),
        type: type,
        label: contentType.label,
        text: data.content,
        timestamp: new Date().toLocaleString()
      }

      setContent(prev => [newContent, ...prev])
    } catch (err) {
      alert('Error generating content: ' + err.message)
    } finally {
      setLoading(false)
      setGeneratingType(null)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Copied to clipboard!')
  }

  const deleteContent = (id) => {
    if (confirm('Delete this content?')) {
      setContent(prev => prev.filter(c => c.id !== id))
    }
  }

  return (
    <Layout>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
        <h1 style={{ fontSize: '28px', marginBottom: '10px' }}>📣 Marketing Content</h1>
        <p style={{ color: '#666', marginBottom: '30px' }}>
          Generate marketing content using AI. Copy what you like, delete what you don't.
        </p>

        {/* Content Type Buttons */}
        <div style={{ marginBottom: '30px' }}>
          <h3 style={{ marginBottom: '15px', color: '#333' }}>Generate New Content:</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {contentTypes.map(type => (
              <button
                key={type.id}
                onClick={() => generateContent(type.id)}
                disabled={loading}
                style={{
                  padding: '12px 20px',
                  background: loading ? '#ccc' : '#f0f0f0',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'all 0.2s'
                }}
              >
                {generatingType === type.id ? '⏳ Generating...' : type.label}
              </button>
            ))}
          </div>
        </div>

        {/* Generated Content */}
        {content.length === 0 ? (
          <div style={{ 
            padding: '40px', 
            textAlign: 'center', 
            background: '#f5f5f5',
            borderRadius: '10px'
          }}>
            <p style={{ color: '#666' }}>No content generated yet.</p>
            <p style={{ color: '#999', fontSize: '14px' }}>
              Click a button above to generate marketing content.
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {content.map((item) => (
              <div 
                key={item.id}
                style={{
                  background: '#16213e',
                  border: '1px solid #0f3460',
                  borderRadius: '10px',
                  padding: '20px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
                }}
              >
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  marginBottom: '15px'
                }}>
                  <span style={{
                    padding: '4px 12px',
                    background: '#e8f5e9',
                    color: '#2e7d32',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: '500'
                  }}>
                    {item.label}
                  </span>
                  <span style={{ fontSize: '12px', color: '#999' }}>
                    {item.timestamp}
                  </span>
                </div>
                
                <pre style={{
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'inherit',
                  fontSize: '14px',
                  lineHeight: '1.6',
                  color: '#fff',
                  margin: 0,
                  background: '#1a1a2e',
                  padding: '15px',
                  borderRadius: '8px'
                }}>
                  {item.text}
                </pre>

                <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                  <button
                    onClick={() => copyToClipboard(item.text)}
                    style={{
                      padding: '8px 16px',
                      background: '#2196f3',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '13px'
                    }}
                  >
                    📋 Copy
                  </button>
                  <button
                    onClick={() => deleteContent(item.id)}
                    style={{
                      padding: '8px 16px',
                      background: '#ffebee',
                      color: '#c62828',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '13px'
                    }}
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tips */}
        <div style={{ marginTop: '40px', padding: '20px', background: '#f0f7ff', borderRadius: '10px' }}>
          <h3 style={{ marginTop: 0, marginBottom: '10px' }}>💡 How to use this:</h3>
          <ul style={{ color: '#555', lineHeight: '1.8', margin: 0 }}>
            <li>Click a category button to generate content</li>
            <li>Review the AI-generated output</li>
            <li>Click "Copy" to copy to clipboard, then paste to StockTwits/X</li>
            <li>Click "Delete" to remove content you don't want</li>
            <li>Content saves in this session - will reset on page refresh</li>
          </ul>
        </div>
      </div>
    </Layout>
  )
}
