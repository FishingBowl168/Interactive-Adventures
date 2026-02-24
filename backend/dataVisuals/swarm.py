import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


df = pd.read_excel("Output.xlsx")

# 2. Set the aesthetic style
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f0f0f0"})
plt.figure(figsize=(12, 7))

# 3. Create Collision-Aware Swarm Coordinates
stage_mapping = {"Planned": 1, "Ongoing": 2, "Completed": 3}
df['Stage_Num'] = df['status'].map(stage_mapping)

final_x = []
final_y = []
final_impacts = []

# Map impact level to a physical distance threshold (0.25 to 0.65)
threshold_map = {3: 1, 2: 0.4, 1: 0.2}

for i, row in df.iterrows():
    placed = False
    attempts = 0
    stage_center = row['Stage_Num']
    curr_impact = row['impact']
    
    while not placed and attempts < 250:
        candidate_x = stage_center + np.random.uniform(-0.35, 0.35)
        candidate_y = np.random.uniform(0.5, 6.5)
        
        is_collision = False
        for px, py, pi in zip(final_x, final_y, final_impacts):
            dist = np.sqrt((candidate_x - px)**2 + (candidate_y - py)**2)
            
            # Use the larger impact to determine minimum allowed space
            required_dist = max(threshold_map[curr_impact], threshold_map[pi])
            
            if dist < required_dist:
                is_collision = True
                break
        
        if not is_collision:
            final_x.append(candidate_x)
            final_y.append(candidate_y)
            final_impacts.append(curr_impact)
            placed = True
        
        attempts += 1
    
    if not placed:
        final_x.append(candidate_x)
        final_y.append(candidate_y)
        final_impacts.append(curr_impact)

df['packed_x'] = final_x
df['packed_y'] = final_y

plot = sns.scatterplot(
    data=df, 
    x='packed_x', 
    y='packed_y', 
    hue='impact', 
    size='impact',        
    sizes=(50, 1250),      
    palette='YlOrRd',       
    alpha=0.8,
    edgecolor='black',    
    linewidth=0.5
)

# 4. Customizing labels and grid
plt.title('Project Portfolio: Impact (Size), Dept (Color), and Stage (Axis)', fontsize=14)
plt.xlabel('') 
plt.xlim(0.5, 3.5) # Tighten limits to focus on the 1, 2, 3 clusters

# Add soft vertical separators between groups
for x_sep in [1.5, 2.5]:
    plt.axvline(x=x_sep, color='gray', linestyle='-', alpha=0.2, linewidth=1)

# Manually set the x-ticks to match the 1, 2, 3 mapping
plt.xticks(ticks=[1, 2, 3], labels=['Planning', 'In progress', 'Completed'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Impact')

# Softening the grid lines 
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()