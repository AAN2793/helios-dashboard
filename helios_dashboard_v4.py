import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import time

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HELIOS COMMAND | Enterprise Dashboard",
    layout="wide",
    page_icon=None,
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# COLOR PALETTE - BLOOMBERG TERMINAL STYLE
# -----------------------------------------------------------------------------
COLORS = {
    'bg_primary': '#0a0a0a',
    'bg_secondary': '#141414',
    'bg_card': '#1a1a1a',
    'bg_header': '#0d1b2a',
    'text_primary': '#e8e8e8',
    'text_secondary': '#7d8590',
    'text_muted': '#4a4a4a',
    'accent_blue': '#00b4d8',
    'accent_cyan': '#00d4ff',
    'accent_green': '#00c853',
    'accent_green_dim': '#008f39',
    'accent_red': '#ff3838',
    'accent_orange': '#ff9500',
    'accent_yellow': '#ffd600',
    'border': '#2a2a2a',
    'grid': '#1f1f1f'
}

# -----------------------------------------------------------------------------
# ENTERPRISE CSS - ZERO EMOJIS, PROFESSIONAL TERMINAL STYLE
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Typography */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: {COLORS['text_primary']} !important;
        text-transform: uppercase;
        font-size: 0.85rem;
    }}
    
    h1 {{ font-size: 1.1rem; border-bottom: 1px solid {COLORS['border']}; padding-bottom: 8px; }}
    h2 {{ font-size: 0.9rem; color: {COLORS['text_secondary']} !important; }}
    h3 {{ font-size: 0.8rem; }}
    
    /* Data Font - Monospace for numbers */
    .data-text {{
        font-family: 'JetBrains Mono', monospace;
        font-variant-numeric: tabular-nums;
    }}
    
    /* Header Bar */
    .terminal-header {{
        background: linear-gradient(90deg, {COLORS['bg_header']} 0%, {COLORS['bg_secondary']} 100%);
        border-bottom: 2px solid {COLORS['accent_blue']};
        padding: 12px 20px;
        margin: -80px -80px 20px -80px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .terminal-brand {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.2rem;
        color: {COLORS['accent_cyan']};
        letter-spacing: 2px;
    }}
    
    .terminal-status {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: {COLORS['text_secondary']};
    }}
    
    /* Cards */
    .metric-card {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 0;
        padding: 16px;
        height: 100%;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['accent_blue']};
    }}
    
    .metric-label {{
        font-size: 0.65rem;
        text-transform: uppercase;
        color: {COLORS['text_secondary']};
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    
    .metric-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        color: {COLORS['text_primary']};
    }}
    
    .metric-change {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        margin-top: 4px;
    }}
    
    .positive {{ color: {COLORS['accent_green']}; }}
    .negative {{ color: {COLORS['accent_red']}; }}
    .neutral {{ color: {COLORS['text_muted']}; }}
    .warning {{ color: {COLORS['accent_orange']}; }}
    
    /* Progress Bars */
    .progress-container {{
        background-color: {COLORS['bg_secondary']};
        height: 8px;
        width: 100%;
        position: relative;
    }}
    
    .progress-fill {{
        height: 100%;
        transition: width 0.3s ease;
    }}
    
    .progress-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: {COLORS['text_secondary']};
        margin-top: 4px;
        display: flex;
        justify-content: space-between;
    }}
    
    /* Tables */
    .stDataFrame {{
        background-color: {COLORS['bg_card']};
    }}
    
    /* Status Indicators */
    .status-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-active {{ background-color: {COLORS['accent_green']}; box-shadow: 0 0 6px {COLORS['accent_green']}; }}
    .status-idle {{ background-color: {COLORS['accent_orange']}; }}
    .status-stopped {{ background-color: {COLORS['accent_red']}; }}
    .status-standby {{ background-color: {COLORS['accent_blue']}; }}
    
    /* Agent Cards */
    .agent-panel {{
        background-color: {COLORS['bg_card']};
        border-left: 3px solid {COLORS['border']};
        padding: 12px 16px;
        margin: 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
    }}
    
    .agent-panel:hover {{
        background-color: {COLORS['bg_secondary']};
    }}
    
    .agent-name {{
        color: {COLORS['text_primary']};
        font-weight: 600;
    }}
    
    .agent-meta {{
        color: {COLORS['text_secondary']};
        margin-top: 4px;
    }}
    
    /* Task Queue Items */
    .task-item {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        padding: 12px;
        margin: 4px 0;
        cursor: grab;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .task-item:hover {{
        border-color: {COLORS['accent_blue']};
        background-color: {COLORS['bg_secondary']};
    }}
    
    .task-priority-high {{ border-left: 3px solid {COLORS['accent_red']}; }}
    .task-priority-med {{ border-left: 3px solid {COLORS['accent_orange']}; }}
    .task-priority-low {{ border-left: 3px solid {COLORS['accent_green']}; }}
    
    /* Section Dividers */
    .section-header {{
        background-color: {COLORS['bg_secondary']};
        border-left: 3px solid {COLORS['accent_blue']};
        padding: 8px 12px;
        margin: 16px 0 8px 0;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {COLORS['text_secondary']};
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {COLORS['bg_card']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 8px 16px;
    }}
    
    .stButton>button:hover {{
        background-color: {COLORS['accent_blue']};
        border-color: {COLORS['accent_blue']};
        color: {COLORS['bg_primary']};
    }}
    
    .export-btn {{
        background-color: {COLORS['accent_green_dim']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    
    /* Streamlit Overrides */
    .css-1d391kg, .css-1lcbmhc {{
        background-color: {COLORS['bg_primary']};
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COLORS['bg_secondary']};
        gap: 0;
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {COLORS['text_secondary']};
        border-radius: 0;
        padding: 12px 24px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['bg_card']};
        color: {COLORS['accent_cyan']};
        border-top: 2px solid {COLORS['accent_cyan']};
        border-bottom: 1px solid {COLORS['accent_cyan']};
    }}
    
    .streamlit-expanderHeader {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {COLORS['text_secondary']};
        background-color: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
    }}
    
    /* Footer */
    .terminal-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: {COLORS['bg_header']};
        border-top: 1px solid {COLORS['border']};
        padding: 8px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: {COLORS['text_muted']};
        display: flex;
        justify-content: space-between;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="terminal-header">
    <div class="terminal-brand">HELIOS COMMAND</div>
    <div class="terminal-status">
        SYS: ONLINE | LATENCY: 12ms | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
CONFIG_PATH = Path('HELIOS_CONFIG.json')
MEMORY_TODOS = Path('memory') / 'todos.md'
MEMORY_IDEAS = Path('memory') / 'ideas.md'
MEMORY_SUBAGENTS = Path('memory') / 'subagents.md'
MEMORY_PATH = Path('memory')
MEMORY_PATH.mkdir(exist_ok=True)

def load_memory(file):
    """Load memory file content."""
    if file.exists():
        try:
            with open(file, 'r') as f:
                content = f.read().strip()
                return [line.strip() for line in content.split('\n') if line.strip()]
        except:
            pass
    return []

def get_system_metrics():
    """Generate realistic system metrics."""
    return {
        'active_agents': 4,
        'agents_delta': 1,
        'tasks_today': 12,
        'tasks_delta': 3,
        'cost_today': 0.89,
        'cost_delta': -0.12,
        'subagents_active': 2,
        'subagents_delta': 1,
        'budget_used': 45.2,
        'budget_total': 100.00,
        'api_calls': 1247,
        'api_delta': 89,
        'uptime_hours': 72.5
    }

def get_task_queue():
    """Generate task queue data."""
    return [
        {'id': 1, 'task': 'Morning market brief', 'assigned': 'Sonnet-Writer', 'status': 'PENDING', 'priority': 'HIGH', 'eta': '09:30'},
        {'id': 2, 'task': 'Monitor NVDA position', 'assigned': 'MiniMax-Cheap', 'status': 'ACTIVE', 'priority': 'MED', 'eta': 'LIVE'},
        {'id': 3, 'task': 'Build earnings scraper', 'assigned': 'Codex-Builder', 'status': 'QUEUED', 'priority': 'HIGH', 'eta': '10:00'},
        {'id': 4, 'task': 'Portfolio rebalancing', 'assigned': 'Kimi-Main', 'status': 'QUEUED', 'priority': 'MED', 'eta': '11:00'},
        {'id': 5, 'task': 'Weekly cost analysis', 'assigned': 'Auto', 'status': 'QUEUED', 'priority': 'LOW', 'eta': '14:00'},
    ]

def get_subagent_status():
    """Generate subagent status data."""
    return [
        {
            'name': 'Kimi-Main',
            'role': 'COORDINATOR',
            'model': 'Kimi-K2.5',
            'status': 'ACTIVE',
            'tasks_completed': 47,
            'cost_total': 0.94,
            'last_active': '2m ago',
            'cpu_usage': 23
        },
        {
            'name': 'Codex-Builder',
            'role': 'DEVELOPER',
            'model': 'GPT-5.1-Codex',
            'status': 'ACTIVE',
            'tasks_completed': 12,
            'cost_total': 0.36,
            'last_active': 'NOW',
            'cpu_usage': 67
        },
        {
            'name': 'Sonnet-Writer',
            'role': 'CONTENT',
            'model': 'Claude-Sonnet-4',
            'status': 'STANDBY',
            'tasks_completed': 8,
            'cost_total': 0.64,
            'last_active': '15m ago',
            'cpu_usage': 0
        },
        {
            'name': 'MiniMax-Cheap',
            'role': 'MONITOR',
            'model': 'MiniMax-M2.1',
            'status': 'ACTIVE',
            'tasks_completed': 89,
            'cost_total': 0.09,
            'last_active': 'NOW',
            'cpu_usage': 12
        }
    ]

def get_cost_history():
    """Generate cost history for charts."""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    costs = np.random.normal(0.85, 0.25, 30)
    costs = np.maximum(costs, 0.2)  # No negative costs
    return pd.DataFrame({
        'date': dates,
        'cost': costs,
        'cumulative': np.cumsum(costs)
    })

def get_api_usage():
    """Generate API usage breakdown."""
    return pd.DataFrame({
        'model': ['Kimi-K2.5', 'GPT-5.1-Codex', 'Claude-Sonnet-4', 'MiniMax-M2.1'],
        'calls': [423, 89, 156, 579],
        'cost': [0.94, 0.36, 0.64, 0.09],
        'avg_latency': [890, 1200, 750, 320]
    })

# -----------------------------------------------------------------------------
# METRICS ROW
# -----------------------------------------------------------------------------
metrics = get_system_metrics()

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Agents</div>
        <div class="metric-value">{metrics['active_agents']}</div>
        <div class="metric-change positive">+{metrics['agents_delta']} today</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Tasks Today</div>
        <div class="metric-value">{metrics['tasks_today']}</div>
        <div class="metric-change positive">+{metrics['tasks_delta']} this hr</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    cost_class = "positive" if metrics['cost_delta'] < 0 else "negative"
    delta_sign = "" if metrics['cost_delta'] < 0 else "+"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Cost Today</div>
        <div class="metric-value">${metrics['cost_today']:.2f}</div>
        <div class="metric-change {cost_class}">{delta_sign}${metrics['cost_delta']:.2f} vs yest</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Workers</div>
        <div class="metric-value">{metrics['subagents_active']}</div>
        <div class="metric-change positive">+{metrics['subagents_delta']} spawned</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">API Calls</div>
        <div class="metric-value">{metrics['api_calls']:,}</div>
        <div class="metric-change positive">+{metrics['api_delta']} this hr</div>
    </div>
    """, unsafe_allow_html=True)

with m6:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Uptime</div>
        <div class="metric-value">{metrics['uptime_hours']:.1f}h</div>
        <div class="metric-change neutral">99.9% SLA</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BUDGET METER SECTION
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>Budget Utilization</div>", unsafe_allow_html=True)

budget_pct = (metrics['budget_used'] / metrics['budget_total']) * 100
budget_color = COLORS['accent_green'] if budget_pct < 50 else COLORS['accent_orange'] if budget_pct < 75 else COLORS['accent_red']

b1, b2, b3 = st.columns([2, 1, 1])

with b1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Daily Budget Consumption</div>
        <div class="progress-container">
            <div class="progress-fill" style="width: {budget_pct}%; background-color: {budget_color};"></div>
        </div>
        <div class="progress-label">
            <span>${metrics['budget_used']:.2f} used</span>
            <span>{budget_pct:.1f}%</span>
            <span>${metrics['budget_total']:.2f} limit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with b2:
    daily_remaining = metrics['budget_total'] - metrics['budget_used']
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Remaining Today</div>
        <div class="metric-value positive">${daily_remaining:.2f}</div>
        <div class="metric-change">Est. 4.2 hrs left</div>
    </div>
    """, unsafe_allow_html=True)

with b3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Monthly Projection</div>
        <div class="metric-value">$24.50</div>
        <div class="metric-change positive">Under budget</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN CONTENT GRID
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 2])

