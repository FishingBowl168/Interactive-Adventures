import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import random

df = pd.read_excel("Output-V3.xlsx")

# 2. Set the aesthetic style
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f0f0f0"})
plt.figure(figsize=(12, 7))

# 3. Create Collision-Aware Swarm Coordinates
#stage_mapping = {"Planned": 1, "Ongoing": 2, "Completed": 3}
#df['Stage_Num'] = df['status'].map(stage_mapping)

final_x = []
final_y = []
final_impacts = [] # Store impact of placed points for collision checking

# Define thresholds for each impact level in coordinate space
# (e.g., impact 3 needs ~0.65 space, impact 1 needs ~0.25)
impact_thresholds = {1: 0.25, 2: 0.45, 3: 0.65}

for i, row in df.iterrows():
    placed = False
    attempts = 0
    stage_center = 1 + (row['stage_numeric'] - 1) * 2
    promising = row['promising']
    current_impact = row['impact']
    
    while not placed and attempts < 50:
        cand_x = stage_center + random.uniform(-0.5, 0.5)
        cand_y = promising * 2 + random.uniform(-1.5, 1.5)
        
        is_collision = False
        for px, py, pi in zip(final_x, final_y, final_impacts):
            dist = np.sqrt((cand_x - px)**2 + (cand_y - py)**2)
            
            # Use the larger threshold of the two points involved
            dynamic_threshold = max(impact_thresholds[pi], impact_thresholds[current_impact])
            
            if dist < dynamic_threshold:
                is_collision = True
                break
        
        if not is_collision:
            final_x.append(cand_x)
            final_y.append(cand_y)
            final_impacts.append(current_impact)
            placed = True
        
        attempts += 1
    
    if not placed: # Fallback
        final_x.append(cand_x)
        final_y.append(cand_y)
        final_impacts.append(current_impact)

df['packed_x'] = final_x
df['packed_y'] = final_y

plot = sns.scatterplot(
    data=df, 
    x='packed_x', 
    y='packed_y', 
    hue='impact', 
    size='impact',        
    sizes=(100, 1500),      
    palette='YlOrRd',       
    alpha=0.8,
    edgecolor='black',    
    linewidth=0.5
)

# 4. Customizing labels and grid
plt.title('Project Portfolio: Impact (Size), Dept (Color), and Stage (Axis)', fontsize=14)
plt.xlabel('') 
plt.xlim(0, 8) # Tighten limits to focus on the 1, 2, 3 clusters
plt.ylim(-4, 4)

# Add soft vertical separators between groups
for x_sep in [2, 4, 6]:
    plt.axvline(x=x_sep, color='gray', linestyle='-', alpha=0.2, linewidth=1)

plt.axhline(y=0, color='gray', linestyle='-', alpha=0.2, linewidth=1)

# Manually set the x-ticks to match the 1, 2, 3 mapping
plt.xticks(ticks=[1, 3, 5, 7], labels=['Ideation', 'POC', 'Pilot', 'Operationalized'])
plt.yticks(ticks=[-2, 2], labels=['Not Promising', 'Promising'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Impact')

# Softening the grid lines 
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()