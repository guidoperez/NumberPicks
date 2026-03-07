import pandas as pd


def invoke(input_0: pd.DataFrame) -> pd.DataFrame:
    """Analyze whether the first row's number set repeats later.

    Returns a DataFrame with columns `repeat_found` (bool) and
    `repeating_rows_indices` (list of matching row indices).
    """
    number_cols = ['num1', 'num2', 'num3', 'num4', 'num5', 'cb']

    # Validate input
    if input_0 is None or input_0.empty:
        return pd.DataFrame({'repeat_found': [False], 'repeating_rows_indices': [[]]})

    missing = set(number_cols) - set(input_0.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Use the first row by position (handles non-zero indices)
    first_index = input_0.index[0]
    first_vals = input_0.loc[first_index, number_cols].astype(str).tolist()

    # Use a sorted tuple as the key to preserve multiplicity but ignore order
    first_key = tuple(sorted(first_vals))

    # Build keys for all rows
    keys = input_0[number_cols].astype(str).apply(lambda r: tuple(sorted(r)), axis=1)

    # Find matching indices excluding the first row
    matches = [idx for idx in keys[keys == first_key].index.tolist() if idx != first_index]

    return pd.DataFrame({'repeat_found': [bool(matches)], 'repeating_rows_indices': [matches]})


if __name__ == '__main__':
    try:
        input_0 = pd.read_csv('data_files/cash_4_life_data_file.csv')
    except FileNotFoundError:
        print("Input CSV not found: data_files/cash_4_life_data_file.csv")
        raise

    analysis_result = invoke(input_0)
    print(analysis_result.to_dict(orient='records'))