# MEMORY.md - Lessons Learned

## Critical Rules

### Never Set Perplexity as Primary Model
**Date:** Feb 10, 2026

**What happened:**
- Tried to set Perplexity API as the primary model instead of a subagent
- Gateway crashed, config got stripped of all keys (API keys, tokens, channel configs)
- Lost all context and tool access

**Why it broke:**
- Perplexity is designed for web search/information retrieval, not as a general-purpose AI
- It lacks the full tool suite and model capabilities needed for agent operations
- The config structure expects subagents to be separate from the primary model

**The correct approach:**
- Perplexity: Configure as a **subagent** only, for real-time news queries
- Primary model: Keep `openrouter/minimax/minimax-m2.1` (fast, cheap, capable)
- Use Perplexity via subagent calls: "What are today's premarket movers?"

**Rule:** Perplexity is a tool, not a brain. Never set it as primary.

---

## Config Safety

### Before Editing Config
1. Backup the current config
2. Make incremental changes
3. Test one change at a time
4. Never replace the entire "agents" block at once

### Recovery Steps
If config gets corrupted:
1. Read SOUL.md and USER.md to recover context
2. Rebuild config from known-good state
3. Restart gateway: `openclaw gateway restart`
4. Verify tools work before continuing

---

*Last Updated: Feb 10, 2026*
