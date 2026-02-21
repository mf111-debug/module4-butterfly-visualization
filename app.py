import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Change in Butterfly Abundance (2000–2020)")
st.markdown("Each dot represents one species.")

np.random.seed(42)

negative = np.random.normal(-40, 20, 300)
positive = np.random.normal(30, 15, 80)
extreme = np.random.normal(120, 10, 15)

percent_change = np.concatenate([negative, positive, extreme])

df = pd.DataFrame({
    "species": range(len(percent_change)),
    "percent_change": percent_change
})

df["category"] = np.where(df["percent_change"] < 0, "Decline", "Increase")

fig = px.strip(
    df,
    x="percent_change",
    color="category",
    color_discrete_map={
        "Decline": "#E76F51",
        "Increase": "#2A9D8F"
    }
)

fig.update_layout(
    xaxis_title="Percent Change",
    yaxis_visible=False,
    template="simple_white"
)

st.plotly_chart(fig, use_container_width=True)
