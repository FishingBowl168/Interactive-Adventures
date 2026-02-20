import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 1. Create dummy data
np.random.seed(42)
n_projects = 80 # Adjust total number if needed

data = {
    'Stage': np.random.choice(['Planning', 'In progress', 'Completed'], n_projects),
    'Impact': np.random.choice([1, 2, 3, 4, 5], n_projects), # Impact range 1 to 5
    'Project': np.arange(1, n_projects + 1)
}

df = pd.DataFrame(data)

# 2. Setup computation for variable width bars
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# Sort stages to ensure consistent order
stages = sorted(df['Stage'].unique())

# Setup figure
fig, ax = plt.subplots(figsize=(14, len(stages) * 2.5))
ax.set_facecolor("#f0f0f0")

# Colormap settings
cmap = plt.get_cmap('YlOrRd')
norm = mcolors.Normalize(vmin=1, vmax=5)

# 3. Plotting
bar_height = 0.8
y_positions = np.arange(len(stages))

for i, stage in enumerate(stages):
    # Filter and sort projects for this stage
    stage_projects = df[df['Stage'] == stage].sort_values('Project')
    n_items = len(stage_projects)
    
    if n_items == 0:
        continue
        
    # Calculate width for each project in this stage to fill the total width (1.0)
    width = 1.0 / n_items
    
    current_x = 0
    y = i
    
    for _, row in stage_projects.iterrows():
        impact = row['Impact']
        pid = int(row['Project'])
        color = cmap(norm(impact))
        
        # Create rectangle
        rect = patches.Rectangle(
            (current_x, y),  # (x, y) bottom-left corner
            width,           # width
            bar_height,      # height
            linewidth=1,
            edgecolor='white',
            facecolor=color
        )
        ax.add_patch(rect)
        
        # Add annotation if width is sufficient (basic check)
        # We always add it, matplotlib clips if it's too huge, but usually it's fine
        # Center text
        text_label = f"{pid}\n({impact})"
        
        # Dynamic font size based on number of items
        font_size = 10 if n_items < 20 else 8 if n_items < 40 else 6
        
        ax.text(
            current_x + width/2, 
            y + bar_height/2, 
            text_label, 
            ha='center', 
            va='center', 
            fontsize=font_size,
            color='black' if impact < 4 else 'white' # Contrast text color
        )
        
        current_x += width

# 4. Customize Axes
ax.set_ylim(-0.2, len(stages))
ax.set_xlim(0, 1)

# Set Y ticks to stage names
ax.set_yticks(y_positions + bar_height/2)
ax.set_yticklabels(stages, fontsize=12)

# Remove X ticks as they represent percentage/proportion
ax.set_xticks([])
ax.set_xlabel("Projects (Normalized Width)", fontsize=12)
ax.set_ylabel("Project Stage", fontsize=12)

# Add Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
cbar.set_label('Impact Score (1-5)', rotation=90)

plt.title('Project Impact Heatmap: Variable Width per Stage', fontsize=16)
plt.tight_layout()
plt.show()
