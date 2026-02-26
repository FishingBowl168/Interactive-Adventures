import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import random


df = pd.read_excel("Output.xlsx")

# 2. Set the aesthetic style
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f0f0f0"})
plt.figure(figsize=(12, 7))

# 3. Create Collision-Aware Swarm Coordinates
stage_mapping = {"Planned": 1, "Ongoing": 3, "Completed": 5}
df['Stage_Num'] = df['status'].map(stage_mapping)

final_x = []
final_y = []
final_impacts = []
size_ratio = 200
min_dist = size_ratio / 750

for i, row in df.iterrows():
    stage_center = row['Stage_Num']
    placed = False
    
    while not placed:
        cand_x = stage_center + random.uniform(-0.5, 0.5)
        cand_y = random.uniform(-4, 4)
        placed = True
        for np_x, np_y in zip(final_x, final_y):
            if (cand_x - np_x)**2 + (cand_y - np_y)**2 < min_dist:
                placed = False
                break
    
    final_x.append(cand_x)
    final_y.append(cand_y)
    final_impacts.append(row['impact'])

print(final_x)
print(final_y)

plot = sns.scatterplot(
    x=final_x, 
    y=final_y, 
    hue=final_impacts, 
    size=final_impacts,        
    sizes=[1 * size_ratio, 3 * size_ratio, 5 * size_ratio],      
    palette='YlOrRd',       
    alpha=0.7,
    edgecolor='black',    
    linewidth=0
)

# 4. Customizing labels and grid
plt.title('Project Portfolio: Impact (Size), Dept (Color), and Stage (Axis)', fontsize=14)
plt.xlabel('') 
plt.xlim(0, 6) # Tighten limits to focus on the 1, 2, 3 clusters
plt.ylim(-5, 5)

# Add soft vertical separators between groups
for x_sep in [2, 4]:
    plt.axvline(x=x_sep, color='gray', linestyle='-', alpha=0.2, linewidth=1)

# Manually set the x-ticks to match the 1, 2, 3 mapping
plt.xticks(ticks=[1, 3, 5], labels=['Planning', 'In progress', 'Completed'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Impact')

# Softening the grid lines 
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()