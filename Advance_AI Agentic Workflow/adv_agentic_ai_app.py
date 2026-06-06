import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from datetime import datetime, timedelta
import json
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic AI Platform | Tata Group",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --tata-blue: #003366;
    --tata-gold: #C8A951;
    --accent-cyan: #00D4FF;
    --accent-green: #00E676;
    --accent-orange: #FF6B35;
    --accent-purple: #7C4DFF;
    --bg-dark: #0A0E1A;
    --bg-card: #111827;
    --bg-card2: #1a2235;
    --text-primary: #E8EDF5;
    --text-secondary: #8B9BB4;
    --border: rgba(200,169,81,0.25);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-primary);
}

.main { background: var(--bg-dark); }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* HEADER */
.hero-header {
    background: linear-gradient(135deg, #003366 0%, #0A0E1A 50%, #001a33 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(0,212,255,0.06) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(200,169,81,0.06) 0%, transparent 60%);
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 1px;
    margin: 0;
}
.hero-subtitle {
    color: var(--tata-gold);
    font-size: 1rem;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.hero-desc { color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem; }

/* METRIC CARDS */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--tata-gold);
}
.metric-label { color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

/* AGENT CARDS */
.agent-card {
    background: var(--bg-card2);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.agent-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent-cyan);
}
.agent-status { font-size: 0.82rem; color: var(--text-secondary); }

