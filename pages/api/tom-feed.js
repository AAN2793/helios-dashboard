import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  const reportPath = '/Users/helios/.openclaw/workspace/twitter_tom_report.txt'
  
  try {
    if (!fs.existsSync(reportPath)) {
      return res.status(200).json({ feed: [], timestamp: null })
    }
    
    const content = fs.readFileSync(reportPath, 'utf8')
    const lines = content.split('\n')
    
    const feed = []
    let currentCategory = ''
    let currentTweet = {}
    
    for (const line of lines) {
      // Category header
      if (line.startsWith('--- ')) {
        currentCategory = line.replace(/---/g, '').trim()
        continue
      }
      
      // Tweet author/time
      if (line.match(/^@\w+ \| \d{2}:\d{2}/)) {
        if (currentTweet.text) {
          feed.push(currentTweet)
        }
        const parts = line.split(' | ')
        currentTweet = {
          category: currentCategory,
          author: parts[0],
          time: parts[1] || '',
          text: '',
          rt: 0,
          likes: 0
        }
        continue
      }
      
      // RT count
      if (line.startsWith('RT:')) {
        currentTweet.rt = parseInt(line.replace('RT:', '').trim()) || 0
        continue
      }
      
      // Likes count
      if (line.startsWith('LIKE:')) {
        currentTweet.likes = parseInt(line.replace('LIKE:', '').trim()) || 0
        continue
      }
      
      // Tweet text
      if (line.trim() && !line.startsWith('===') && !line.startsWith('Generated:')) {
        currentTweet.text = line.trim()
      }
    }
    
    if (currentTweet.text) {
      feed.push(currentTweet)
    }
    
    // Get file modification time
    const stats = fs.statSync(reportPath)
    
    res.status(200).json({
      feed: feed.reverse(),
      timestamp: stats.mtime.toISOString()
    })
  } catch (e) {
    console.error('Error reading Tom feed:', e)
    res.status(200).json({ feed: [], timestamp: null })
  }
}
