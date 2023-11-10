import json
import matplotlib.pyplot as plt
import datetime
import argparse

def plot_timeseries_from_json(filename):
    # Load the JSON data
    with open(filename, 'r') as f:
        data = json.load(f)

    # Extract CPU data
    cpu_data = data.get("cpu", {}).get("data", {}).get("result", [])

    # Plot each pod's CPU usage
    for pod_data in cpu_data:
        pod_name = pod_data["metric"]["pod"]
        
        # Check if pod name starts with "hive", "koku", or "trino"
        if pod_name.startswith(("koku")):
            timestamps, values = zip(*pod_data["values"])
            # Convert timestamps to datetime format for better plotting
            readable_timestamps = [datetime.datetime.fromtimestamp(int(ts)) for ts in timestamps]
            plt.plot(readable_timestamps, values, label=pod_name)

    # Configure the plot
    plt.title("CPU Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

    # Save the plot as a JPEG image
    output_filename = f"cpu_usage_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpeg"
    plt.savefig(output_filename, format='jpeg')
    print(f"Plot saved as {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CPU usage from a JSON file.")
    parser.add_argument("filename", type=str, help="Path to the JSON file.")
    args = parser.parse_args()
    plot_timeseries_from_json(args.filename)

