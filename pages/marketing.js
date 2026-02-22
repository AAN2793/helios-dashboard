import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

export default function Marketing() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/generated-posts')
      .then(res => res.json())
      .then(data => {
        setPosts(data.posts || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
        <h1 style={{ fontSize: '28px', marginBottom: '10px' }}>📣 Marketing Content</h1>
        <p style={{ color: '#666', marginBottom: '30px' }}>
          AI-generated marketing posts for AlertsAndNews
        </p>

        {loading ? (
          <p>Loading...</p>
        ) : posts.length === 0 ? (
          <div style={{ 
            padding: '40px', 
            textAlign: 'center', 
            background: '#f5f5f5',
            borderRadius: '10px'
          }}>
            <p style={{ color: '#666' }}>No marketing posts yet.</p>
            <p style={{ color: '#999', fontSize: '14px' }}>
              Run Allen or use Codex/Claude to generate content.
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {posts.map((post, index) => (
              <div 
                key={index}
                style={{
                  background: 'white',
                  border: '1px solid #e0e0e0',
                  borderRadius: '10px',
                  padding: '20px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
                }}
              >
                <div style={{ 
                  fontFamily: 'monospace', 
                  color: '#0066cc',
                  fontWeight: 'bold',
                  marginBottom: '8px'
                }}>
                  ${post.ticker || 'TICKER'}
                </div>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '16px' }}>
                  {post.headline || 'Headline here'}
                </h3>
                <p style={{ color: '#555', margin: 0, fontSize: '14px', lineHeight: '1.5' }}>
                  {post.body || 'Body content...'}
                </p>
                {post.source && (
                  <p style={{ color: '#999', fontSize: '12px', marginTop: '10px' }}>
                    Source: {post.source}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        <div style={{ marginTop: '40px', padding: '20px', background: '#f0f7ff', borderRadius: '10px' }}>
          <h3 style={{ marginTop: 0 }}>💡 How to Generate More Content</h3>
          <ul style={{ color: '#555', lineHeight: '1.8' }}>
            <li>Run the Allen content writer cron job</li>
            <li>Use Claude Code: <code>claude "Generate 5 marketing posts for AlertsAndNews"</code></li>
            <li>Use Codex: <code>codex "Generate engaging financial posts"</code></li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