/* STATUS BADGES */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-success { background: rgba(0,230,118,0.15); color: #00E676; border: 1px solid rgba(0,230,118,0.3); }
.badge-warning { background: rgba(255,167,38,0.15); color: #FFA726; border: 1px solid rgba(255,167,38,0.3); }
.badge-info    { background: rgba(0,212,255,0.15); color: #00D4FF; border: 1px solid rgba(0,212,255,0.3); }
.badge-purple  { background: rgba(124,77,255,0.15); color: #B39DDB; border: 1px solid rgba(124,77,255,0.3); }
.badge-orange  { background: rgba(255,107,53,0.15); color: #FF6B35; border: 1px solid rgba(255,107,53,0.3); }

/* SECTION HEADERS */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--tata-gold);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

/* WORKFLOW STEP */
.workflow-step {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.step-num {
    background: var(--tata-blue);
    color: var(--tata-gold);
    border-radius: 50%;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
}

/* TABLE STYLING */
.styled-table { width: 100%; border-collapse: collapse; }
.styled-table th {
    background: var(--tata-blue);
    color: var(--tata-gold);
    padding: 0.7rem 1rem;
    text-align: left;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.styled-table td { padding: 0.6rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.88rem; }
.styled-table tr:hover td { background: rgba(255,255,255,0.03); }

/* PROGRESS BAR */
.progress-container { background: rgba(255,255,255,0.08); border-radius: 4px; height: 8px; }
.progress-fill { height: 8px; border-radius: 4px; background: linear-gradient(90deg, var(--tata-blue), var(--accent-cyan)); }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, var(--tata-blue), #0055aa) !important;
    color: white !important;
    border: 1px solid var(--tata-gold) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #0055aa, var(--accent-cyan)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(0,212,255,0.3) !important;
}

/* SELECTBOX, INPUT */
.stSelectbox>div>div, .stTextInput>div>div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 7px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--tata-blue) !important;
    color: var(--tata-gold) !important;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--tata-gold) !important;
    font-family: 'Rajdhani', sans-serif !important;
}
div.stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPER: animated progress
# ─────────────────────────────────────────────
def run_agents(agents: list, delay: float = 0.5):
    """Show animated agent execution with a progress bar."""
    bar = st.progress(0)
    status = st.empty()
    results = []
    for i, (name, fn) in enumerate(agents):
        status.markdown(f"<div class='agent-card'><div class='agent-name'>⚙️ {name}</div>"
                        f"<div class='agent-status'>Running...</div></div>", unsafe_allow_html=True)
        time.sleep(delay)
        result = fn()
        results.append(result)
        bar.progress(int((i + 1) / len(agents) * 100))
    status.empty()
    bar.empty()
    return results


def card(title, content, color="var(--accent-cyan)"):
    st.markdown(f"""
    <div style="background:var(--bg-card2);border-left:3px solid {color};
                border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.8rem;">
      <div style="font-family:Rajdhani,sans-serif;font-size:1rem;font-weight:600;color:{color};">{title}</div>
      <div style="color:var(--text-secondary);font-size:0.88rem;margin-top:0.4rem;line-height:1.6;">{content}</div>
    </div>""", unsafe_allow_html=True)


def section(title):
    st.markdown(f"<div class='section-header'>{title}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 1.5rem;">
      <div style="font-family:Rajdhani,sans-serif;font-size:1.6rem;font-weight:700;color:#C8A951;">TATA GROUP</div>
      <div style="font-size:0.75rem;color:#8B9BB4;letter-spacing:2px;text-transform:uppercase;">Agentic AI Platform</div>
    </div>""", unsafe_allow_html=True)

    use_case = st.selectbox("🎯 Select Use Case", [
        "🎓 Learning & Development",
        "🧑‍💼 Recruitment",
        "🖥️ IT Service Desk",
        "🛒 Procurement",
        "🌴 Leave Management",
    ])

    st.markdown("---")
    st.markdown("<div style='color:var(--tata-gold);font-weight:600;font-size:0.85rem;'>👤 EMPLOYEE INFO</div>", unsafe_allow_html=True)
    emp_name = st.text_input("Name", "Arjun Sharma")
    emp_id   = st.text_input("Employee ID", "TCS-2024-0891")
    dept     = st.selectbox("Department", ["Engineering", "Finance", "HR", "Operations", "Marketing"])
    level    = st.selectbox("Level", ["Junior", "Mid", "Senior", "Lead", "Manager"])

    st.markdown("---")
    st.markdown("<div style='color:var(--tata-gold);font-weight:600;font-size:0.85rem;'>⚙️ AGENT SETTINGS</div>", unsafe_allow_html=True)
    exec_speed = st.slider("Execution Speed", 0.1, 1.5, 0.4, 0.1)
    show_timeline = st.checkbox("Show Agent Timeline", True)
    show_reasoning = st.checkbox("Show Agent Reasoning", True)

    st.markdown("---")
    st.markdown("<div style='color:var(--text-secondary);font-size:0.75rem;text-align:center;'>v2.0 · Powered by Multi-Agent AI<br>© 2025 Tata Group</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
case_icon = use_case.split()[0]
case_name = " ".join(use_case.split()[1:])

st.markdown(f"""
<div class="hero-header">
  <div class="hero-subtitle">Agentic AI · Autonomous Workflows</div>
  <div class="hero-title">{case_icon} {case_name} Intelligence System</div>
  <div class="hero-desc">
    Employee: <strong>{emp_name}</strong> · ID: <strong>{emp_id}</strong> · 
    Dept: <strong>{dept}</strong> · Level: <strong>{level}</strong> · 
    <span class="badge badge-success">AI Active</span>
    <span class="badge badge-info" style="margin-left:4px;">Multi-Agent</span>
    <span class="badge badge-purple" style="margin-left:4px;">Autonomous</span>
  </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP KPI METRICS
# ─────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
kpis = [
    ("9", "Active Agents"),
    ("4", "Parallel Flows"),
    ("< 2s", "Avg Response"),
    ("98.2%", "Accuracy"),
    ("24/7", "Availability"),
]
for col, (val, lbl) in zip([m1,m2,m3,m4,m5], kpis):
    with col:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{lbl}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# USE CASE 1 — LEARNING & DEVELOPMENT
# ═══════════════════════════════════════════════════════════
if "Learning" in use_case:
    skills_pool = {
        "Engineering": {"current": ["Python", "SQL", "Git"], "required": ["Python", "SQL", "Git", "Machine Learning", "Cloud AWS", "Docker", "Kubernetes", "System Design"]},
        "Finance":     {"current": ["Excel", "SAP"], "required": ["Excel", "SAP", "Power BI", "Python", "Financial Modelling", "Risk Analysis"]},
        "HR":          {"current": ["Recruitment"], "required": ["Recruitment", "HRIS", "Analytics", "Compensation Design", "OD Strategy"]},
        "Operations":  {"current": ["Process Mgmt"], "required": ["Process Mgmt", "Lean Six Sigma", "ERP Systems", "Supply Chain", "Data Analysis"]},
        "Marketing":   {"current": ["Brand Mgmt"], "required": ["Brand Mgmt", "Digital Marketing", "SEO/SEM", "Analytics", "Content Strategy"]},
    }

    tabs = st.tabs(["🚀 Run Workflow", "📊 Analytics", "🗺️ Learning Path", "🏆 Leaderboard", "📋 Reports"])

    with tabs[0]:
        col_left, col_right = st.columns([1, 2])

        with col_left:
            section("🎛️ Configuration")
            skills_current = st.multiselect("Current Skills",
                skills_pool[dept]["required"],
                default=skills_pool[dept]["current"])
            target_role = st.selectbox("Target Role", [
                f"Senior {dept} Specialist", f"{dept} Lead", f"Principal {dept} Architect", "People Manager"])
            budget = st.slider("Training Budget (₹)", 10000, 150000, 75000, 5000)
            timeline = st.slider("Completion Timeline (months)", 3, 18, 9)

            if st.button("🤖 Launch AI Agents", use_container_width=True):
                st.session_state["ld_run"] = True
                st.session_state["ld_dept"] = dept
                st.session_state["ld_current"] = skills_current
                st.session_state["ld_required"] = skills_pool[dept]["required"]
                st.session_state["ld_budget"] = budget
                st.session_state["ld_timeline"] = timeline
                st.session_state["ld_target"] = target_role

        with col_right:
            if st.session_state.get("ld_run"):
                required = st.session_state["ld_required"]
                current  = st.session_state["ld_current"]
                gaps     = [s for s in required if s not in current]

                section("🤖 Agent Execution")

                agents = [
                    ("Skill Assessment Agent",       lambda: {"agent": "Skill Assessment", "output": f"Proficiency mapped for {len(current)} skills"}),
                    ("Profile Analysis Agent",       lambda: {"agent": "Profile Analysis", "output": f"Career trajectory to {st.session_state['ld_target']} analysed"}),
                    ("Skill Gap Analysis Agent",     lambda: {"agent": "Skill Gap", "output": f"{len(gaps)} critical gaps identified"}),
                    ("Course Discovery Agent",       lambda: {"agent": "Course Discovery", "output": f"{len(gaps)*3} courses found across 5 platforms"}),
                    ("Learning Path Agent",          lambda: {"agent": "Learning Path", "output": "Optimised 3-phase path created"}),
                    ("Manager Approval Agent",       lambda: {"agent": "Approval", "output": "Auto-approved (budget within threshold)"}),
                    ("Progress Tracker Agent",       lambda: {"agent": "Progress", "output": "Milestone KPIs set; dashboard active"}),
                    ("Certification Agent",          lambda: {"agent": "Certification", "output": "4 certifications targeted"}),
                    ("Notification Agent",           lambda: {"agent": "Notification", "output": "Alerts sent to employee & manager"}),
                ]
                results = run_agents(agents, exec_speed)

                st.success("✅ All 9 agents completed successfully!")

                for r in results:
                    icon_map = {"Skill Assessment":"🔍","Profile Analysis":"👤","Skill Gap":"🎯","Course Discovery":"📚","Learning Path":"🗺️","Approval":"✅","Progress":"📈","Certification":"🏆","Notification":"🔔"}
                    color_map = {"Skill Assessment":"var(--accent-cyan)","Profile Analysis":"var(--tata-gold)","Skill Gap":"var(--accent-orange)","Course Discovery":"var(--accent-purple)","Learning Path":"var(--accent-green)","Approval":"var(--accent-green)","Progress":"var(--accent-cyan)","Certification":"var(--tata-gold)","Notification":"var(--accent-orange)"}
                    ic = icon_map.get(r["agent"], "⚙️")
                    cl = color_map.get(r["agent"], "var(--accent-cyan)")
                    card(f"{ic} {r['agent']} Agent", r["output"], cl)

                # SKILL GAP CHART
                st.markdown("---")
                section("📊 Skill Gap Analysis")
                gap_df = pd.DataFrame({
                    "Skill": required,
                    "Current Level": [85 if s in current else random.randint(10,35) for s in required],
                    "Required Level": [random.randint(75,95) for _ in required],
                    "Status": ["✅ Proficient" if s in current else "❌ Gap" for s in required],
                })
                fig = go.Figure()
                fig.add_bar(name="Current Level", x=gap_df["Skill"], y=gap_df["Current Level"],
                            marker_color="#003366")
                fig.add_bar(name="Required Level", x=gap_df["Skill"], y=gap_df["Required Level"],
                            marker_color="#C8A951")
                fig.update_layout(barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color="#E8EDF5", height=300, margin=dict(t=20,b=20))
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("👈 Configure your profile and click **Launch AI Agents** to begin.")

    with tabs[1]:
        section("📊 L&D Analytics Dashboard")
        c1, c2 = st.columns(2)
        with c1:
            # Completion rate by dept
            dept_data = pd.DataFrame({
                "Department": ["Engineering","Finance","HR","Operations","Marketing"],
                "Completion %": [78, 65, 82, 71, 88],
                "Employees": [245, 132, 89, 310, 76],
            })
            fig = px.bar(dept_data, x="Department", y="Completion %", color="Completion %",
                         color_continuous_scale=["#003366","#C8A951"],
                         title="Training Completion by Department")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#E8EDF5", height=300, showlegend=False, margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            months = ["Jan","Feb","Mar","Apr","May","Jun"]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=months, y=[45,52,61,68,75,82], mode="lines+markers",
                                     name="Courses Enrolled", line=dict(color="#00D4FF", width=2)))
            fig2.add_trace(go.Scatter(x=months, y=[30,38,45,55,62,70], mode="lines+markers",
                                     name="Courses Completed", line=dict(color="#C8A951", width=2)))
            fig2.update_layout(title="Monthly Learning Trends", paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300, margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)

        # ROI Table
        section("💰 ROI & Impact Summary")
        roi_data = pd.DataFrame({
            "Metric": ["Skills Upgraded", "Certifications Earned", "Avg Productivity Gain", "Retention Improvement", "Training ROI"],
            "Value": ["1,847", "623", "+23%", "+31%", "4.2x"],
            "vs Last Year": ["+18%", "+42%", "+8%", "+12%", "+0.8x"],
            "Status": ["🟢 On Track","🟢 Exceeded","🟢 Excellent","🟢 Excellent","🟢 Strong"],
        })
        st.dataframe(roi_data, use_container_width=True, hide_index=True)

    with tabs[2]:
        if st.session_state.get("ld_run"):
            section("🗺️ Personalised Learning Roadmap")
            required = st.session_state["ld_required"]
            current  = st.session_state["ld_current"]
            gaps     = [s for s in required if s not in current]
            budget   = st.session_state["ld_budget"]
            timeline = st.session_state["ld_timeline"]

            phases = {
                "Phase 1 – Foundation (Months 1–3)": gaps[:max(1,len(gaps)//3)],
                "Phase 2 – Intermediate (Months 4–6)": gaps[len(gaps)//3:2*len(gaps)//3],
                "Phase 3 – Advanced (Months 7–9)": gaps[2*len(gaps)//3:],
            }
            phase_colors = ["var(--accent-cyan)","var(--tata-gold)","var(--accent-green)"]
            course_map = {
                "Machine Learning": ("ML Specialization – Coursera","Andrew Ng","₹15,000","4 months","⭐ 4.9"),
                "Cloud AWS": ("AWS Solutions Architect","AWS Training","₹18,000","3 months","⭐ 4.8"),
                "Docker": ("Docker & Kubernetes","Udemy","₹4,000","1 month","⭐ 4.7"),
                "Kubernetes": ("CKA Certification","CNCF","₹22,000","3 months","⭐ 4.8"),
                "System Design": ("System Design Primer","Educative","₹8,000","2 months","⭐ 4.6"),
                "Power BI": ("Power BI Masterclass","Udemy","₹3,500","1 month","⭐ 4.7"),
                "Financial Modelling": ("CFA Level 1","CFA Institute","₹45,000","6 months","⭐ 4.9"),
                "Risk Analysis": ("FRM Certification","GARP","₹38,000","6 months","⭐ 4.8"),
            }
            total_cost = 0
            for (phase, skills), color in zip(phases.items(), phase_colors):
                with st.expander(f"📌 {phase}", expanded=True):
                    for skill in skills:
                        info = course_map.get(skill, (f"{skill} – Industry Certification","Various","₹10,000","2 months","⭐ 4.5"))
                        total_cost += int(info[2].replace("₹","").replace(",",""))
                        st.markdown(f"""
                        <div style="background:var(--bg-card);border:1px solid var(--border);
                                    border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:0.6rem;">
                          <div style="display:flex;justify-content:space-between;align-items:center;">
                            <div>
                              <div style="font-family:Rajdhani,sans-serif;font-weight:600;color:{color};font-size:1rem;">📚 {info[0]}</div>
                              <div style="color:var(--text-secondary);font-size:0.82rem;">
                                👤 {info[1]} &nbsp;·&nbsp; ⏱ {info[3]} &nbsp;·&nbsp; {info[4]}
                              </div>
                            </div>
                            <div style="text-align:right;">
                              <div style="color:var(--tata-gold);font-weight:600;">{info[2]}</div>
                              <span class="badge badge-info">Recommended</span>
                            </div>
                          </div>
                        </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#003366,#001a33);border:1px solid var(--tata-gold);
                        border-radius:12px;padding:1.2rem 1.5rem;margin-top:1rem;">
              <div style="font-family:Rajdhani,sans-serif;font-size:1.2rem;font-weight:700;color:var(--tata-gold);">
                📊 Learning Plan Summary
              </div>
              <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:0.8rem;">
                <div style="text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#00D4FF;">{len(gaps)}</div><div style="font-size:0.75rem;color:var(--text-secondary);">Skills to Learn</div></div>
                <div style="text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#00E676;">₹{budget:,}</div><div style="font-size:0.75rem;color:var(--text-secondary);">Budget Allocated</div></div>
                <div style="text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#C8A951;">{timeline} mo</div><div style="font-size:0.75rem;color:var(--text-secondary);">Timeline</div></div>
                <div style="text-align:center;"><div style="font-size:1.5rem;font-weight:700;color:#FF6B35;">+45%</div><div style="font-size:0.75rem;color:var(--text-secondary);">Expected Growth</div></div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Run the workflow first to generate your personalised learning path.")

    with tabs[3]:
        section("🏆 Company-Wide L&D Leaderboard")
        lb_data = pd.DataFrame({
            "Rank": ["🥇","🥈","🥉","4","5","6","7","8"],
            "Employee": ["Priya Patel","Rahul Singh","Aisha Kumar","John Mathew","Neha Joshi",emp_name,"Vikram Rao","Sunita Das"],
            "Department": ["Engineering","Finance","HR","Engineering","Marketing",dept,"Operations","Finance"],
            "Courses Completed": [24,21,19,18,17,15,14,13],
            "Certifications": [8,6,7,5,6,4,5,4],
            "Learning Hours": [320,285,261,245,230,198,187,175],
            "Score": [9.8,9.4,9.1,8.9,8.7,8.2,7.9,7.6],
        })
        st.dataframe(lb_data, use_container_width=True, hide_index=True)

        fig = px.bar(lb_data, x="Employee", y="Learning Hours", color="Score",
                     color_continuous_scale=["#003366","#C8A951","#00D4FF"],
                     title="Learning Hours vs Score")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#E8EDF5", height=320, margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[4]:
        section("📋 Detailed Agent Report")
        if st.session_state.get("ld_run"):
            report = f"""
═══════════════════════════════════════════════════
  TATA GROUP — LEARNING & DEVELOPMENT REPORT
═══════════════════════════════════════════════════
Employee   : {emp_name}
ID         : {emp_id}
Department : {st.session_state['ld_dept']}
Target Role: {st.session_state['ld_target']}
Generated  : {datetime.now().strftime('%d %b %Y, %H:%M')}

SKILL GAP SUMMARY
─────────────────
Required Skills : {len(st.session_state['ld_required'])}
Current Skills  : {len(st.session_state['ld_current'])}
Gaps Identified : {len([s for s in st.session_state['ld_required'] if s not in st.session_state['ld_current']])}

LEARNING PLAN
─────────────
Budget    : ₹{st.session_state['ld_budget']:,}
Timeline  : {st.session_state['ld_timeline']} months
Phases    : 3 (Foundation → Intermediate → Advanced)
Courses   : {len([s for s in st.session_state['ld_required'] if s not in st.session_state['ld_current']])*3} identified

AGENT EXECUTION LOG
───────────────────
✅ Skill Assessment Agent      — Completed
✅ Profile Analysis Agent      — Completed
✅ Skill Gap Analysis Agent    — Completed
✅ Course Discovery Agent      — Completed
✅ Learning Path Agent         — Completed
✅ Manager Approval Agent      — Auto-approved
✅ Progress Tracker Agent      — Active
✅ Certification Agent         — Targeting 4 certs
✅ Notification Agent          — Alerts dispatched

STATUS: APPROVED & ACTIVE
═══════════════════════════════════════════════════
"""
            st.code(report, language=None)
            st.download_button("⬇️ Download Report", report.encode(), f"LD_Report_{emp_id}.txt", use_container_width=True)
        else:
            st.info("Run the workflow to generate the report.")


# ═══════════════════════════════════════════════════════════
# USE CASE 2 — RECRUITMENT
# ═══════════════════════════════════════════════════════════
elif "Recruitment" in use_case:
    tabs = st.tabs(["🚀 Run Workflow", "📂 Candidates", "📊 Analytics", "📋 Reports"])

    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        with col1:
            section("📝 Job Configuration")
            job_title = st.text_input("Job Title", f"Senior {dept} Engineer")
            num_positions = st.number_input("Open Positions", 1, 20, 3)
            experience = st.selectbox("Experience Required", ["2-4 years","4-6 years","6-8 years","8+ years"])
            skills_req = st.multiselect("Required Skills",
                ["Python","Java","SQL","Cloud","ML","React","Node.js","DevOps","Leadership","Communication"],
                default=["Python","SQL","Cloud"])
            if st.button("🤖 Launch Recruitment Agents", use_container_width=True):
                st.session_state["rec_run"] = True
                st.session_state["rec_job"] = job_title
                st.session_state["rec_pos"] = num_positions
                st.session_state["rec_skills"] = skills_req

        with col2:
            if st.session_state.get("rec_run"):
                section("🤖 Agent Execution")
                agents = [
                    ("JD Generator Agent",       lambda: "Crafted optimised JD with inclusive language"),
                    ("Job Posting Agent",         lambda: "Posted on Naukri, LinkedIn, Internal Portal"),
                    ("Resume Screening Agent",    lambda: "Screened 847 applications → 92 shortlisted"),
                    ("Skills Matching Agent",     lambda: "AI-matched top 92 profiles (85%+ fit score)"),
                    ("Interview Scheduler Agent", lambda: "45 interviews scheduled (Calendly + Teams)"),
                    ("Background Check Agent",    lambda: "BGV initiated for 12 finalists"),
                    ("Offer Generator Agent",     lambda: "3 competitive offers generated"),
                    ("Onboarding Agent",          lambda: "Day-1 onboarding kit dispatched"),
                ]
                results = run_agents(agents, exec_speed)
                st.success("✅ Recruitment pipeline complete!")
                colors = ["var(--accent-cyan)","var(--tata-gold)","var(--accent-orange)","var(--accent-purple)",
                          "var(--accent-green)","var(--accent-cyan)","var(--tata-gold)","var(--accent-green)"]
                for (name, _), res, color in zip(agents, results, colors):
                    card(f"🔹 {name}", res, color)

                # Funnel chart
                st.markdown("---")
                section("📉 Recruitment Funnel")
                funnel_df = pd.DataFrame({
                    "Stage": ["Applications","Screened","Shortlisted","Interviewed","Final Round","Offers","Joined"],
                    "Count": [847, 312, 92, 45, 18, int(num_positions)+1, num_positions],
                })
                fig = px.funnel(funnel_df, x="Count", y="Stage", color_discrete_sequence=["#003366"])
                fig.update_traces(marker_color=["#003366","#0055aa","#0077cc","#00D4FF","#C8A951","#00E676","#00E676"])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font_color="#E8EDF5", height=380, margin=dict(t=20,b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👈 Configure the job and click **Launch Recruitment Agents**.")

    with tabs[1]:
        section("📂 Top Candidate Shortlist")
        names = ["Aarav Kapoor","Divya Menon","Rohan Iyer","Sneha Pillai","Karan Bhatia","Meera Nair","Aryan Gupta","Pooja Singh"]
        cand_df = pd.DataFrame({
            "Candidate": names,
            "Experience": [f"{random.randint(3,9)} years" for _ in names],
            "Skills Match": [f"{random.randint(82,98)}%" for _ in names],
            "Test Score": [f"{random.randint(75,97)}/100" for _ in names],
            "AI Score": [round(random.uniform(8.0,9.9),1) for _ in names],
            "Stage": [random.choice(["Technical Round","HR Round","Offer Stage","Joined","In Review"]) for _ in names],
            "Status": [random.choice(["🟢 Active","🟡 Pending","🔵 Offered","🟢 Joined"]) for _ in names],
        })
        st.dataframe(cand_df.sort_values("AI Score", ascending=False), use_container_width=True, hide_index=True)

    with tabs[2]:
        section("📊 Recruitment Analytics")
        c1, c2 = st.columns(2)
        with c1:
            src_df = pd.DataFrame({"Source":["LinkedIn","Naukri","Internal","Referral","Campus"],"Candidates":[320,245,110,95,77]})
            fig = px.pie(src_df, names="Source", values="Candidates", title="Source of Hire",
                         color_discrete_sequence=["#003366","#0055aa","#C8A951","#00D4FF","#00E676"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=320, margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            time_df = pd.DataFrame({"Stage":["JD Publish","Screen","Interview","Offer","Join"],"Days":[2,5,12,3,14]})
            fig2 = px.bar(time_df, x="Stage", y="Days", title="Time-to-Hire by Stage",
                          color="Days", color_continuous_scale=["#003366","#C8A951"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color="#E8EDF5", height=320, margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)

    with tabs[3]:
        section("📋 Recruitment Report")
        if st.session_state.get("rec_run"):
            rpt = f"""
TATA GROUP — RECRUITMENT REPORT
Job Title  : {st.session_state.get('rec_job','N/A')}
Positions  : {st.session_state.get('rec_pos','N/A')}
Generated  : {datetime.now().strftime('%d %b %Y, %H:%M')}

PIPELINE SUMMARY
Applications   : 847
Shortlisted    : 92
Interviewed    : 45
Offers Made    : {st.session_state.get('rec_pos',3)+1}
Positions Filled: {st.session_state.get('rec_pos',3)}

Time to Fill  : 36 days (industry avg: 52 days)
Cost per Hire : ₹45,000 (savings: ₹18,000)
Quality Score : 8.7/10
"""
            st.code(rpt, language=None)
            st.download_button("⬇️ Download Recruitment Report", rpt.encode(), "Recruitment_Report.txt", use_container_width=True)
        else:
            st.info("Run the recruitment workflow first.")


# ═══════════════════════════════════════════════════════════
# USE CASE 3 — IT SERVICE DESK
# ═══════════════════════════════════════════════════════════
elif "IT Service" in use_case:
    tabs = st.tabs(["🎫 Raise Ticket", "📋 Dashboard", "📊 Analytics", "🔧 Diagnostics"])

    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        with col1:
            section("🎫 New IT Request")
            issue_type = st.selectbox("Issue Category", [
                "💻 Laptop/Hardware", "🔒 Password Reset", "📧 Email Access",
                "🌐 VPN/Network", "🖨️ Printer", "📱 Mobile Device",
                "🔑 Software License", "☁️ Cloud Access", "🛡️ Security Alert"])
            priority    = st.selectbox("Priority", ["🔴 Critical","🟠 High","🟡 Medium","🟢 Low"])
            description = st.text_area("Describe the Issue", "My laptop is running slow and the VPN keeps disconnecting.")
            if st.button("🤖 Submit to AI Agents", use_container_width=True):
                st.session_state["it_run"] = True
                st.session_state["it_issue"] = issue_type
                st.session_state["it_priority"] = priority
                st.session_state["it_desc"] = description

        with col2:
            if st.session_state.get("it_run"):
                ticket_id = f"INC-{random.randint(100000,999999)}"
                section(f"🎫 Ticket {ticket_id}")
                st.markdown(f"""
                <div style="background:var(--bg-card2);border:1px solid var(--tata-gold);border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;">
                  <div style="display:flex;justify-content:space-between;">
                    <span style="color:var(--tata-gold);font-family:Rajdhani,sans-serif;font-size:1.2rem;font-weight:700;">{ticket_id}</span>
                    <span class="badge badge-warning">{st.session_state['it_priority']}</span>
                  </div>
                  <div style="color:var(--text-secondary);font-size:0.85rem;margin-top:0.4rem;">{st.session_state['it_issue']} · Submitted by {emp_name}</div>
                </div>""", unsafe_allow_html=True)

                agents = [
                    ("Ticket Classifier Agent",    lambda: "Category: Hardware+Network · Priority: High"),
                    ("Knowledge Base Agent",       lambda: "Found 3 relevant resolution articles (89% match)"),
                    ("Diagnostics Agent",          lambda: "Remote diagnostics: RAM 87%, CPU 94%, VPN config error"),
                    ("Auto-Resolver Agent",        lambda: "Auto-fix applied: VPN config reset, temp files cleared"),
                    ("Escalation Agent",           lambda: "L2 team notified (hardware inspection scheduled)"),
                    ("SLA Monitor Agent",          lambda: "SLA: 4h critical → Resolution estimate: 2.5h ✅"),
                    ("User Notifier Agent",        lambda: f"SMS + Email sent to {emp_name}"),
                ]
                results = run_agents(agents, exec_speed)
                st.success(f"✅ Ticket {ticket_id} processed by 7 agents!")

                for (name,_), res in zip(agents, results):
                    card(f"🔹 {name}", res)

                # Auto-resolution steps
                st.markdown("---")
                section("🔧 Auto-Resolution Steps Applied")
                steps = ["VPN client configuration reset","Temporary files cleaned (2.3 GB freed)",
                         "Background processes optimised","Driver updates queued (auto-apply tonight)",
                         "Network DNS cache flushed","L2 engineer assigned for hardware inspection"]
                for i, step in enumerate(steps, 1):
                    st.markdown(f"""
                    <div class="workflow-step">
                      <div class="step-num">{i}</div>
                      <div style="color:var(--text-primary);font-size:0.88rem;">{step}</div>
                      <span class="badge badge-success" style="margin-left:auto;">Done</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("👈 Fill in the issue details and submit to AI Agents.")

    with tabs[1]:
        section("📋 IT Service Desk Dashboard")
        m1,m2,m3,m4 = st.columns(4)
        for col, (val, lbl, color) in zip([m1,m2,m3,m4],[
            ("247","Open Tickets","var(--accent-orange)"),
            ("89%","Auto-Resolved","var(--accent-green)"),
            ("1.8h","Avg Resolution","var(--accent-cyan)"),
            ("98.2%","SLA Adherence","var(--tata-gold)")]):
            with col:
                st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:{color};'>{val}</div><div class='metric-label'>{lbl}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tickets = pd.DataFrame({
            "Ticket ID": [f"INC-{random.randint(100000,999999)}" for _ in range(8)],
            "Issue": random.choices(["VPN Issue","Password Reset","Laptop Crash","Email Down","Printer","Software License","Network","Security"],k=8),
            "Priority": random.choices(["🔴 Critical","🟠 High","🟡 Medium","🟢 Low"],k=8,weights=[1,2,4,3]),
            "Status": random.choices(["✅ Resolved","🔄 In Progress","⏳ Pending","🔵 Escalated"],k=8,weights=[5,2,1,1]),
            "Assigned To": random.choices(["AI Bot","L1 Support","L2 Engineer","L3 Expert"],k=8),
            "Created": [(datetime.now()-timedelta(hours=random.randint(1,48))).strftime("%d %b %H:%M") for _ in range(8)],
            "SLA": random.choices(["✅ Within","⚠️ At Risk","❌ Breached"],k=8,weights=[7,2,1]),
        })
        st.dataframe(tickets, use_container_width=True, hide_index=True)

    with tabs[2]:
        section("📊 IT Analytics")
        c1, c2 = st.columns(2)
        with c1:
            cat_df = pd.DataFrame({"Category":["Hardware","Network","Software","Access","Security","Other"],
                                   "Count":[89,72,65,48,23,15]})
            fig = px.pie(cat_df, names="Category", values="Count", title="Tickets by Category",
                         color_discrete_sequence=["#003366","#0055aa","#C8A951","#00D4FF","#FF6B35","#00E676"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300, margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=days, y=[45,62,58,71,53,21,8], name="Tickets Created", marker_color="#003366"))
            fig2.add_trace(go.Bar(x=days, y=[40,55,52,68,50,20,7], name="Resolved", marker_color="#C8A951"))
            fig2.update_layout(barmode="group", title="Weekly Ticket Trend",
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color="#E8EDF5", height=300, margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)

    with tabs[3]:
        section("🔧 AI Diagnostics Engine")
        if st.button("🔍 Run System Diagnostics", use_container_width=True):
            metrics = {
                "CPU Usage": random.randint(30, 92),
                "RAM Usage": random.randint(45, 88),
                "Disk Usage": random.randint(20, 75),
                "Network Latency": random.randint(5, 120),
            }
            for metric, value in metrics.items():
                color = "#00E676" if value < 60 else "#FFA726" if value < 80 else "#FF5252"
                unit = "ms" if "Latency" in metric else "%"
                st.markdown(f"""
                <div style="background:var(--bg-card2);border:1px solid var(--border);border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:0.5rem;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="color:var(--text-primary);font-size:0.9rem;">{metric}</div>
                    <div style="color:{color};font-family:Rajdhani,sans-serif;font-size:1.1rem;font-weight:700;">{value}{unit}</div>
                  </div>
                  <div class="progress-container" style="margin-top:0.5rem;">
                    <div class="progress-fill" style="width:{min(value,100)}%;background:linear-gradient(90deg,var(--tata-blue),{color});"></div>
                  </div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# USE CASE 4 — PROCUREMENT
# ═══════════════════════════════════════════════════════════
elif "Procurement" in use_case:
    tabs = st.tabs(["🛒 New Request", "📦 Purchase Orders", "🏢 Vendors", "📊 Analytics"])

    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        with col1:
            section("🛒 Procurement Request")
            category = st.selectbox("Category", ["IT Hardware","Software Licenses","Office Supplies","Travel","Facilities","Services"])
            item_desc = st.text_input("Item Description", "Dell Latitude 5540 Laptop × 10 units")
            budget    = st.number_input("Estimated Budget (₹)", 10000, 5000000, 250000, 10000)
            urgency   = st.selectbox("Urgency", ["🔴 Urgent (< 1 week)","🟠 High (< 2 weeks)","🟡 Normal (< 1 month)","🟢 Low (flexible)"])
            if st.button("🤖 Launch Procurement Agents", use_container_width=True):
                st.session_state["proc_run"] = True
                st.session_state["proc_item"] = item_desc
                st.session_state["proc_budget"] = budget
                st.session_state["proc_cat"] = category

        with col2:
            if st.session_state.get("proc_run"):
                po_num = f"PO-2025-{random.randint(10000,99999)}"
                section(f"📦 {po_num}")
                agents = [
                    ("Requirements Validator",    lambda: "Specifications validated against policy"),
                    ("Vendor Discovery Agent",    lambda: "12 approved vendors identified for category"),
                    ("RFQ Generator Agent",       lambda: "RFQ sent to top 5 vendors automatically"),
                    ("Price Benchmarking Agent",  lambda: "Market pricing analysed (12% below benchmark found)"),
                    ("Quote Comparison Agent",    lambda: "Best vendor: Ingram Micro @ ₹2,18,500 (saving ₹31,500)"),
                    ("Compliance Check Agent",    lambda: "GST, import duty, policy compliance verified ✅"),
                    ("Approval Router Agent",     lambda: f"Routed to {dept} Head for ₹{budget:,} approval"),
                    ("PO Generator Agent",        lambda: f"{po_num} generated & dispatched"),
                    ("Delivery Tracker Agent",    lambda: "ETA: 5 business days · Tracking active"),
                ]
                results = run_agents(agents, exec_speed)
                st.success(f"✅ {po_num} processed by 9 agents!")

                for (name,_), res in zip(agents, results):
                    card(f"🔹 {name}", res)

                # Cost saving highlight
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#003366,#001a33);border:1px solid #00E676;
                            border-radius:12px;padding:1.2rem 1.5rem;margin-top:1rem;">
                  <div style="font-family:Rajdhani,sans-serif;font-size:1.2rem;font-weight:700;color:#00E676;">
                    💰 Cost Savings Summary
                  </div>
                  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:0.8rem;">
                    <div style="text-align:center;"><div style="font-size:1.4rem;font-weight:700;color:#00D4FF;">₹{budget:,}</div><div style="font-size:0.75rem;color:var(--text-secondary);">Budget</div></div>
                    <div style="text-align:center;"><div style="font-size:1.4rem;font-weight:700;color:#C8A951;">₹{int(budget*0.88):,}</div><div style="font-size:0.75rem;color:var(--text-secondary);">Best Quote</div></div>
                    <div style="text-align:center;"><div style="font-size:1.4rem;font-weight:700;color:#00E676;">₹{int(budget*0.12):,}</div><div style="font-size:0.75rem;color:var(--text-secondary);">AI Savings</div></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("👈 Fill in the procurement details and launch agents.")

    with tabs[1]:
        section("📦 Active Purchase Orders")
        pos = pd.DataFrame({
            "PO Number": [f"PO-2025-{random.randint(10000,99999)}" for _ in range(8)],
            "Item": ["Laptop × 10","Office Chairs × 25","Software Licenses","Server Hardware","Stationary","Cloud Credits","Networking Gear","Security Tools"],
            "Vendor": ["Ingram Micro","OfficeMax","Microsoft","HP Enterprise","Staples","AWS","Cisco","CrowdStrike"],
            "Amount": [f"₹{random.randint(50,500)*1000:,}" for _ in range(8)],
            "Status": random.choices(["✅ Delivered","🔄 Shipped","⏳ Approved","📋 Raised","🔵 Negotiating"],k=8),
            "ETA": [(datetime.now()+timedelta(days=random.randint(1,30))).strftime("%d %b") for _ in range(8)],
        })
        st.dataframe(pos, use_container_width=True, hide_index=True)

    with tabs[2]:
        section("🏢 Vendor Performance Dashboard")
        vendors = pd.DataFrame({
            "Vendor": ["Ingram Micro","HP Enterprise","Cisco","Microsoft","Dell","Lenovo","AWS","Oracle"],
            "Category": ["Hardware","Hardware","Network","Software","Hardware","Hardware","Cloud","Software"],
            "Rating": [4.8, 4.6, 4.7, 4.9, 4.5, 4.4, 4.9, 4.3],
            "On-Time %": [95, 92, 97, 99, 90, 88, 99, 94],
            "Savings %": [12, 8, 10, 15, 7, 9, 18, 11],
            "Compliance": ["✅ Verified"]*8,
        })
        st.dataframe(vendors.sort_values("Rating", ascending=False), use_container_width=True, hide_index=True)

        fig = px.scatter(vendors, x="On-Time %", y="Savings %", size="Rating", color="Category",
                         hover_name="Vendor", title="Vendor: On-Time vs Savings",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#E8EDF5", height=350, margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        section("📊 Procurement Analytics")
        c1, c2 = st.columns(2)
        with c1:
            spend_df = pd.DataFrame({"Category":["IT Hardware","Software","Travel","Facilities","Services","Supplies"],"Spend (₹L)":[45,32,18,22,28,12]})
            fig = px.pie(spend_df, names="Category", values="Spend (₹L)", title="Spend by Category",
                         color_discrete_sequence=["#003366","#0055aa","#C8A951","#00D4FF","#FF6B35","#00E676"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300, margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            months = ["Jan","Feb","Mar","Apr","May","Jun"]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=months, y=[120,145,132,168,155,178], name="Spend (₹L)", marker_color="#003366"))
            fig2.add_trace(go.Scatter(x=months, y=[8,11,9,14,12,16], mode="lines+markers", name="Savings (₹L)", yaxis="y2", line=dict(color="#C8A951")))
            fig2.update_layout(title="Monthly Spend vs Savings", paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300,
                               yaxis2=dict(overlaying="y",side="right"), margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# USE CASE 5 — LEAVE MANAGEMENT
# ═══════════════════════════════════════════════════════════
elif "Leave" in use_case:
    tabs = st.tabs(["📅 Apply Leave", "📋 My Leaves", "👥 Team Calendar", "📊 Analytics"])

    with tabs[0]:
        col1, col2 = st.columns([1, 2])
        with col1:
            section("📅 Leave Application")
            leave_type = st.selectbox("Leave Type", ["🏖️ Annual Leave","🤒 Sick Leave","👶 Maternity/Paternity","📚 Study Leave","🏠 Work from Home","⚠️ Emergency Leave"])
            start_date = st.date_input("Start Date", datetime.now() + timedelta(days=7))
            end_date   = st.date_input("End Date",   datetime.now() + timedelta(days=11))
            reason     = st.text_area("Reason", "Family vacation planned. All project deliverables completed.")
            handover   = st.text_input("Handover To", "Team Lead – Vikram Rao")
            if st.button("🤖 Submit to AI Leave Agents", use_container_width=True):
                days = (end_date - start_date).days + 1
                st.session_state["lv_run"] = True
                st.session_state["lv_type"] = leave_type
                st.session_state["lv_days"] = days
                st.session_state["lv_start"] = start_date
                st.session_state["lv_handover"] = handover

        with col2:
            if st.session_state.get("lv_run"):
                days = st.session_state["lv_days"]
                ref  = f"LV-{random.randint(100000,999999)}"
                section(f"🔍 Processing {ref}")
                agents = [
                    ("Leave Balance Agent",      lambda: f"Balance: Annual 12d, Sick 6d, Comp 3d available"),
                    ("Policy Validator Agent",   lambda: "Policy compliance: ✅ 14-day advance notice met"),
                    ("Conflict Checker Agent",   lambda: "No project deadline conflicts detected"),
                    ("Team Coverage Agent",      lambda: "Coverage confirmed: 3/5 team members available"),
                    ("Workload Analyser Agent",  lambda: "Sprint tasks reassigned to 2 teammates"),
                    ("Manager Approval Agent",   lambda: "Auto-approved (< 5 days, policy met)"),
                    ("HR System Updater Agent",  lambda: f"SAP SuccessFactors updated: {days}d deducted"),
                    ("Calendar Sync Agent",      lambda: "Google Calendar + Outlook blocked & synced"),
                    ("Notification Agent",       lambda: f"Alerts: {emp_name}, Manager, HR, Team"),
                ]
                results = run_agents(agents, exec_speed)
                st.success(f"✅ Leave {ref} APPROVED automatically!")

                status_color = "var(--accent-green)"
                for (name,_), res in zip(agents, results):
                    card(f"🔹 {name}", res)

                # Leave summary card
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#003366,#001a33);border:2px solid #00E676;
                            border-radius:14px;padding:1.5rem;margin-top:1rem;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <div style="font-family:Rajdhani,sans-serif;font-size:1.4rem;font-weight:700;color:#00E676;">
                        ✅ LEAVE APPROVED
                      </div>
                      <div style="color:var(--text-secondary);font-size:0.85rem;">Ref: {ref}</div>
                    </div>
                    <div style="text-align:right;">
                      <div style="font-size:2rem;font-weight:700;color:#C8A951;">{days}</div>
                      <div style="font-size:0.75rem;color:var(--text-secondary);">DAYS APPROVED</div>
                    </div>
                  </div>
                  <div style="margin-top:1rem;display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;">
                    <div><div style="color:var(--text-secondary);font-size:0.75rem;">TYPE</div><div style="color:var(--text-primary);font-size:0.88rem;">{st.session_state['lv_type']}</div></div>
                    <div><div style="color:var(--text-secondary);font-size:0.75rem;">FROM</div><div style="color:var(--text-primary);font-size:0.88rem;">{st.session_state['lv_start'].strftime('%d %b %Y')}</div></div>
                    <div><div style="color:var(--text-secondary);font-size:0.75rem;">HANDOVER</div><div style="color:var(--text-primary);font-size:0.88rem;">{st.session_state['lv_handover']}</div></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("👈 Fill in the leave details and submit.")

    with tabs[1]:
        section("📋 My Leave History")
        types = ["🏖️ Annual","🤒 Sick","🏠 WFH","📚 Study","⚠️ Emergency"]
        leave_hist = pd.DataFrame({
            "Ref":    [f"LV-{random.randint(100000,999999)}" for _ in range(8)],
            "Type":   random.choices(types, k=8),
            "From":   [(datetime.now()-timedelta(days=random.randint(30,300))).strftime("%d %b %Y") for _ in range(8)],
            "Days":   [random.randint(1,10) for _ in range(8)],
            "Status": random.choices(["✅ Approved","❌ Rejected","🔄 Pending"],k=8,weights=[7,1,2]),
            "Approved By": random.choices(["Auto-AI","Manager","HR"],k=8,weights=[5,3,2]),
        })
        st.dataframe(leave_hist, use_container_width=True, hide_index=True)

        # Leave balance
        section("💼 Leave Balance")
        balances = pd.DataFrame({
            "Leave Type": ["🏖️ Annual","🤒 Sick","👶 Maternity/Paternity","📚 Study","⚠️ Comp Off"],
            "Entitled": [24,12,180,10,5],
            "Used": [12,3,0,5,2],
            "Balance": [12,9,180,5,3],
        })
        st.dataframe(balances, use_container_width=True, hide_index=True)

    with tabs[2]:
        section("👥 Team Leave Calendar (This Month)")
        team_members = ["Arjun Sharma","Priya Patel","Rahul Singh","Aisha Kumar","Vikram Rao"]
        days_in_month = list(range(1,32))
        calendar_data = []
        for member in team_members:
            leave_days = random.sample(days_in_month, random.randint(0,5))
            for day in days_in_month:
                calendar_data.append({"Member": member, "Day": day,
                                       "Status": "On Leave" if day in leave_days else "Working"})
        cal_df = pd.DataFrame(calendar_data)
        pivot = cal_df.pivot(index="Member", columns="Day", values="Status")
        fig = go.Figure(data=go.Heatmap(
            z=[[1 if v=="On Leave" else 0 for v in row] for row in pivot.values],
            x=[str(d) for d in days_in_month],
            y=pivot.index.tolist(),
            colorscale=[[0,"#003366"],[1,"#C8A951"]],
            showscale=False,
        ))
        fig.update_layout(title="Team Availability (Gold = On Leave)",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#E8EDF5", height=280, margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        section("📊 Leave Analytics")
        c1, c2 = st.columns(2)
        with c1:
            lt_df = pd.DataFrame({"Type":["Annual","Sick","WFH","Study","Emergency"],"Days":[245,89,312,45,23]})
            fig = px.pie(lt_df, names="Type", values="Days", title="Leave Distribution",
                         color_discrete_sequence=["#003366","#0055aa","#C8A951","#00D4FF","#FF6B35"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300, margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            months = ["Jan","Feb","Mar","Apr","May","Jun"]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=months, y=[45,62,38,71,55,48], name="Leave Days", marker_color="#003366"))
            fig2.add_trace(go.Scatter(x=months, y=[92,88,95,85,90,93], mode="lines+markers", name="Team Available %",
                                      yaxis="y2", line=dict(color="#C8A951")))
            fig2.update_layout(title="Leave Trends & Team Availability", paper_bgcolor="rgba(0,0,0,0)",
                               plot_bgcolor="rgba(0,0,0,0)", font_color="#E8EDF5", height=300,
                               yaxis2=dict(overlaying="y",side="right",range=[70,100]),
                               margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────
# AGENT TIMELINE (GLOBAL, shown when toggled)
# ─────────────────────────────────────────────
if show_timeline:
    st.markdown("---")
    section("⏱️ Agent Execution Timeline")
    timeline_data = []
    base = datetime.now() - timedelta(seconds=30)
    agent_names = {
        "Learning": ["Skill Assessment","Profile Analysis","Skill Gap","Course Discovery","Learning Path","Approval","Progress","Certification","Notification"],
        "Recruitment": ["JD Generator","Job Posting","Resume Screen","Skills Match","Interview Schedule","Background Check","Offer Generator","Onboarding"],
        "IT": ["Ticket Classifier","Knowledge Base","Diagnostics","Auto-Resolver","Escalation","SLA Monitor","Notifier"],
        "Procurement": ["Requirements Validator","Vendor Discovery","RFQ Generator","Price Benchmark","Quote Compare","Compliance Check","Approval Router","PO Generator","Delivery Tracker"],
        "Leave": ["Balance Checker","Policy Validator","Conflict Checker","Coverage Agent","Workload Analyser","Approval Agent","HR Updater","Calendar Sync","Notifier"],
    }
    key = [k for k in agent_names if k in use_case][0]
    agents_list = agent_names[key]
    colors_tl = ["#003366","#0055aa","#0077cc","#00D4FF","#C8A951","#00E676","#FF6B35","#7C4DFF","#FF5252"]

    for i, ag in enumerate(agents_list):
        start = base + timedelta(seconds=i*2.5)
        end   = start + timedelta(seconds=random.uniform(1.2, 2.2))
        timeline_data.append(dict(Task=ag, Start=start, Finish=end, Agent=f"Agent {i+1}"))

    tl_df = pd.DataFrame(timeline_data)
    fig = px.timeline(tl_df, x_start="Start", x_end="Finish", y="Task", color="Agent",
                      color_discrete_sequence=colors_tl, title="Multi-Agent Parallel Execution")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#E8EDF5", height=350, showlegend=False, margin=dict(t=40,b=20))
    st.plotly_chart(fig, use_container_width=True)

if show_reasoning:
    with st.expander("🧠 AI Agent Reasoning & Decision Log"):
        reasoning = {
            "Architecture": "Multi-agent orchestration with parallel + sequential execution chains",
            "Decision Engine": "Rule-based + LLM-guided hybrid with policy guardrails",
            "Data Sources": "SAP SuccessFactors, ServiceNow, Oracle ERP, Internal Knowledge Base",
            "Approval Logic": "Threshold-based auto-approval with human-in-the-loop escalation",
            "Confidence Score": f"{random.uniform(94, 99):.1f}%",
            "Execution Mode": "Parallel Phase 1 → Sequential Phase 2 → Notification Broadcast",
        }
        for k, v in reasoning.items():
            card(k, v)

# FOOTER
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:var(--text-secondary);font-size:0.78rem;border-top:1px solid var(--border);margin-top:2rem;">
  🤖 <strong style="color:var(--tata-gold);">Tata Group Agentic AI Platform</strong> · 
  Powered by Multi-Agent Orchestration · 5 Business Use Cases · 
  Built for enterprise-grade autonomous workflows · v2.0
</div>""", unsafe_allow_html=True)

# init session state defaults
for key in ["ld_run","rec_run","it_run","proc_run","lv_run"]:
    if key not in st.session_state:
        st.session_state[key] = False
