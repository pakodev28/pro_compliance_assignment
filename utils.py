import numpy as np
import pandas as pd
from pandas.errors import ParserError


def get_file_columns(file_path):
    """
    Reads a CSV file and returns a list of column names.

    Params:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of column names in the CSV file.

    Raises:
        ParserError: Raises if there's an issue while reading the file.
    """
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return columns
    except ParserError as error_message:
        raise ParserError(
            f"Error reading file: {error_message}"
        ) from error_message


def sort_data(df, columns, ascending):
    """
    Sorts the data in a DataFrame based on the specified columns.

    Params:
        df: The DataFrame to be sorted.
        columns (list): Columns to sort by.
        ascending (list): Sorting direction for each column
        (True for ascending, False for descending).

    Examples:
        sort_data(df, ['Column'], [True])
        sort_data(df, ['Column1', 'Column2'], [True, False])
    """
    if columns:
        df.sort_values(columns, ascending=ascending, inplace=True)
    return df


def filter_data(df, conditions):
    """
    Filtering of a DataFrame based on specified conditions.

    Params:
        df: The source DataFrame to be filtered.
        conditions: A list of filtering conditions(column, operator, value).

    Returns:
        Filtered DataFrame.
    """
    for column, operator, value in conditions:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in file")

        column_dtype = df[column].dtype
        if column_dtype in (np.int64, np.float64):
            try:
                value = column_dtype.type(value)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid value '{value}' for column '{column}'"
                ) from exc
        elif isinstance(column_dtype, object):
            if operator == "eq":
                df = df[df[column] == value]
            elif operator == "ne":
                df = df[df[column] != value]
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        else:
            raise ValueError(f"Unsupported data type for column '{column}'")

        if operator == "eq":
            df = df[df[column] == value]
        elif operator == "gt":
            df = df[df[column] > value]
        elif operator == "ge":
            df = df[df[column] >= value]
        elif operator == "lt":
            df = df[df[column] < value]
        elif operator == "le":
            df = df[df[column] <= value]
        elif operator == "ne":
            df = df[df[column] != value]
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    return df
