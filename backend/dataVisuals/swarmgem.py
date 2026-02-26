import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import random

# Load data (using dummy data for demonstration)
df = pd.read_excel("Output-V4.xlsx")
# data = {'stage_numeric': [1, 2, 3, 4] * 10, 'promising': [random.uniform(-1, 1) for _ in range(40)], 'impact': [1, 2, 3] * 13 + [1]}
# df = pd.DataFrame(data)

print(df.count())

impact_palette = [
    "O",
    "g", 
    "b",   
    "r"
]

# 1. Set the aesthetic style - 'white' removes the default grid background
sns.set_theme(style="white")
fig, ax = plt.subplots(figsize=(14, 8))

final_x, final_y, final_impacts, final_colors = [], [], [], []
size_ratio = 200
fnt_size = 16

for i, row in df.iterrows():
    # Centering logic to match your tick positions [1, 3, 5, 7]
    stage_center = 1 + (row['stage_numeric'] - 1) * 2
    cand_x = stage_center + random.uniform(-0.75, 0.75)
    cand_y = row['promising'] * 2 + random.uniform(-1.5, 1.5)
    
    final_x.append(cand_x)
    final_y.append(cand_y)
    final_impacts.append(row['impact'])
    # Assign color based on stage to match the label boxes
    final_colors.append(impact_palette[int(row['stage_numeric'])-1])

# 2. Draw the Scatter Plot
plot = sns.scatterplot(
    x=final_x, y=final_y, hue=final_colors, size=final_impacts,
    sizes=[1 * size_ratio, 2.5 * size_ratio, 4 * size_ratio],
    palette={c: c for c in impact_palette}, alpha=1, ax=ax, 
    legend=False
)

# --- 3. ADD COLORED LABEL BOXES (The "Funnel" Labels) ---
# Define positions and colors matching your reference image
label_configs = [
    {"label": "Ideation", "color": "#ffb338", "x_start": 0.1},
    {"label": "POC/prototyping","color": "#96d13d", "x_start": 2.1},
    {"label": "Pilot", "color": "#2ab2bc", "x_start": 4.1},
    {"label": "Operationalized", "color": "#e64b43", "x_start": 6.1},
]

for cfg in label_configs:
    # Add the colored rectangle at the bottom
    rect = patches.FancyBboxPatch(
        (cfg["x_start"], -5), 1.8, 1.2, # (x, y), width, height
        boxstyle="round,pad=0.1", color=cfg["color"], ec="none", zorder=2
    )
    ax.add_patch(rect)
    
    # Add the text inside the box
    ax.text(
        cfg["x_start"] + 0.9, -4.4, cfg["label"], 
        color='white', ha='center', va='center', fontweight='bold', fontsize=fnt_size
    )

# 4. Formatting to match the clean look
plt.xlim(0, 8)
plt.ylim(-5, 4) # Expanded bottom limit to make room for boxes

# Remove standard axes and ticks for that "infographic" feel
ax.set_xticks([]) # Remove default x-ticks
ax.set_yticks([])
sns.despine(left=True, bottom=True)

# --- ADD IN-GRAPH Y-AXIS LABELS ---
# Positioned at x=0.1 (near the left) and slightly above/below the y=0 line
ax.text(0.1, 3.5, "Promising", fontsize=fnt_size, fontweight='bold', 
        color='#6a6a6a', va='bottom', ha='left', alpha=0.6)

ax.text(0.1, -3.25, "KIV", fontsize=fnt_size, fontweight='bold', 
        color='#6a6a6a', va='top', ha='left', alpha=0.6)

# Add soft vertical separators (as seen in your reference)
for x_sep in [2, 4, 6]:
    plt.axvline(x=x_sep, color='#e0e0e0', linestyle='-', linewidth=1.5, zorder=1)


plt.axhline(y=0, color='gray', linestyle='-', alpha=0.2, linewidth=1)
plt.tight_layout()
plt.show()