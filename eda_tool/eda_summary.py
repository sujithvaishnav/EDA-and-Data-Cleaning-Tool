def dataset_summary(df):
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "types": df.dtypes,
        "summary": df.describe()
    }
