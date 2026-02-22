import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.markdown("## Change in butterfly abundance, 2000–20")
st.markdown("Each dot represents one species. Data for the contiguous U.S.")

np.random.seed(42)

negative = np.random.normal(-45, 18, 245)
neutral = np.random.normal(0, 4, 32)
positive = np.random.normal(35, 15, 65)
extreme = np.random.normal(115, 10, 12)

percent_change = np.concatenate([negative, neutral, positive, extreme])

df = pd.DataFrame({"percent_change": percent_change})

def categorize(x):
    if x < -5:
        return "Decline"
    elif x > 5:
        return "Increase"
    else:
        return "Little change"

df["category"] = df["percent_change"].apply(categorize)

color_scale = alt.Scale(
    domain=["Decline", "Little change", "Increase"],
    range=["#D95F02", "#CFC2A5", "#6A8F3F"]
)

chart = (
    alt.Chart(df)
    .mark_circle(size=120, stroke="black", strokeWidth=0.5)
    .encode(
        x=alt.X(
            "percent_change:Q",
            axis=alt.Axis(
                values=[-100, -50, 0, 50, 100],
                labelExpr="datum.value == -100 ? '-100%' : datum.value == 100 ? '+100' : datum.value"
            ),
            title="Percent change"
        ),
        y=alt.Y("category:N", axis=None),
        color=alt.Color("category:N", scale=color_scale, legend=None),
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)
