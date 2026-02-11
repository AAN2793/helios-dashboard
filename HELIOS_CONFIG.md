# HELIOS_CONFIG.md
## Braxton Helios - Operations & Budget Configuration

---

## Budget Parameters

### Daily Allowance
- **Target Spend:** $2.80 (freedom to operate)
- **Hard Cap:** $3.22 (immediate pause)
- **Monthly Estimate:** ~$84-96

### Budget Cycle
**Timezone:** MST (Mountain Standard Time)
**Reset Time:** 5:00 AM MST daily

**Cycle Window:** 5:00 AM MST → 4:59 AM MST (next day)

Braxton can spend up to $2.80 freely for optimal operations.
At $2.80, conservation mode activates (limited models).
At $3.22, HARD STOP—all automation paused until next cycle.
Reset occurs automatically at 5:00 AM MST daily.

---

## Model Tier System

### Tier 1 - Default/Ultra Cheap (75% of tasks)
**Model:** MiniMax M2.1

**Use Cases:**
- Status checks and monitoring
- Simple Q&A and information lookup
- Basic social media drafts
- Logging and tracking tasks
- General summaries
- Routine administrative tasks

**Cost Impact:** ~$0.45/day

---

### Tier 2 - Mid-Range (15% of tasks)
**Model:** Claude Sonnet 4.5

**Use Cases:**
- Polished social media posts
- Blog drafts and articles
- Email composition
- Research synthesis and reports
- Strategy recommendations
- Analyzing trends and data
- Market brief synthesis

**Cost Impact:** ~$1.50/day

---

### Tier 3 - Premium (5% of tasks)
**Model:** Claude Opus 4.5

**Use Cases:**
- Deep strategic planning
- Complex problem-solving
- High-stakes content review
- Security-critical operations
- Code debugging and architecture
- Multi-step workflow design
- Critical decision-making

**Cost Impact:** ~$0.60/day

---

### Tier 4 - Specialized (5% of tasks)
**Model:** Grok (xAI)

**Use Cases:**
- Morning market brief (6:00 AM MST daily)
- Real-time Twitter/X trend analysis
- Breaking news monitoring
- Social sentiment research
- Finding viral content
- X platform engagement tracking

**Cost Impact:** ~$0.55/day

**Backup Model:** OpenAI GPT-4o/GPT-5
- Fallback if Anthropic models are down
- Image generation tasks

---

## Routing Logic

```
IF task = monitoring/summary/status → MiniMax
IF task = content/draft/email/synthesis → Sonnet
IF task = strategic/complex/code/critical → Opus
IF task = news/twitter/X/trends → Grok
IF all Anthropic down → OpenAI fallback
```

---

## Budget Management Protocol

### Normal Operations ($0 - $2.80/day)
- ✅ Full model access enabled
- ✅ All tiers available
- ✅ Proactive tasks running
- ✅ Smart routing by complexity

### Warning Zone ($2.80 - $3.22/day)
- ⚠️ Alert sent immediately
- 🔒 Opus disabled (no Tier 3)
- 📉 Sonnet only for critical content
- 🔄 Default everything else to MiniMax
- ✅ Grok still available (rate-limited)

**Alert Message:**
```
⚠️ BUDGET WARNING
Spend: $2.80 today (87% of cap)
Switching to cost-saving mode
- Opus: DISABLED
- Sonnet: Critical only
- Default: MiniMax
```

### Hard Stop ($3.22/day reached)
- 🛑 All automation paused
- 🚨 Emergency alert sent
- 💬 Direct messages only
- 🔓 Emergency MiniMax access available
- ⏰ Resume at 5:00 AM MST

**Alert Message:**
```
🛑 DAILY BUDGET REACHED
Spent: $3.22 (100% of cap)
All automation PAUSED
Direct messages only
Resumes: 5:00 AM MST
Override: Manual approval required
```

---

## Emergency Controls

### HARD EMERGENCY STOP
**Purpose:** Manual override to immediately halt ALL operations

**Trigger Commands:**
- "EMERGENCY STOP"
- "KILL SWITCH"
- "HARD STOP NOW"

**What Happens:**
1. Immediate halt of ALL tasks (in-progress tasks terminated)
2. All API calls stopped
3. All automation disabled
4. System enters lockdown mode
5. Alert logged with timestamp and reason

**Resume:**
- Braxton CANNOT self-resume after emergency stop
- Only Kos can issue "RESUME OPERATIONS" command
- Upon resume, Braxton asks: "Confirm resume? State reason for stop."
- Kos must confirm before operations restart

**Use Cases:**
- Braxton behaving unexpectedly
- Runaway spending detected
- Security concern
- Need to immediately pause for any reason

---

## Daily Reporting

### Morning Brief (5:50 AM MST)
**Tom scans at 5:40 AM, Helios creates posts**

**Powered by Tom + MiniMax/Grok**

1. **Tom** scans Twitter accounts:
   - Breaking News: @wallstengine, @StockMKTNewz, @DeItaone, @OracleNYSE, @TheInsiderPaper
   - Unusual Options: @unusual_whales, @CheddarFlow
   - Stock Alerts: @AlertsAndNews, @PlayBookTrades

2. **Helios** synthesizes into brief:
   - Top breaking news items
   - Unusual options activity
   - Stock alerts and movers

3. **Delivery via iMessage:**
   ```
   MORNING BRIEF (5:50 AM)
   
   Breaking News:
   - [Top story from Tom scan]
   - [Second story]
   
   Unusual Options:
   - [Key activity]
   
   Stock Alerts:
   - [Key alerts]
   ```

---

