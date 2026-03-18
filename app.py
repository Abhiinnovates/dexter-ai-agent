import streamlit as st
import uuid
import pandas as pd
from graph_pipeline import research_app

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Financial AI Research Assistant",
    page_icon="✨",
    layout="wide",
)

# 2. INJECT MODERN NEO-FINTECH CSS (GLASSMORPHISM)
modern_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* Global Font and Background */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0b0f19 !important; /* Deep navy/slate background */
    color: #e2e8f0 !important;
}

/* Hide default Streamlit headers and footers */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sleek Gradient Title */
.gradient-title {
    font-size: 3rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #00E1D9, #5D8BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

/* Subtitle */
.modern-subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    font-weight: 300;
    text-align: center;
    margin-bottom: 3rem;
    letter-spacing: 0.5px;
}

/* User Input Bubble - Glassmorphism */
.user-bubble {
    background: rgba(93, 139, 250, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(93, 139, 250, 0.3);
    border-radius: 12px 12px 0px 12px;
    padding: 15px 20px;
    color: #ffffff;
    font-weight: 400;
    margin-bottom: 1rem;
    width: fit-content;
    float: right;
    clear: both;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Clearfix for floating user bubbles */
.clearfix::after {
    content: "";
    clear: both;
    display: table;
}

/* Tool Execution Chips */
.tool-chip {
    display: inline-block;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 5px 15px;
    font-size: 0.85rem;
    color: #94a3b8;
    margin: 4px;
    backdrop-filter: blur(4px);
}
.tool-chip.success {
    border-color: rgba(0, 225, 217, 0.4);
    color: #00E1D9;
}

/* Section Dividers */
.section-divider {
    color: #5D8BFA;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 0.5rem;
}
</style>
"""
st.markdown(modern_css, unsafe_allow_html=True)

# 3. RENDER THE BRAND NEW HEADER
st.markdown(
    '<div class="gradient-title">Your Financial AI Research Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="modern-subtitle">Next-generation quantitative analysis and market intelligence.</div>',
    unsafe_allow_html=True,
)

# 4. INITIALIZE SESSION STATE
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome. What market trends, companies, or financial data can I analyze for you today?",
        }
    ]

# 5. RENDER CHAT HISTORY
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="clearfix"><div class="user-bubble">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(message["content"])

# 6. HANDLE NEW USER INPUT
if user_input := st.chat_input("Ask a financial question..."):
    # 1. Show the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Build the FULL chat history string
    full_chat_history = "\n".join(
        [
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in st.session_state.messages
        ]
    )

    with st.chat_message("assistant"):
        with st.spinner("Analyzing market data..."):

            # 3. Build a CLEAN slate
            current_state = {
                "question": user_input,
                "chat_history": full_chat_history,
                "companies": [],
                "tickers": [],  # <--- ADD THIS LINE!
                "research_data": [],
            }

            # 4. Generate a unique thread ID for this specific question
            # This completely kills the "Tesla/BYD Ghost" bug forever!
            unique_run_id = f"run_{len(st.session_state.messages)}"
            config = {"configurable": {"thread_id": unique_run_id}}

            from graph_pipeline import research_app

            final_state = research_app.invoke(current_state, config=config)

            # 5. Display the final report
            report = final_state.get("report", "Error generating report.")
            st.markdown(report)

            # 6. Save the AI's response
            st.session_state.messages.append({"role": "assistant", "content": report})
    # 7. AGENT EXECUTION WITH MODERN STATUS CHIPS
    with st.container():
        status_placeholder = st.empty()

        tool_logs = ""
        for output in research_app.stream(current_state, config=config):
            for node_name, state_update in output.items():
                # Modern pill-shaped status indicators
                tool_logs += (
                    f"<span class='tool-chip success'>✓ {node_name} completed</span>"
                )
                status_placeholder.markdown(tool_logs, unsafe_allow_html=True)

        final_state = research_app.get_state(config).values
        final_reply = final_state.get("report", "Error generating report.")

        # Clear the tool logs and show the final response
        status_placeholder.empty()

        # Display the text response
        st.markdown(final_reply)
        st.session_state.messages.append({"role": "assistant", "content": final_reply})

        # ---------------------------------------------------------
        # 📊 VISUALIZATION BLOCK: Modern Fintech Charts
        # ---------------------------------------------------------
        import pandas as pd
        import plotly.graph_objects as go

        raw_data_list = final_state.get("research_data", [])

        for data_item in raw_data_list:
            if "Live_Indian_IPOs" in data_item:
                ipo_data = data_item["Live_Indian_IPOs"]
                if (
                    len(ipo_data) > 0
                    and "error" not in ipo_data[0]
                    and "message" not in ipo_data[0]
                ):
                    st.markdown(
                        "<div class='section-divider'>Live IPO Market Data</div>",
                        unsafe_allow_html=True,
                    )
                    st.dataframe(pd.DataFrame(ipo_data), use_container_width=True)

            for key, value in data_item.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "historical_prices" in item:
                            ticker_name = item["ticker"]
                            timeframe = item.get("timeframe", "Data")
                            st.markdown(
                                f"<div class='section-divider'>{timeframe.upper()} Price History: {ticker_name}</div>",
                                unsafe_allow_html=True,
                            )

                            df_prices = pd.DataFrame(item["historical_prices"])
                            if not df_prices.empty:
                                df_prices["Date"] = pd.to_datetime(df_prices["Date"])

                                # 🟢 BUILD A SLEEK FINTECH CHART
                                fig = go.Figure()
                                fig.add_trace(
                                    go.Scatter(
                                        x=df_prices["Date"],
                                        y=df_prices["Close"],
                                        mode="lines",
                                        line=dict(
                                            color="#00E1D9", width=2.5
                                        ),  # Sleek Cyan Line
                                        fill="tozeroy",
                                        fillcolor="rgba(0, 225, 217, 0.08)",  # Subtle fade
                                        name="Close",
                                    )
                                )

                                # Premium dark-mode layout
                                fig.update_layout(
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(0,0,0,0)",
                                    font=dict(
                                        family="Inter, sans-serif", color="#94a3b8"
                                    ),
                                    xaxis=dict(
                                        showgrid=True,
                                        gridcolor="rgba(255,255,255,0.05)",
                                    ),
                                    yaxis=dict(
                                        showgrid=True,
                                        gridcolor="rgba(255,255,255,0.05)",
                                        tickprefix="$",
                                    ),
                                    margin=dict(l=0, r=0, t=10, b=0),
                                    hovermode="x unified",
                                )

                                unique_chart_key = (
                                    f"price_chart_{ticker_name}_{uuid.uuid4().hex[:8]}"
                                )
                                st.plotly_chart(
                                    fig, use_container_width=True, key=unique_chart_key
                                )
