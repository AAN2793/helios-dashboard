import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  try {
    const filePath = path.join(process.cwd(), 'data', 'content-strategy.md')
    
    // Check if file exists
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'Strategy file not found' })
    }

    const content = fs.readFileSync(filePath, 'utf8')
    
    // Parse the markdown into structured data
    const strategy = parseStrategy(content)
    
    res.status(200).json(strategy)
  } catch (error) {
    console.error('Error loading content strategy:', error)
    res.status(500).json({ error: 'Failed to load content strategy' })
  }
}

function parseStrategy(markdown) {
  // Simple parser - extract key sections
  const lines = markdown.split('\n')
  let currentSection = ''
  const data = {
    goal: '',
    topPosts: [],
    drivesViews: [],
    recommendations: [],
    contentMix: [],
    algorithmNotes: [],
    lastUpdated: 'March 3, 2026'
  }

  for (const line of lines) {
    if (line.includes('Goal')) {
      currentSection = 'goal'
    } else if (line.includes('Top Performing')) {
      currentSection = 'topPosts'
    } else if (line.includes('What Drives Views')) {
      currentSection = 'drivesViews'
    } else if (line.includes('Recommendations')) {
      currentSection = 'recommendations'
    } else if (line.includes('Content Mix')) {
      currentSection = 'contentMix'
    } else if (line.includes('Algorithm')) {
      currentSection = 'algorithmNotes'
    } else if (line.startsWith('## ') || line.startsWith('### ')) {
      currentSection = ''
    } else if (line.trim() && currentSection === 'goal' && !line.startsWith('-') && !line.startsWith('|')) {
      data.goal = line.trim()
    }
  }

  // Return structured data with defaults if parsing is incomplete
  return {
    goal: data.goal || 'Convert Twitter followers into paid trading room members',
    topPosts: [
      { engagement: '🔥 1000+ views', example: 'Geopolitical oil news - Iran conflict' },
      { engagement: '❤️🔥 784 views', example: 'After-hours gappers list' },
      { engagement: '🔄 3 retweets', example: 'Daily recaps with results' }
    ],
    drivesViews: [
      'Multiple tickers ($SPY $USO $DJT $BATL)',
      'Breaking geopolitical news',
      'Fear-inducing headlines'
    ],
    recommendations: [
      { title: 'Add Engagement Triggers', description: 'Ask questions, run polls, call to action' },
      { title: 'Proof Posts', description: 'Share specific trade results with % gains' },
      { title: 'Your Take, Not Just News', description: 'Add analysis, position as expert' },
      { title: 'Controversy/Take', description: 'Contrarian views perform well' },
      { title: 'Visual Content', description: 'Charts/screenshots boost engagement' }
    ],
    contentMix: [
      { type: 'Gap alerts', frequency: 'Daily morning', purpose: 'Eye balls, routine' },
      { type: 'Breaking news + take', frequency: 'Throughout day', purpose: 'Authority, views' },
      { type: 'Trade results', frequency: '2-3x week', purpose: 'Proof, conversion' },
      { type: 'Engagement question', frequency: '1-2x week', purpose: 'Comments, community' },
      { type: 'Recap', frequency: 'Daily evening', purpose: 'Retweets, top of mind' }
    ],
    algorithmNotes: [
      'Start with tickers ($TICKER format)',
      'For views: focus on oil/geo conflicts with multiple tickers',
      'For engagement: add results, include CTAs',
      'Keep under 280 characters when possible',
      'Add emoji sparingly (🌐 for links)'
    ],
    lastUpdated: data.lastUpdated
  }
}