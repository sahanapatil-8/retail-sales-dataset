import streamlit as st
import requests
import pandas as pd

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PriceIQ · Dynamic Pricing Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "PriceIQ — AI-Powered Dynamic Pricing Intelligence"
    }
)

API_URL = "https://dynamic-pricing-backend-rywt.onrender.com/predict"

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@400;500;600;700;800;900&family=Instrument+Sans:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1380px;
}

/* ── Dark Sidebar ── */
[data-testid="stSidebar"] {
    background: #070d1a !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] label {
    font-family: 'Fira Code', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #334155 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #0f1929 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * {
    background: #0f1929 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] input {
    background: #0f1929 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    color: #e2e8f0 !important;
}

/* ── Sidebar Brand ── */
.sidebar-brand {
    padding: 1.75rem 1.25rem 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.75rem;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}
.sidebar-logo-mark {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; line-height: 1;
}
.sidebar-logo-name {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 900;
    color: #ffffff !important;
    letter-spacing: -0.03em;
}
.sidebar-tagline {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    color: #334155 !important;
    letter-spacing: 0.08em;
}
.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 1.25rem 0;
}
.sidebar-section {
    font-family: 'Fira Code', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1e3a5f !important;
    margin-bottom: 0.85rem;
    padding: 0 0.2rem;
}
.sidebar-cta {
    margin-top: 1.5rem;
    padding: 0 0.2rem;
}

