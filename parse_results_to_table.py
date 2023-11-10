import os
import argparse
from prettytable import PrettyTable

def create_table(log_directory):
    """
    Creates a table with function names and their execution times from log files in the given directory.

    Args:
        log_directory (str): The directory containing the log files.

    Returns:
        A PrettyTable object with the function names and their execution times.
    """
    # Dictionary to store the function names and execution times
    data = {}

    # Get all log files in the directory
    log_files = [f for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))]

    # Process each log file
    for log_file in log_files:
        file_path = os.path.join(log_directory, log_file)

        # Read the log file
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                function_name = parts[2].strip().split()[1] 
                execution_time = float(parts[3].split()[0])

                # Add the execution time to the function's entry in the dictionary
                if function_name in data:
                    data[function_name].append(execution_time)
                else:
                    data[function_name] = [execution_time]

    # Create the table
    table = PrettyTable()
    table.field_names = ["Function Name"] + log_files

    # Add the data to the table
    for function_name, execution_times in data.items():
        # Create a row with function name and execution times for each log file
        row = [function_name] + execution_times
        table.add_row(row)

    # Return the table
    return table

# Create an argument parser to get the log directory from the user
parser = argparse.ArgumentParser()
parser.add_argument("log_directory", help="Path to the log directory")
args = parser.parse_args()

log_directory = args.log_directory

# Create the table
table = create_table(log_directory)

# Print the table
print(table)

