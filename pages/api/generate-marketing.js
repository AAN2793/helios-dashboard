export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { prompt } = req.body

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' })
  }

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://helios-dashboard-beta.vercel.app',
        'X-Title': 'Helios Marketing Generator'
      },
      body: JSON.stringify({
        model: 'google/gemma-3-4b-it:free',
        messages: [
          { role: 'user', content: prompt }
        ],
        max_tokens: 2000
      })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error?.message || 'API error')
    }

    const content = data.choices?.[0]?.message?.content || 'No content generated'

    return res.status(200).json({ content })
  } catch (error) {
    console.error('Error generating content:', error)
    return res.status(500).json({ error: error.message })
  }
}