/* ── Sidebar button ── */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    width: 100%;
    letter-spacing: -0.01em;
    box-shadow: 0 4px 20px rgba(245,158,11,0.35) !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    box-shadow: 0 6px 28px rgba(245,158,11,0.5) !important;
    transform: translateY(-1px);
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 2.25rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}
.page-header-left {}
.page-eyebrow {
    font-family: 'Fira Code', monospace;
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #f59e0b;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.page-eyebrow::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 2px;
    background: linear-gradient(90deg, #f59e0b, #ef4444);
    border-radius: 2px;
}
.page-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 900;
    color: #0f172a;
    margin: 0 0 0.4rem;
    letter-spacing: -0.04em;
    line-height: 1;
}
.page-subtitle {
    font-size: 14px;
    color: #64748b;
    font-weight: 400;
    line-height: 1.6;
    max-width: 480px;
}
.page-header-right {
    text-align: right;
    padding-bottom: 4px;
}
.status-live {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 100px;
    padding: 7px 16px;
    font-family: 'Fira Code', monospace;
    font-size: 11px;
    color: #16a34a;
    font-weight: 500;
}
.status-live::before {
    content: '';
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Idle State ── */
.idle-state {
    background: linear-gradient(135deg, #fafafa 0%, #f8fafc 100%);
    border: 2px dashed #e2e8f0;
    border-radius: 20px;
    padding: 60px 40px;
    text-align: center;
    margin: 1rem 0 2rem;
}
.idle-icon { font-size: 48px; margin-bottom: 16px; }
.idle-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}
.idle-sub { font-size: 14px; color: #94a3b8; max-width: 380px; margin: 0 auto; line-height: 1.6; }

/* ── KPI Cards ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.75rem;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card:hover {
    box-shadow: 0 8px 30px rgba(0,0,0,0.07);
    transform: translateY(-2px);
}
.kpi-card-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.accent-amber  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.accent-red    { background: linear-gradient(90deg, #ef4444, #f97316); }
.accent-green  { background: linear-gradient(90deg, #10b981, #34d399); }
.accent-blue   { background: linear-gradient(90deg, #3b82f6, #6366f1); }
.kpi-label {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1;
    letter-spacing: -0.03em;
    margin-bottom: 5px;
}
.kpi-sub { font-size: 12px; color: #94a3b8; }

/* ── Result cards ── */
.result-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 1.75rem;
}
.result-card {
    background: #0f172a;
    border-radius: 18px;
    padding: 26px 28px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top right, rgba(245,158,11,0.12), transparent 60%);
}
.result-label {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}
.result-value {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 34px;
    font-weight: 900;
    color: #f1f5f9;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 6px;
}
.result-value.highlight { color: #fbbf24; }
.result-sub { font-size: 12px; color: #475569; }
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 100px;
    font-family: 'Fira Code', monospace;
    font-size: 11px;
    font-weight: 500;
    margin-top: 8px;
}
.risk-low    { background: rgba(16,185,129,0.15); color: #34d399; }
.risk-medium { background: rgba(245,158,11,0.15); color: #fbbf24; }
.risk-high   { background: rgba(239,68,68,0.15);  color: #f87171; }

/* ── Panels ── */
.panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 1.5rem;
    height: 100%;
}
.panel-dark {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 1.5rem;
}
.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
}
.panel-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
}
.panel-title-light {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}
.panel-pill {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    color: #64748b;
    background: #f1f5f9;
    border-radius: 100px;
    padding: 3px 10px;
    letter-spacing: 0.06em;
}
.panel-pill-dark {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    color: #475569;
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    padding: 3px 10px;
    letter-spacing: 0.06em;
}

/* ── Strategy Card ── */
.strategy-item {
    display: flex;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    align-items: flex-start;
}
.strategy-item:last-child { border-bottom: none; }
.strategy-icon {
    width: 36px; height: 36px; flex-shrink: 0;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.strategy-key {
    font-family: 'Fira Code', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 3px;
}
.strategy-val {
    font-size: 13px;
    color: #cbd5e1;
    font-weight: 500;
    line-height: 1.5;
}

/* ── Summary prose ── */
.summary-prose {
    font-size: 14px;
    line-height: 1.8;
    color: #475569;
    background: #f8fafc;
    border-radius: 12px;
    padding: 18px 20px;
    border-left: 4px solid #f59e0b;
    margin-bottom: 1.5rem;
}
.summary-prose strong { color: #0f172a; font-weight: 600; }

/* ── Checklist ── */
.checklist-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.check-item {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.check-mark {
    width: 28px; height: 28px; flex-shrink: 0;
    background: #22c55e;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    color: white;
}
.check-text { font-size: 13px; font-weight: 600; color: #166534; }

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-left { font-size: 12px; color: #94a3b8; }
.footer-right { display: flex; gap: 10px; }
.tech-tag {
    font-size: 10px;
    font-family: 'Fira Code', monospace;
    color: #64748b;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 3px 9px;
    letter-spacing: 0.04em;
}

/* ── Misc ── */
[data-testid="stSpinner"] { color: #f59e0b !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">
            <div class="sidebar-logo-mark">◈</div>
            <div class="sidebar-logo-name">PriceIQ</div>
        </div>
        <div class="sidebar-tagline">DYNAMIC PRICING INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Product Signal</div>', unsafe_allow_html=True)
    product_category = st.selectbox(
        "Product Category",
        ["Electronics", "Clothing", "Beauty", "Home & Kitchen", "Sports"],
        help="The product segment for pricing analysis"
    )
    competitor_price = st.number_input(
        "Competitor Price (₹)",
        min_value=50, max_value=10000, value=500, step=10,
        help="Current market benchmark price"
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Inventory & Demand</div>', unsafe_allow_html=True)
    inventory = st.slider("Inventory Level (units)", 10, 500, 100)
    quantity  = st.slider("Units Sold / Demand", 1, 50, 10)
    discount  = st.slider("Discount (%)", 0, 50, 10)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Business Strategy</div>', unsafe_allow_html=True)
    business_goal = st.selectbox(
        "Business Objective",
        ["Maximize Revenue", "Clear Inventory", "Stay Competitive", "Increase Demand"]
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    predict_btn = st.button("◈  Run Pricing Engine", use_container_width=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px; color:#1e3a5f; line-height:1.7; padding: 0 0.2rem; font-family:'Fira Code',monospace;">
        ML model + business logic layer<br>
        adjusts pricing for demand signals,<br>
        inventory levels & market position.
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE HEADER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-header-left">
        <div class="page-eyebrow">AI-POWERED PRICING</div>
        <div class="page-title">Dynamic Pricing<br>Intelligence</div>
        <div class="page-subtitle">Real-time AI pricing recommendations that balance revenue, inventory, and competitive positioning.</div>
    </div>
    <div class="page-header-right">
        <div class="status-live">ENGINE READY</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── INPUT KPI STRIP ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-card-accent accent-amber"></div>
        <div class="kpi-label">Inventory Level</div>
        <div class="kpi-value">{inventory}</div>
        <div class="kpi-sub">units in stock</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-card-accent accent-red"></div>
        <div class="kpi-label">Demand Signal</div>
        <div class="kpi-value">{quantity}</div>
        <div class="kpi-sub">units sold</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-card-accent accent-blue"></div>
        <div class="kpi-label">Competitor Price</div>
        <div class="kpi-value">₹{competitor_price:,}</div>
        <div class="kpi-sub">market benchmark</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-card-accent accent-green"></div>
        <div class="kpi-label">Discount Applied</div>
        <div class="kpi-value">{discount}%</div>
        <div class="kpi-sub">on final price</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN LOGIC ─────────────────────────────────────────────────────────────
if predict_btn:
    with st.spinner("Fetching ML signal · Applying business logic · Evaluating market position…"):
        try:
            response = requests.get(
                API_URL,
                params={"inventory": inventory, "quantity": quantity},
                timeout=15
            )

            if response.status_code == 200:
                result    = response.json()
                ml_price  = result["predicted_price"]

                # ── Business logic layer ──
                adjusted_price = ml_price
                if business_goal == "Maximize Revenue":
                    adjusted_price *= 1.08
                elif business_goal == "Clear Inventory":
                    adjusted_price *= 0.90
                elif business_goal == "Stay Competitive":
                    adjusted_price = (adjusted_price * 0.7) + (competitor_price * 0.3)
                elif business_goal == "Increase Demand":
                    adjusted_price *= 0.95

                final_price = adjusted_price - (adjusted_price * discount / 100)
                margin_vs_competitor = ((final_price - competitor_price) / competitor_price) * 100

                # ── Risk logic ──
                if inventory < 50 and quantity > 20:
                    market_status = "High Demand + Low Inventory"
                    risk_level    = "High"
                    risk_cls      = "risk-high"
                    risk_icon     = "🔴"
                    strategy      = "Increase price carefully to protect stock availability and avoid stockouts."
                    strategy_icon = "📈"
                elif inventory > 300 and quantity < 10:
                    market_status = "Excess Inventory + Low Demand"
                    risk_level    = "Medium"
                    risk_cls      = "risk-medium"
                    risk_icon     = "🟡"
                    strategy      = "Use discount-led pricing to improve sales velocity and reduce holding costs."
                    strategy_icon = "📦"
                elif competitor_price < final_price:
                    market_status = "Competitor Undercutting"
                    risk_level    = "Medium"
                    risk_cls      = "risk-medium"
                    risk_icon     = "🟡"
                    strategy      = "Blend ML price with competitor benchmark to remain competitive in market."
                    strategy_icon = "⚖️"
                else:
                    market_status = "Stable Pricing Condition"
                    risk_level    = "Low"
                    risk_cls      = "risk-low"
                    risk_icon     = "🟢"
                    strategy      = "Maintain balanced price recommendation. Market conditions are favorable."
                    strategy_icon = "✅"

                # ─ Result KPI cards ──────────────────────────────────────
                st.markdown(f"""
                <div class="result-row">
                    <div class="result-card">
                        <div class="result-label">ML Predicted Price</div>
                        <div class="result-value">₹{ml_price:,.2f}</div>
                        <div class="result-sub">Raw model output</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Final Recommended Price</div>
                        <div class="result-value highlight">₹{final_price:,.2f}</div>
                        <div class="result-sub">After goal adjust + {discount}% discount</div>
                    </div>
                    <div class="result-card">
                        <div class="result-label">Risk Assessment</div>
                        <div class="result-value" style="font-size:20px; padding-top:6px;">
                            <span class="risk-badge {risk_cls}">{risk_icon} {risk_level} Risk</span>
                        </div>
                        <div class="result-sub" style="margin-top:8px;">{market_status}</div>
                        <div style="margin-top:6px; font-size:12px; color:#475569;">
                            vs competitor: 
                            <span style="color:{'#f87171' if margin_vs_competitor > 0 else '#34d399'}; font-family:'Fira Code',monospace; font-weight:600;">
                                {'+' if margin_vs_competitor > 0 else ''}{margin_vs_competitor:.1f}%
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ─ Chart + Strategy row ──────────────────────────────────
                col_chart, col_strat = st.columns([3, 2], gap="large")

                with col_chart:
                    st.markdown("""
                    <div class="panel">
                        <div class="panel-header">
                            <span class="panel-title">Price Intelligence Comparison</span>
                            <span class="panel-pill">₹ COMPARISON</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    chart_data = pd.DataFrame({
                        "Price Type": ["ML Predicted", "Goal Adjusted", "Final Price", "Competitor"],
                        "Amount (₹)": [round(ml_price,2), round(adjusted_price,2), round(final_price,2), competitor_price]
                    })
                    st.bar_chart(chart_data.set_index("Price Type"), height=280, use_container_width=True)

                with col_strat:
                    strategy_rows = [
                        ("🎯", "#fef3c7", "Business Objective", business_goal),
                        (strategy_icon, "#f0fdf4", "Recommended Action", strategy),
                        ("🛍️", "#eff6ff", "Product Category",   product_category),
                        ("📊", "#fdf4ff", "Margin vs Competitor",f"{'+' if margin_vs_competitor > 0 else ''}{margin_vs_competitor:.1f}%"),
                    ]
                    rows_html = ""
                    for icon, bg, key, val in strategy_rows:
                        rows_html += f"""
                        <div class="strategy-item">
                            <div class="strategy-icon" style="background:{bg};">{icon}</div>
                            <div>
                                <div class="strategy-key">{key}</div>
                                <div class="strategy-val">{val}</div>
                            </div>
                        </div>
                        """
                    with st.container():
                        st.markdown("### 🧠 Strategy Playbook")
                        st.caption("AI Analysis")

                        st.write("**🎯 Business Objective:**", business_goal)
                        st.write("**📊 Recommended Action:**", strategy)
                        st.write("**🛍️ Product Category:**", product_category)
                        st.write("**📈 Margin vs Competitor:**",
                                f"{'+' if margin_vs_competitor > 0 else ''}{margin_vs_competitor:.1f}%")

                # ─ Summary Prose ─────────────────────────────────────────
                st.markdown(f"""
                <div class="summary-prose">
                    The pricing engine analysed <strong>{product_category}</strong> with an inventory of 
                    <strong>{inventory} units</strong>, demand signal of <strong>{quantity} units sold</strong>, 
                    and competitor benchmark of <strong>₹{competitor_price:,}</strong>. Operating under the 
                    <strong>{business_goal}</strong> objective, the model produced an ML price of 
                    <strong>₹{ml_price:,.2f}</strong>, adjusted to <strong>₹{adjusted_price:,.2f}</strong> 
                    post goal-weighting, and <strong>₹{final_price:,.2f}</strong> after applying the 
                    {discount}% discount. Market condition: <strong>{market_status}</strong> · 
                    Risk: <strong>{risk_level}</strong>.
                </div>
                """, unsafe_allow_html=True)

                # ─ Decision Checklist ─────────────────────────────────────
                st.markdown("""
                <div class="checklist-row">
                    <div class="check-item">
                        <div class="check-mark">✓</div>
                        <div class="check-text">ML Model Prediction Completed</div>
                    </div>
                    <div class="check-item">
                        <div class="check-mark">✓</div>
                        <div class="check-text">Inventory Signal Evaluated</div>
                    </div>
                    <div class="check-item">
                        <div class="check-mark">✓</div>
                        <div class="check-text">Competitor Pricing Compared</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"⚠️ Backend API returned status {response.status_code}. Check your Render deployment.")

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The Render backend may be cold-starting — try again in 30 seconds.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot reach backend API. Verify the Render service is running.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

else:
    # ─ Idle State ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="idle-state">
        <div class="idle-icon">◈</div>
        <div class="idle-title">Engine Standing By</div>
        <div class="idle-sub">Configure your product signals and business objective in the sidebar, then click <strong>Run Pricing Engine</strong> to generate an AI pricing decision.</div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">Built by <strong>Sahana Patil</strong> · PriceIQ Dynamic Pricing Intelligence Platform</div>
    <div class="footer-right">
        <span class="tech-tag">Python</span>
        <span class="tech-tag">Streamlit</span>
        <span class="tech-tag">REST API</span>
        <span class="tech-tag">ML Pricing</span>
        <span class="tech-tag">Render</span>
    </div>
</div>
""", unsafe_allow_html=True)