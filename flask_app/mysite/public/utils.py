from pandas import DataFrame

def clean_column_names(df: DataFrame) -> DataFrame:
    df.columns = [name.strip().replace('/n', '').replace(' ', '_').lower() for name in df.columns]
    return df
