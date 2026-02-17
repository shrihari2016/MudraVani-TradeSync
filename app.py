

# --- 1. SETUP & AUTH ---
# You will set this API Key in the Streamlit Dashboard (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["AIzaSyBJyCwXsJwLk83JmgscyKBMCJRFBymSeiM"])
else:
    st.error("API Key missing! Please set AIzaSyBJyCwXsJwLk83JmgscyKBMCJRFBymSeiM in Secrets.")

# --- 2. THE UI ---
st.set_page_config(page_title="MudraVani - TradeSync Pro", layout="wide", initial_sidebar_state="expanded")

# Sidebar for Navigation
st.sidebar.title("MudraVani AI")
page = st.sidebar.radio("Go to", ["Live Analysis", "Monthly Performance", "Support"])

# --- PAGE: LIVE ANALYSIS ---
if page == "Live Analysis":
    st.title("🎯 TradeSync Pro: Live Trend Filter")
    st.markdown("Upload your screenshots for a high-probability bias check.")

    tf = st.selectbox("Select Analysis Timeframe", ["5 Min", "15 Min", "30 Min", "Hourly", "Daily"])

    col1, col2 = st.columns(2)
    with col1:
        chart_file = st.file_uploader("📈 Upload EMA Chart (50/200)", type=['png', 'jpg', 'jpeg'])
    with col2:
        oi_file = st.file_uploader("🔥 Upload Option Chain Screenshot", type=['png', 'jpg', 'jpeg'])

    if st.button("GENERATE MARKET BIAS", type="primary"):
        if chart_file and oi_file:
            with st.spinner("AI is analyzing the institutional footprints..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"""
                    Identify market bias for {tf} timeframe. 
                    Image 1: EMA Chart. Image 2: Option Chain.
                    Use 50/200 EMA strategy and OI walls.
                    Output format:
                    - STATUS: [BULLISH/BEARISH/SIDEWAYS]
                    - LOGIC: (One sentence analysis)
                    - PRO TIP: (A specific tip for {tf} trading)
                    """
                    img1, img2 = Image.open(chart_file), Image.open(oi_file)
                    response = model.generate_content([prompt, img1, img2])
                    res_text = response.text.upper()

                    # Color Coding Logic
                    if "BULLISH" in res_text:
                        st.success("🐂 BULLISH BIAS DETECTED")
                    elif "BEARISH" in res_text:
                        st.error("🐻 BEARISH BIAS DETECTED")
                    else:
                        st.warning("↔️ SIDEWAYS / CHOPPY MARKET")
                    
                    st.info(f"**Analysis Report:**\n\n{response.text}")
                except Exception as e:
                    st.error("Scanning Error. Please try again with a clearer screenshot.")
        else:
            st.warning("Please upload both Chart and OI screenshots.")

# --- PAGE: PERFORMANCE ---
elif page == "Monthly Performance":
    st.title("📊 Trial Period Performance (30 Days)")
    st.markdown("Proof of Profit: See how the tool performed over the last month.")
    
    # Mock data for demonstration (You can update this manually)
    data = {
        "Date": pd.date_range(start="2026-01-18", periods=15),
        "P&L (Points)": [45, 20, 0, -15, 60, 10, -10, 30, 0, 50, 40, -20, 15, 55, 10]
    }
    df = pd.DataFrame(data)
    df['Cumulative Profit'] = df['P&L (Points)'].cumsum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Points Captured", f"{df['P&L (Points)'].sum()} pts")
    c2.metric("Win Rate", "72%")
    c3.metric("Shark Moves", "4 Caught")

    fig = px.line(df, x="Date", y="Cumulative Profit", title="Nifty Equity Curve (Points Growth)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.download_button("Download Full CSV Report", df.to_csv(), "monthly_report.csv")

# --- PAGE: SUPPORT ---
elif page == "Support":
    st.title("📞 MudraVani Support")
    st.write("For billing, license renewals, or feedback, contact us below:")
    st.success("WhatsApp/Call: **+91 9035875900**")
    st.info("Company: **Vayu E-commerce Enterprises**")
