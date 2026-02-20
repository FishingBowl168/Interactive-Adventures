import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

# 1. Load Data
df = pd.read_excel('project_data.xlsx')

# 2. Setup Plot
plt.figure(figsize=(14, 8))
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f2f2f2"})

# Map stages to numbers
stage_map = {'Planning': 1, 'In progress': 2, 'Completed': 3}
df['x'] = df['Stage'].map(stage_map) + np.random.uniform(-0.1, 0.1, len(df))
df['y'] = df['Impact'] + np.random.uniform(-0.1, 0.1, len(df))

# 3. Plot Bubbles
# We save the path collections to a variable
paths = plt.scatter(
    df['x'], df['y'], 
    s=df['Impact'] * 200, 
    c=pd.factorize(df['Department'])[0], 
    cmap='Set2', edgecolors='white', alpha=0.8
)

# 4. The "No-Overlap" Magic for Labels
texts = []
for i, txt in enumerate(df['Project']):
    # Only label specific projects to keep it clean, or all of them
    if txt in ['Project 3', 'Project 70']:
        texts.append(plt.text(df['x'].iloc[i], df['y'].iloc[i], txt, fontweight='bold'))

# This single line moves labels so they don't overlap bubbles or each other
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

plt.xticks([1, 2, 3], ['Planning', 'In progress', 'Completed'])
plt.ylim(0, 6)
plt.title("Zero-Overlap Project Visualization")
plt.show()