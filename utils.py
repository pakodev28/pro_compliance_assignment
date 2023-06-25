import pandas as pd
from pandas.errors import ParserError


def get_file_columns(file_path):
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return columns
    except ParserError as error_message:
        raise ParserError(
            f"Error reading file: {error_message}"
        ) from error_message
