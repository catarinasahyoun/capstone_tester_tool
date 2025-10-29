def read_data(file_path):
    """Read data from a specified file path."""
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def write_data(file_path, data):
    """Write data to a specified file path."""
    with open(file_path, 'w') as file:
        file.write(data)

def append_data(file_path, data):
    """Append data to a specified file path."""
    with open(file_path, 'a') as file:
        file.write(data)

def read_csv(file_path):
    """Read data from a CSV file."""
    import pandas as pd
    return pd.read_csv(file_path)

def write_csv(file_path, dataframe):
    """Write a DataFrame to a CSV file."""
    import pandas as pd
    dataframe.to_csv(file_path, index=False)