import pandas as pd

def compare_sheets(original, amended):
    """
    Compare two dataframes and return the amended dataframe with comments indicating changes.
    """
    # Make copies of the dataframes to avoid modifying the originals
    original_copy = original.copy()
    amended_copy = amended.copy()

    # Add a comment column if it doesn't exist
    if 'Comment' not in amended_copy.columns:
        amended_copy['Comment'] = None

    # Set a unique identifier for comparison, assuming the first column is unique (e.g., "Name")
    identifier = original.columns[0]

    # Identify rows in the original but not in the amended (Removed rows)
    removed_rows = original[~original[identifier].isin(amended[identifier])]
    for index, row in removed_rows.iterrows():
        new_row = row.copy()
        new_row['Comment'] = "Removed"
        amended_copy = pd.concat([amended_copy, pd.DataFrame([new_row])], ignore_index=True)

    # Identify rows in the amended but not in the original (Added rows)
    added_rows = amended[~amended[identifier].isin(original[identifier])]
    for index, row in added_rows.iterrows():
        amended_copy.loc[amended_copy[identifier] == row[identifier], 'Comment'] = "Added"

    # Identify modified rows
    common_rows = original[original[identifier].isin(amended[identifier])]
    for index, row in common_rows.iterrows():
        amended_row = amended.loc[amended[identifier] == row[identifier]]
        if not row.equals(amended_row.iloc[0]):  # Check if rows differ
            amended_copy.loc[amended_copy[identifier] == row[identifier], 'Comment'] = (
                "Amended: " + ", ".join(row[:6].astype(str))
            )

    return amended_copy

# Load the original and amended Excel files
original_path = '/mnt/data/original.xlsx'
amended_path = '/mnt/data/amended.xlsx'

# Read the Excel files
original_df = pd.read_excel(original_path)
amended_df = pd.read_excel(amended_path)

# Perform comparison
result_df = compare_sheets(original_df, amended_df)

# Save the result to a new Excel file for review
result_path = '/mnt/data/result.xlsx'
result_df.to_excel(result_path, index=False)

