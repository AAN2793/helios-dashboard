import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  // Try multiple possible locations for Tom's report
  const possiblePaths = [
    path.join(process.cwd(), 'data', 'tom-report.json'),
    path.join(process.cwd(), '..', 'twitter_tom_report.txt'),
    path.join(process.cwd(), '..', '..', 'twitter_tom_report.txt'),
    path.join(process.cwd(), 'data', 'twitter_tom_report.txt'),
  ]

  // GET - return Tom posts
  if (req.method === 'GET') {
    try {
      let tomData = null
      let foundPath = null

      // Try to find and parse Tom's report
      for (const filePath of possiblePaths) {
        if (fs.existsSync(filePath)) {
          foundPath = filePath
          const content = fs.readFileSync(filePath, 'utf-8')
          
          // Try to parse as JSON first
          try {
            tomData = JSON.parse(content)
          } catch {
            // If not JSON, create a structured response from text
            tomData = {
              lastRun: new Date().toISOString(),
              rawContent: content,
              posts: parseTomReport(content)
            }
          }
          break
        }
      }

      if (tomData) {
        return res.status(200).json(tomData)
      }

      // Return sample data if no report found
      return res.status(200).json({
        lastRun: null,
        posts: [],
        message: 'No Tom report found. Run Tom to generate content.'
      })
    } catch (err) {
      return res.status(200).json({
        lastRun: null,
        posts: [],
        error: err.message
      })
    }
  }

  res.status(405).json({ error: 'Method not allowed' })
}

// Parse Tom's report text into structured posts
function parseTomReport(content) {
  const posts = []
  const lines = content.split('\n')
  
  let currentPost = null
  
  for (const line of lines) {
    const trimmed = line.trim()
    
    // Look for ticker symbols (e.g., $AMD, $META)
    const tickerMatch = trimmed.match(/\$([A-Z]{1,5})/)
    const ticker = tickerMatch ? tickerMatch[1] : null
    
    // Look for category markers
    let category = null
    if (trimmed.toLowerCase().includes('breaking')) category = 'Breaking News'
    else if (trimmed.toLowerCase().includes('earnings')) category = 'Earnings'
    else if (trimmed.toLowerCase().includes('market') || trimmed.toLowerCase().includes('futures')) category = 'Market Watch'
    else if (trimmed.toLowerCase().includes('options')) category = 'Unusual Options'
    
    if (ticker || (category && trimmed.length > 20)) {
      if (currentPost) posts.push(currentPost)
      currentPost = {
        id: posts.length + 1,
        ticker: ticker,
        category: category,
        title: trimmed.substring(0, 100),
        content: trimmed
      }
    } else if (currentPost && trimmed.length > 0) {
      currentPost.content += '\n' + trimmed
    }
  }
  
  if (currentPost) posts.push(currentPost)
  
  return posts
}
