import pandas as pd
import numpy as np

# 1. Setup the parameters
n_projects = 80
stages = ['Planning', 'In progress', 'Completed']
departments = ['Tech', 'Marketing', 'Sales', 'Ops'] # Added for the color grouping

# 2. Generate random data
data = {
    'Project': [f'Project {i+1}' for i in range(n_projects)],
    'Impact': np.random.randint(1, 4, n_projects), # Random integers 1 to 5
    'Stage': np.random.choice(stages, n_projects),
    'Department': np.random.choice(departments, n_projects)
}

# 3. Create DataFrame and save
df = pd.DataFrame(data)
df.to_excel('project_data.xlsx', index=False)

print("Sample Excel file 'project_data.xlsx' has been created!")
