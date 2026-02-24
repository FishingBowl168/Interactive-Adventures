import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


df = pd.read_excel("Output.xlsx")

# 2. Set the aesthetic style
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f0f0f0"})
plt.figure(figsize=(12, 7))

# 3. Create the Jittered Scatter Plot (Manual Swarm effect)
# swarmplot doesn't support 'size' mapping efficiently, so we use scatterplot with manual jitter.
# User requested range: 0.7 to 1.3 for 1, 1.7 to 2.3 for 2. -> Center at 1, 2, 3 with +/- 0.3 jitter.

stage_mapping = {"Planned": 1, "Ongoing": 2, "Completed": 3}
df['Stage_Num'] = df['status'].map(stage_mapping)

# Add jitter to x-axis (Stage)
df['Stage_Jittered'] = df['Stage_Num'] + np.random.uniform(-0.35, 0.35, len(df))

# Range 0.7 to 1.3 means 1.0 +/- 0.3
df['Impact_Jittered'] = np.random.uniform(0.5, 6.5, len(df))

plot = sns.scatterplot(
    data=df, 
    x='Stage_Jittered', 
    y='Impact_Jittered', 
    hue='impact', 
    size='impact',        
    sizes=(50, 1000),      
    palette='YlOrRd',       
    alpha=0.8,
    edgecolor='black',    
    linewidth=0.5
)

# 4. Customizing labels and grid
plt.title('Project Portfolio: Impact (Size), Dept (Color), and Stage (Axis)', fontsize=14)
plt.xlabel('') 
plt.ylabel('Impact Scale (1-3)')
plt.ylim(0, 7)
plt.xlim(0, 4) 

# Manually set the x-ticks to match the 1, 2, 3 mapping
plt.xticks(ticks=[1, 2, 3], labels=['Planning', 'In progress', 'Completed'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Impact')

# Softening the grid lines 
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()