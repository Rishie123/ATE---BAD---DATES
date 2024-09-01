import pandas as pd

# Load the new CSV file
file_path = 'ate-900.csv'
data = pd.read_csv(file_path)

# Remove leading and trailing spaces from column names
data.columns = data.columns.str.strip()

# Remove leading and trailing spaces from all cell values
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save the modified DataFrame to a new CSV file
modified_file_path = 'modified_ate_900.csv'
data.to_csv(modified_file_path, index=False)

print(f"Modified file saved as {modified_file_path}")
