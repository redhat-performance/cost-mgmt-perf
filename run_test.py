import requests
import datetime
import time
import json
import os
import subprocess
import argparse

PROMETHEUS_ENDPOINT = "https://thanos-querier.openshift-monitoring.svc.cluster.local:9091/api/v1/query_range"
# Fetch BEARER_TOKEN from environment variable
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError("BEARER_TOKEN environment variable is not set!")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}


def start_time():
    return datetime.datetime.now()

def end_time(start):
    end = datetime.datetime.now()
    duration = end - start
    return duration

def run_test(test_name):
    command = [
        "iqe",
        "tests",
        "plugin",
        "cost_management",
        "-k",
        test_name,
        "-m",
        "cost_smoke"
    ]
    try:
        result = subprocess.run(command, check=True)
        print("Args:", result.args)
        print("Return code:", result.returncode)
        print("Have {} bytes in stdout:\n{}".format(len(result.stdout), result.stdout))
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_resource_usage(start_time, test_name):
    """
    Runs a test with the given name and captures CPU and memory usage data for each pod in the 'hccm-perf' namespace.
    The data is written to a JSON file with a filename that includes the current timestamp.

    Args:
        start_time (str): The start time of the test in UTC format (e.g. "2022-01-01T00:00:00Z").
        test_name (str): The name of the test to run.

    Returns:
        None
    """
    # Run the test
    run_test(test_name)

    # Capture end time
    end_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Test ended at: {end_time}")

    # CPU Query
    cpu_params = {
        "query": "sum(rate(container_cpu_usage_seconds_total{namespace='hccm-perf'}[5m])) by (pod)",
        "start": start_time,
        "end": end_time,
        "step": "15s"
    }
    cpu_response = requests.get(PROMETHEUS_ENDPOINT, headers=HEADERS, params=cpu_params, verify=False)
    cpu_data = cpu_response.json()

    # Memory Query
    memory_params = {
        "query": "sum(container_memory_usage_bytes{namespace='hccm-perf'}) by (pod)",
        "start": start_time,
        "end": end_time,
        "step": "30s"
    }
    memory_response = requests.get(PROMETHEUS_ENDPOINT, headers=HEADERS, params=memory_params, verify=False)
    memory_data = memory_response.json()

    # Combine CPU and Memory data
    combined_data = {
        "cpu": cpu_data,
        "memory": memory_data
    }

    # Generate a filename with the current timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"resource_usage_data_{timestamp}.json"
    
    # Write the combined data to the JSON file
    with open(filename, 'w') as file:
        json.dump(combined_data, file, indent=4)
    
    print(f"Data written to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Capture resource usage and run a test.")
    parser.add_argument("test_name", help="Name of the test to run.")
    args = parser.parse_args()

    # Capture start time
    start_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Test started at: {start_time}")

    # Get resource usage
    get_resource_usage(start_time, args.test_name)


if __name__ == "__main__":
    start = start_time()
    main()
    duration = end_time(start)
    print(f"=== Duration: {duration} ===")

