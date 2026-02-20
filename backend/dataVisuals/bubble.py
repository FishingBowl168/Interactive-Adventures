import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 1. Create dummy data
np.random.seed(42)
n_projects = 80

data = {
    'Stage': np.random.choice(['Planning', 'In progress', 'Completed'], n_projects),
    'Impact': np.random.choice([1, 2, 3, 4, 5], n_projects), # Impact range 1 to 5
    'Department': np.random.choice(['Tech', 'Marketing', 'Sales', 'Ops'], n_projects)
}

df = pd.DataFrame(data)

# 2. Set the aesthetic style
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f0f0f0"})
plt.figure(figsize=(12, 7))

# 3. Create the Jittered Bubble Plot using scatterplot
# WORKAROUND: Map stages to numbers and add random noise (jitter) manually
stage_mapping = {'Planning': 0, 'In progress': 1, 'Completed': 2}
df['Stage_Num'] = df['Stage'].map(stage_mapping)
# Add jitter to x-axis
df['Stage_Jittered'] = df['Stage_Num'] + np.random.uniform(-0.15, 0.15, len(df))

plot = sns.scatterplot(
    data=df, 
    x='Stage_Jittered', 
    y='Impact', 
    hue='Department', 
    size='Impact',         # Map size to Impact
    sizes=(50, 400),       # Control the range of bubble sizes (min_area, max_area)
    palette='Set2',       
    alpha=0.7,
)

# Manually set the x-ticks to match the original categories
plt.xticks(ticks=[0, 1, 2], labels=['Planning', 'In progress', 'Completed'])

# 4. Customizing labels and grid
plt.title('Project Portfolio: Impact (Size), Dept (Color), and Stage (Axis)', fontsize=14)
plt.xlabel('') # Removing x-label as stages are self-explanatory
plt.ylabel('Impact Scale (1-5)')
plt.ylim(0, 6)   # Giving some breathing room for the bubbles
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Department')

# Softening the grid lines to match your image
plt.grid(axis='y', linestyle='--', alpha=0.6)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()