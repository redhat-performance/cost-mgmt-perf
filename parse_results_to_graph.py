import os
import matplotlib.pyplot as plt
from prettytable import PrettyTable

log_directory = "test_n_1_nam_1_p_1_v_1/"

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
            function_name = parts[2].strip()
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

    # Plot the graph for the function
    plt.plot(log_files, execution_times, label=function_name)

# Customize the graph
plt.xlabel("Log Files")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time Comparison")
plt.legend()

# Print the table
print(table)

# Show the graph
plt.show()