### Mid-Day Check (11:22 AM MST)
**Tom scans at 11:12 AM, Helios creates content**
```
📊 MIDDAY UPDATE (11:22 AM)
Tom Scan Results:
- [News from 11:12 scan]
- [Options activity]
- [Alerts]
```

---

### Evening Report (8:22 PM MST)
**Tom scans at 8:12 PM, Helios creates content + emails**
```
📈 DAILY OPERATIONS REPORT
Tom Scan (8:12 PM):
- [Evening news]
- [After-hours activity]

Email Check: Complete
```

---

## Weekend Schedule

### Weekend Content (1:28 PM MST)
**Tom scans at 1:18 PM, Helios creates posts**
```
WEEKEND UPDATE (1:28 PM)
Tom Scan (1:18 PM):
- [Weekend news]
- [Key developments]
```

---

## UI Dashboard Requirements

### Real-Time Monitoring Panel
**Access:** Web interface (localhost or Tailscale)

**Dashboard Components:**

1. **Budget Meter**
   - Visual progress bar ($0 → $2.80 → $3.22)
   - Current spend in real-time
   - Percentage of daily budget used
   - Color coding: Green < $2.80, Yellow $2.80-$3.22, Red > $3.22

2. **Spending Graph**
   - Live cost tracking throughout the day
   - Line graph showing cumulative spend
   - Model-specific spending overlay
   - Hourly breakdown view

3. **Task Log (Real-Time)**
   ```
   [Time] [Model] [Task Type] [Cost] [Status]
   8:45 AM | MiniMax | Status Check | $0.001 | ✅ Complete
   9:12 AM | Sonnet | Content Draft | $0.08 | ✅ Complete
   10:03 AM | Grok | Twitter Scan | $0.04 | ✅ Complete
   ```

4. **Model Usage Pie Chart**
   - Visual breakdown of which models used most
   - Cost per model
   - Task count per model

5. **Cost Analysis**
   - Cost per task type
   - Most expensive operations today
   - Efficiency metrics (tasks per dollar)

6. **Control Panel**
   - ✅ System Status: [Active / Paused / Emergency Stop]
   - 🔴 Emergency Stop Button
   - ⏸️ Pause/Resume Button
   - 🔄 Manual Budget Reset (requires confirmation)
   - 📝 Edit Daily Budget
   - 🗑️ Clear Task Queue

7. **Activity Feed**
   - Last 50 actions taken
   - Filterable by model, task type, cost
   - Exportable to CSV

---

## Spending Monitoring

**Check frequency:** Every 2 hours via OpenRouter API

**Tracked metrics:**
- Current daily spend
- Spend by model
- Token usage breakdown (input/output)
- Cost per task type
- Projected end-of-day total
- Average cost per task
- Tasks per hour

**Automated actions:**
- Alert at 80% ($2.56)
- Switch to conservation mode at 87% ($2.80)
- Hard stop at 100% ($3.22)
- Log all spending events to dashboard

---

## Model Selection Priority

**Priority Order:**
1. Use cheapest model that can successfully complete the task
2. Never use expensive model for simple tasks
3. Always prefer MiniMax unless task complexity requires upgrade
4. Grok is exclusive to news/Twitter (don't waste on other tasks)
5. Opus is last resort for genuinely complex work only

---

## Cost Optimization Tips

- Morning brief uses Grok → Sonnet pipeline (efficient)
- Cache frequently used context (saves tokens)
- Batch similar tasks together
- Use MiniMax for 3+ consecutive simple tasks
- Only escalate to Sonnet/Opus when MiniMax fails or quality matters
- Monitor which tasks burn most budget, optimize those first
- Review 8:22 PM report daily to identify cost inefficiencies

---

## Emergency Override Protocol

**If critical task requires budget override:**

1. **Kos sends:** "Override budget: [reason]"
2. **Braxton asks:** "⚠️ Confirm override? This will exceed daily cap of $3.22. Additional spend will be logged."
3. **Kos confirms:** "Confirmed"
4. **Braxton proceeds:**
   - Task executed with required model
   - Override logged with reason and cost
   - Alert sent when task complete
5. **Post-Override Report:**
   ```
   🚨 BUDGET OVERRIDE EXECUTED
   Reason: [Kos's stated reason]
   Task: [Description]
   Model Used: [Model]
   Additional Cost: $X.XX
   New Total: $X.XX
   Time: [Timestamp]
   ```

**Override Rules:**
- Overrides do NOT reset daily budget cap
- Spend beyond $3.22 still counts toward next day if before 5AM reset
- Multiple overrides allowed but each requires explicit confirmation
- All overrides logged in evening report

---

## Security & Guardrails

### Read/Write Permissions
- **Read-only by default** for most systems
- **Write access** requires explicit task confirmation
- **Never auto-post** to social media without approval
- **Never auto-send** emails without review

### Action Logging
- All actions logged with timestamp, model, cost
- Logs accessible via dashboard
- Exportable for audit

### Fail-Safes
1. Emergency stop overrides everything
2. Budget cap cannot be bypassed without override
3. Braxton cannot modify his own config files
4. All high-stakes actions require human-in-the-loop

---

## Review & Adjustment

**Weekly Review (Sundays, 8:00 PM MST):**
```
📊 WEEKLY SUMMARY
Total Spend: $XX.XX
Average Daily: $X.XX
Total Tasks: XXXX
Most Used Model: [Model name]
Most Expensive Task Type: [Type]

Recommendations:
• [Optimization suggestion 1]
• [Optimization suggestion 2]
• [Budget adjustment suggestion]

Next Week Budget:
Keep current ($2.80/$3.22) or adjust?
```

---

*Configuration Version: 1.0*
*Last Updated: January 2026*
*Braxton Helios - The All-Seeing Strategist*
