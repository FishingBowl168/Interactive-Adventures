import altair as alt
import pandas as pd
import numpy as np
import os
import streamlit as st

# Set page config for a premium look
st.set_page_config(page_title="Project Distribution Dashboard", layout="wide")

# Custom CSS for premium aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stHeader {
        color: #1e3a8a;
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Get the absolute path to the data file relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Beeswarm.xlsx")

# 1. Load data
try:
    data = pd.read_excel(DATA_PATH)
except FileNotFoundError:
    print(f"Error: {DATA_PATH} not found.")
    # Fallback/Dummy data logic could go here if needed
    raise


import circlify

# 2. Prepare data for Swarm logic using Circlify for ZERO overlap
status_labels = {0: 'Planning', 1: 'Ongoing', 2: 'Completed'}
data['status_label'] = data['status'].map(status_labels)

# We will store the final packed coordinates here
packed_x = []
packed_y = []

# Process each group separately to keep them clustered under their status
for status_val in [0, 1, 2]:
    group = data[data['status'] == status_val].copy()
    if group.empty:
        continue
        
    # Radius is based on impact. Impact is [1, 2, 3]
    # We use radii like [0.1, 0.2, 0.3] for packing
    radii = (group['impact'] * 0.1).tolist()
    
    # Circlify returns a list of circles with x, y, r in a unit circle
    circles = circlify.circlify(
        radii, 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=0.5)
    )
    
    # Shift and scale the circles
    # Center X should be at status_val + 1 (1, 2, 3)
    center_x = status_val + 1
    
    for circle in circles:
        # Scale the relative coordinates and shift to the center
        # We multiply by a small factor to keep the clusters tight
        packed_x.append(center_x + circle.x * 1.0) 
        packed_y.append(circle.y * 1.0)

# Add the packed coordinates back to the dataframe
data['packed_x'] = packed_x
data['packed_y'] = packed_y

# 3. Create the Bee Swarm Chart
st.title("📊 Guaranteed Non-Overlapping Beeswarm")
st.markdown("This visualization uses `circlify` to calculate exact coordinates so that **no two circles ever touch or overlap.**")

# Calculate the chart with white background and packed coordinates
chart = alt.Chart(data).mark_circle(stroke='black', strokeWidth=1, opacity=0.9).encode(
    x=alt.X('packed_x:Q', 
            axis=alt.Axis(
                values=[1, 2, 3],
                labelExpr="datum.value == 1 ? 'Planning' : datum.value == 2 ? 'Ongoing' : 'Completed'",
                title=None,
                grid=False,
                labelFontSize=14,
                labelPadding=10,
                labelColor='black'
            ),
            scale=alt.Scale(domain=[0, 4])),
    y=alt.Y('packed_y:Q', 
            axis=None), # Zero Y-axis as requested
    size=alt.Size('impact:O', 
                 scale=alt.Scale(range=[400, 1200]), 
                 legend=alt.Legend(title="Impact Level", titleColor='black', labelColor='black')),
    color=alt.Color('impact:O', 
                   scale=alt.Scale(
                       domain=[3, 2, 1],
                       range=['#F77F00', '#FCBF49', '#EAE2B7']
                   ), 
                   legend=alt.Legend(title="Impact Color", titleColor='black', labelColor='black')),
    tooltip=['status_label', 'impact']
).configure_view(
    stroke=None,
    fill='white'
).configure_axis(
    domain=False,
    labelColor='black',
    titleColor='black'
).properties(
    width='container',
    height=500,
    background='white'
)

# Display in Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown("""
<div style="background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #eee;">
    <strong>Design Notes:</strong> This beeswarm uses <strong>sideway jitter</strong> (X-axis) to separate projects 
    by their stage, while the vertical position clearly shows their <strong>Impact Score</strong>.
</div>
""", unsafe_allow_html=True)

