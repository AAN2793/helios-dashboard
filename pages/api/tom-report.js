import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  const reportFile = '/Users/helios/.openclaw/workspace/twitter_tom_report.txt'

  try {
    const content = fs.readFileSync(reportFile, 'utf-8')
    const lines = content.split('\n')
    
    // Parse the report into structured data
    const result = {
      generated: '',
      categories: {},
      raw: content
    }

    let currentCategory = ''
    let currentTweets = []

    for (const line of lines) {
      const trimmed = line.trim()

      if (trimmed.startsWith('Generated:')) {
        result.generated = trimmed.replace('Generated:', '').trim()
      } else if (trimmed.startsWith('===') || trimmed.startsWith('---')) {
        // Save previous category
        if (currentCategory && currentTweets.length > 0) {
          result.categories[currentCategory] = currentTweets
        }
        currentCategory = trimmed.replace(/^[-=]+\s*|[-=]+$/g, '').trim()
        currentTweets = []
      } else if (trimmed.startsWith('@')) {
        // Parse tweet: @author | time
        const parts = trimmed.split('|')
        const author = parts[0].trim()
        const created_at = parts[1]?.trim() || ''
        
        currentTweets.push({
          author,
          created_at,
          text: '',
          retweet_count: 0,
          like_count: 0
        })
      } else if (trimmed && currentTweets.length > 0 && !trimmed.startsWith('RT:') && !trimmed.startsWith('LIKE:')) {
        // This is the tweet text
        currentTweets[currentTweets.length - 1].text = trimmed
      } else if (trimmed.startsWith('RT:')) {
        currentTweets[currentTweets.length - 1].retweet_count = trimmed.replace('RT:', '').trim()
      } else if (trimmed.startsWith('LIKE:')) {
        currentTweets[currentTweets.length - 1].like_count = trimmed.replace('LIKE:', '').trim()
      }
    }

    // Save last category
    if (currentCategory && currentTweets.length > 0) {
      result.categories[currentCategory] = currentTweets
    }

    res.status(200).json(result)
  } catch (err) {
    // If file doesn't exist, return empty state
    res.status(200).json({
      generated: new Date().toISOString(),
      categories: {},
      raw: 'No report available. Run Twitter Tom to generate feed.',
      error: err.message
    })
  }
}
