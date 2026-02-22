import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Change in butterfly abundance, 2000–20")
st.markdown("Each dot represents one species. Data for the contiguous U.S.")

np.random.seed(42)

negative = np.random.normal(-45, 18, 300)
positive = np.random.normal(30, 12, 80)
extreme = np.random.normal(115, 10, 15)

percent_change = np.concatenate([negative, positive, extreme])

df = pd.DataFrame({"percent_change": percent_change})
df["y"] = np.random.uniform(-0.08, 0.08, len(df))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["percent_change"],
    y=df["y"],
    mode="markers",
    marker=dict(
        color=np.where(df["percent_change"] < 0, "#D95F02", "#1B9E77"),
        size=6,
        opacity=0.85
    ),
    hovertemplate="Percent change: %{x:.1f}%<extra></extra>"
))

fig.add_vline(x=0, line_width=1, line_color="black")

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Percent change",
    yaxis_visible=False,
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=40)
)

fig.update_xaxes(showgrid=False)

st.plotly_chart(fig, width="stretch")