# -----------------------------------------------------------------------------
# LEFT COLUMN: SUBAGENT ACTIVITY PANEL
# -----------------------------------------------------------------------------
with left_col:
    st.markdown("<div class='section-header'>Subagent Activity</div>", unsafe_allow_html=True)
    
    agents = get_subagent_status()
    
    for agent in agents:
        status_class = "status-active" if agent['status'] == 'ACTIVE' else "status-standby" if agent['status'] == 'STANDBY' else "status-idle"
        
        st.markdown(f"""
        <div class="agent-panel">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="agent-name">{agent['name']}</span>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.65rem;">{agent['role']}</span>
            </div>
            <div class="agent-meta">
                <span class="status-dot {status_class}"></span>{agent['status']} | {agent['last_active']}
            </div>
            <div style="margin-top: 8px; display: flex; justify-content: space-between; color: {COLORS['text_muted']};">
                <span>Tasks: {agent['tasks_completed']}</span>
                <span>Cost: ${agent['cost_total']:.2f}</span>
                <span>CPU: {agent['cpu_usage']}%</span>
            </div>
            <div style="margin-top: 4px; font-size: 0.6rem; color: {COLORS['text_muted']};">
                {agent['model']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Export buttons
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("EXPORT CSV", key="export_csv_agents"):
            df_agents = pd.DataFrame(agents)
            csv = df_agents.to_csv(index=False)
            st.download_button(
                label="DOWNLOAD CSV",
                data=csv,
                file_name=f"helios_agents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    with col_exp2:
        if st.button("EXPORT PDF", key="export_pdf_agents"):
            st.info("PDF export: Install reportlab for full support")

# -----------------------------------------------------------------------------
# RIGHT COLUMN: TABS FOR TASKS, CHARTS, DATA
# -----------------------------------------------------------------------------
with right_col:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Task Queue",
        "Cost Analytics", 
        "API Metrics",
        "System Logs"
    ])
    
    # TAB 1: TASK QUEUE
    with tab1:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Queue controls
        qc1, qc2, qc3 = st.columns([1, 1, 2])
        with qc1:
            st.button("ADD TASK", key="add_task_btn")
        with qc2:
            st.button("CLEAR COMPLETED", key="clear_completed")
        with qc3:
            st.text_input("Filter", placeholder="Search tasks...", label_visibility="collapsed")
        
        # Task list
        tasks = get_task_queue()
        
        for task in tasks:
            priority_class = f"task-priority-{task['priority'].lower()[:3]}"
            status_color = COLORS['accent_green'] if task['status'] == 'ACTIVE' else COLORS['accent_blue'] if task['status'] == 'QUEUED' else COLORS['accent_orange']
            
            st.markdown(f"""
            <div class="task-item {priority_class}">
                <div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: {COLORS['text_primary']};">
                        {task['task']}
                    </div>
                    <div style="font-size: 0.65rem; color: {COLORS['text_secondary']}; margin-top: 2px;">
                        Assigned: {task['assigned']} | ETA: {task['eta']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: {status_color}; font-weight: 600;">
                        {task['status']}
                    </div>
                    <div style="font-size: 0.6rem; color: {COLORS['text_muted']}; margin-top: 2px;">
                        PR:{task['priority'][:1]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Task stats
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        active_count = sum(1 for t in tasks if t['status'] == 'ACTIVE')
        pending_count = sum(1 for t in tasks if t['status'] == 'PENDING')
        queued_count = sum(1 for t in tasks if t['status'] == 'QUEUED')
        
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Active", active_count)
        s2.metric("Pending", pending_count)
        s3.metric("Queued", queued_count)
        s4.metric("Total", len(tasks))
    
    # TAB 2: COST ANALYTICS
    with tab2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Cost history chart
        cost_df = get_cost_history()
        
        fig_cost = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Cost (30 Days)', 'Cumulative Cost'),
            vertical_spacing=0.15
        )
        
        fig_cost.add_trace(
            go.Bar(
                x=cost_df['date'].dt.strftime('%m-%d'),
                y=cost_df['cost'],
                marker_color=COLORS['accent_blue'],
                name='Daily'
            ),
            row=1, col=1
        )
        
        fig_cost.add_trace(
            go.Scatter(
                x=cost_df['date'].dt.strftime('%m-%d'),
                y=cost_df['cumulative'],
                mode='lines',
                line=dict(color=COLORS['accent_green'], width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 200, 83, 0.1)',
                name='Cumulative'
            ),
            row=2, col=1
        )
        
        fig_cost.update_layout(
            plot_bgcolor=COLORS['bg_card'],
            paper_bgcolor=COLORS['bg_primary'],
            font=dict(family='JetBrains Mono', color=COLORS['text_secondary'], size=10),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            height=500
        )
        
        fig_cost.update_xaxes(showgrid=True, gridcolor=COLORS['grid'], tickfont=dict(size=8))
        fig_cost.update_yaxes(showgrid=True, gridcolor=COLORS['grid'], tickprefix='$', tickfont=dict(size=8))
        
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Export cost data
        col_c1, col_c2 = st.columns([4, 1])
        with col_c2:
            csv_cost = cost_df.to_csv(index=False)
            st.download_button(
                label="EXPORT COST DATA",
                data=csv_cost,
                file_name=f"cost_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # TAB 3: API METRICS
    with tab3:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        api_df = get_api_usage()
        
        # API usage chart
        fig_api = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Calls by Model', 'Cost by Model'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        fig_api.add_trace(
            go.Bar(
                x=api_df['model'],
                y=api_df['calls'],
                marker_color=[COLORS['accent_blue'], COLORS['accent_cyan'], COLORS['accent_green'], COLORS['accent_orange']],
                text=api_df['calls'],
                textposition='outside',
                textfont=dict(size=10, color=COLORS['text_secondary'])
            ),
            row=1, col=1
        )
        
        fig_api.add_trace(
            go.Pie(
                labels=api_df['model'],
                values=api_df['cost'],
                hole=0.5,
                marker=dict(colors=[COLORS['accent_blue'], COLORS['accent_cyan'], COLORS['accent_green'], COLORS['accent_orange']]),
                textinfo='percent',
                textfont=dict(size=9, color=COLORS['text_primary'])
            ),
            row=1, col=2
        )
        
        fig_api.update_layout(
            plot_bgcolor=COLORS['bg_card'],
            paper_bgcolor=COLORS['bg_primary'],
            font=dict(family='JetBrains Mono', color=COLORS['text_secondary'], size=10),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            height=350
        )
        
        fig_api.update_xaxes(tickangle=45, tickfont=dict(size=8))
        
        st.plotly_chart(fig_api, use_container_width=True)
        
        # API metrics table
        st.markdown("<div class='section-header'>API Performance</div>", unsafe_allow_html=True)
        
        api_display = api_df.copy()
        api_display['cost'] = api_display['cost'].apply(lambda x: f"${x:.2f}")
        api_display['avg_latency'] = api_display['avg_latency'].apply(lambda x: f"{x}ms")
        api_display.columns = ['Model', 'Calls', 'Cost', 'Avg Latency']
        
        st.dataframe(
            api_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Model': st.column_config.TextColumn('MODEL', width='medium'),
                'Calls': st.column_config.NumberColumn('CALLS', width='small'),
                'Cost': st.column_config.TextColumn('COST', width='small'),
                'Avg Latency': st.column_config.TextColumn('LATENCY', width='small')
            }
        )
    
    # TAB 4: SYSTEM LOGS
    with tab4:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Generate log entries
        logs = [
            {'timestamp': '2026-02-02 22:21:03', 'level': 'INFO', 'component': 'Codex-Builder', 'message': 'Task completed: Built trading_journal.py'},
            {'timestamp': '2026-02-02 22:18:45', 'level': 'INFO', 'component': 'MiniMax-Cheap', 'message': 'Monitoring NVDA @ $120.50'},
            {'timestamp': '2026-02-02 22:15:22', 'level': 'WARN', 'component': 'Kimi-Main', 'message': 'High API latency detected: 1200ms'},
            {'timestamp': '2026-02-02 22:12:00', 'level': 'INFO', 'component': 'Sonnet-Writer', 'message': 'Standby mode activated'},
            {'timestamp': '2026-02-02 22:08:33', 'level': 'INFO', 'component': 'System', 'message': 'Subagent spawned: Codex-Builder'},
            {'timestamp': '2026-02-02 22:05:12', 'level': 'ERROR', 'component': 'Scheduler', 'message': 'Task timeout: retry scheduled'},
            {'timestamp': '2026-02-02 22:00:00', 'level': 'INFO', 'component': 'System', 'message': 'Daily budget reset: $100.00'},
            {'timestamp': '2026-02-02 21:45:22', 'level': 'INFO', 'component': 'MiniMax-Cheap', 'message': 'Batch processing: 47 alerts'},
        ]
        
        for log in logs:
            level_color = COLORS['accent_green'] if log['level'] == 'INFO' else COLORS['accent_orange'] if log['level'] == 'WARN' else COLORS['accent_red']
            
            st.markdown(f"""
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.7rem;
                padding: 6px 0;
                border-bottom: 1px solid {COLORS['border']};
                display: flex;
                gap: 12px;
            ">
                <span style="color: {COLORS['text_muted']}; width: 140px;">{log['timestamp']}</span>
                <span style="color: {level_color}; width: 50px; font-weight: 600;">{log['level']}</span>
                <span style="color: {COLORS['accent_blue']}; width: 120px;">{log['component']}</span>
                <span style="color: {COLORS['text_secondary']};">{log['message']}</span>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# COLLAPSIBLE PANELS SECTION
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>System Configuration & Memory</div>", unsafe_allow_html=True)

c_col1, c_col2 = st.columns(2)

with c_col1:
    with st.expander("ACTIVE MODELS", expanded=False):
        models = [
            {'name': 'Kimi-K2.5', 'provider': 'Moonshot AI', 'role': 'Primary / Coordinator', 'cost_per_1k': '$0.003'},
            {'name': 'GPT-5.1-Codex', 'provider': 'OpenAI', 'role': 'Code Development', 'cost_per_1k': '$0.004'},
            {'name': 'Claude-Sonnet-4', 'provider': 'Anthropic', 'role': 'Content / Analysis', 'cost_per_1k': '$0.008'},
            {'name': 'MiniMax-M2.1', 'provider': 'MiniMax', 'role': 'Monitoring / Simple', 'cost_per_1k': '$0.0005'},
        ]
        
        for m in models:
            st.markdown(f"""
            <div style="padding: 8px 0; border-bottom: 1px solid {COLORS['border']}; font-size: 0.75rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: {COLORS['text_primary']}; font-weight: 600;">{m['name']}</span>
                    <span style="color: {COLORS['text_muted']};">{m['cost_per_1k']}/1K</span>
                </div>
                <div style="color: {COLORS['text_secondary']}; margin-top: 2px;">
                    {m['provider']} | {m['role']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("TODO ITEMS", expanded=False):
        todos = load_memory(MEMORY_TODOS)
        if todos:
            for i, todo in enumerate(todos[:10]):
                st.checkbox(todo, key=f"todo_v4_{i}")
        else:
            st.markdown(f"""
            <div style="color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 8px;">
                No active todos
            </div>
            """, unsafe_allow_html=True)
        
        new_todo = st.text_input("Add task", placeholder="Enter new task...", label_visibility="collapsed")
        if st.button("ADD", key="add_todo_v4") and new_todo:
            with open(MEMORY_TODOS, 'a') as f:
                f.write(f"\n{new_todo}")
            st.rerun()

with c_col2:
    with st.expander("SYSTEM HEALTH", expanded=False):
        health_metrics = [
            ('CPU', 34, COLORS['accent_green']),
            ('Memory', 67, COLORS['accent_orange']),
            ('Disk', 42, COLORS['accent_green']),
            ('Network', 12, COLORS['accent_green']),
        ]
        
        for name, val, color in health_metrics:
            st.markdown(f"""
            <div style="margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 4px;">
                    <span style="color: {COLORS['text_secondary']};">{name}</span>
                    <span style="color: {COLORS['text_primary']};">{val}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill" style="width: {val}%; background-color: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("IDEAS & BACKLOG", expanded=False):
        ideas = load_memory(MEMORY_IDEAS)
        if ideas:
            for idea in ideas[:10]:
                st.markdown(f"""
                <div style="padding: 6px 0; border-bottom: 1px solid {COLORS['border']}; 
                            font-size: 0.7rem; color: {COLORS['text_secondary']};">
                    [{datetime.now().strftime('%Y-%m-%d')}] {idea}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 8px;">
                No backlog items
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STOCK HOLDINGS PANEL (Collapsible)
# -----------------------------------------------------------------------------
with st.expander("PORTFOLIO HOLDINGS", expanded=True):
    stocks_data = {
        'Symbol': ['NVDA', 'PEP', 'WMT', 'BTI', 'TSLA', 'MSFT'],
        'Qty': [100, 50, 75, 200, 25, 40],
        'Price': [120.50, 170.80, 75.40, 35.20, 245.30, 420.15],
        'Change': [2.1, 0.8, -0.5, 1.3, -3.2, 1.5],
        'ROIC': ['25.4%', '18.2%', '12.1%', '8.5%', '15.3%', '22.8%'],
        'PE': ['35.2', '22.1', '28.3', '12.4', '65.2', '32.1'],
        'Value': [12050, 8540, 5655, 7040, 6132.50, 16806]
    }
    
    df_stocks = pd.DataFrame(stocks_data)
    df_stocks['Day P&L'] = df_stocks['Qty'] * df_stocks['Change']
    total_value = df_stocks['Value'].sum()
    total_pnl = df_stocks['Day P&L'].sum()
    
    # Portfolio summary
    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Total Value", f"${total_value:,.2f}")
    with p2:
        pnl_class = "positive" if total_pnl > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Day P&L</div>
            <div class="metric-value {pnl_class}">${total_pnl:+,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.metric("Positions", len(df_stocks))
    
    # Holdings table
    st.dataframe(
        df_stocks,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Symbol': st.column_config.TextColumn('SYMBOL', width='small'),
            'Qty': st.column_config.NumberColumn('QTY', width='small'),
            'Price': st.column_config.NumberColumn('PRICE', format='$%.2f', width='small'),
            'Change': st.column_config.Number_column('CHG', format='%+.2f', width='small'),
            'ROIC': st.column_config.TextColumn('ROIC', width='small'),
            'PE': st.column_config.TextColumn('P/E', width='small'),
            'Value': st.column_config.NumberColumn('VALUE', format='$%,.0f', width='medium'),
            'Day P&L': st.column_config.Number_column('P&L', format='%+,.2f', width='small')
        }
    )
    
    # Export holdings
    col_h1, col_h2 = st.columns([6, 1])
    with col_h2:
        csv_holdings = df_stocks.to_csv(index=False)
        st.download_button(
            label="EXPORT HOLDINGS",
            data=csv_holdings,
            file_name=f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: {COLORS['bg_header']};
    border-top: 1px solid {COLORS['border']};
    padding: 8px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: {COLORS['text_muted']};
    display: flex;
    justify-content: space-between;
    z-index: 999;
">
    <span>HELIOS v4.0 | Enterprise Dashboard</span>
    <span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</span>
    <span>Build 2026.02.02-RC1</span>
</div>
""", unsafe_allow_html=True)

# Add padding at bottom for fixed footer
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
