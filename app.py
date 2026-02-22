import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Change in butterfly abundance, 2000–20")
st.markdown("Each dot represents one species. Data for the contiguous U.S.")

# ----- Simulated data -----
np.random.seed(42)

negative = np.random.normal(-45, 18, 245)
neutral = np.random.normal(0, 4, 32)
positive = np.random.normal(35, 15, 65)
extreme = np.random.normal(115, 10, 12)

percent_change = np.concatenate([negative, neutral, positive, extreme])

df = pd.DataFrame({"percent_change": percent_change})
df = df.sort_values("percent_change").reset_index(drop=True)

# ----- Category logic -----
def categorize(x):
    if x < -5:
        return "Decline"
    elif x > 5:
        return "Increase"
    else:
        return "Little change"

df["category"] = df["percent_change"].apply(categorize)

# ----- Beeswarm stacking -----
y_positions = []
stack_height = 0.04
previous_x = None
stack = 0

for x in df["percent_change"]:
    if previous_x is None or abs(x - previous_x) > 2:
        stack = 0
    else:
        stack += 1
    y_positions.append((stack % 12) * stack_height)
    previous_x = x

df["y"] = y_positions

# ----- Colors -----
color_map = {
    "Decline": "#D95F02",
    "Little change": "#CFC2A5",
    "Increase": "#6A8F3F"
}

colors = df["category"].map(color_map)

# ----- Plot -----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["percent_change"],
    y=df["y"],
    mode="markers",
    marker=dict(
        color=colors,
        size=9,
        line=dict(width=1, color="black")
    ),
    hovertemplate="Percent change: %{x:.1f}%<extra></extra>"
))

# Vertical reference lines
fig.add_vline(x=0, line_width=1, line_color="black")

# Layout
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Percent change",
    yaxis_visible=False,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig.update_xaxes(
    tickvals=[-100, -50, 0, 50, 100],
    ticktext=["-100%", "-50", "0", "+50", "+100"],
    showgrid=False
)

# Annotations
fig.add_annotation(x=-60, y=0.6, text="245 species decreased",
                   showarrow=False, font=dict(size=18))

fig.add_annotation(x=0, y=0.6, text="32 showed little change",
                   showarrow=False, font=dict(size=18))

fig.add_annotation(x=70, y=0.6, text="65 increased",
                   showarrow=False, font=dict(size=18))

st.plotly_chart(fig, width="stretch")
