import sys
import yaml
import random
import string
import uuid


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))



def generate_fake_data_pom(num_nodes, num_namespaces, num_pods, num_volumes, template_path, output_path):
    """
    Generates fake data report.

    Args:
        num_nodes (int): Number of nodes to generate data for.
        num_namespaces (int): Number of namespaces to generate data for.
        num_pods (int): Number of pods to generate data for.
        num_volumes (int): Number of volumes to generate data for.
        template_path (str): Path to the YAML template file.
        output_path (str): Path to the output file.

    Returns:
        None
    """
    with open(template_path, "r") as file:
        template_dict = yaml.safe_load(file)

    for i in range(num_nodes):
        node = {
            "node": {
                "node_name": f"test_gcp_pom_{i+1}",
                "cpu_cores": 10,
                "memory_gig": 10,
                "namespaces": generate_namespaces(num_namespaces, num_pods, num_volumes, i+1)
            }
        }
        template_dict["generators"][0]["OCPGenerator"]["nodes"].append(node)

    with open(output_path, "w") as f:
        yaml.dump(template_dict, f, sort_keys=False)

    print(f"Generated output file: {output_path}")


def generate_namespaces(num_namespaces, num_pods, num_volumes, node_num):
    """
    Generate a dictionary of namespaces with the given number of namespaces, pods, volumes, and node number.

    Args:
        num_namespaces (int): The number of namespaces to generate.
        num_pods (int): The number of pods to generate for each namespace.
        num_volumes (int): The number of volumes to generate for each namespace.
        node_num (int): The node number to use in the volume claims.

    Returns:
        dict: A dictionary of namespaces.
    """
    namespaces = {}
    for i in range(num_namespaces):
        namespace_name = f"test_namespace_{generate_random_string(6)}"
        namespace = {
            namespace_name: {
                "pods": generate_pods(num_pods, i+1),
                "volumes": generate_volumes(num_volumes, i+1, node_num)
            }
        }
        namespaces.update(namespace)

    return namespaces


def generate_pods(num_pods, namespace_num):
    """
    Generate a list of pod dictionaries with the given number of pods and namespace number.

    Args:
        num_pods (int): The number of pods to generate.
        namespace_num (int): The namespace number to use in the pod labels.

    Returns:
        list: A list of pod dictionaries.
    """
    pods = []
    for i in range(num_pods):
        pod_name = f"test_pod_{generate_random_string(6)}"
        labels = f"label_app:test_app_{i+1}_ns{namespace_num}"
        pod = {
            "pod": {
                "pod_name": pod_name,
                "cpu_request": 5,
                "mem_request_gig": 4,
                "cpu_limit": 8,
                "mem_limit_gig": 8,
                "pod_seconds": 3600,
                "cpu_usage": {"full_period": 4},
                "mem_usage_gig": {"full_period": 3},
                "labels": labels
            }
        }
        pods.append(pod)

    return pods


def generate_volumes(num_volumes, namespace_num, node_num):
    """
    Generates a list of volumes with the given number of volumes, namespace number, and node number.

    Args:
        num_volumes (int): The number of volumes to generate.
        namespace_num (int): The namespace number to use in the volume names.
        node_num (int): The node number to use in the volume claims.

    Returns:
        list: A list of volumes, each represented as a dictionary.
    """
    volumes = []
    for _ in range(num_volumes):
        volume_name = f"test_volume_{uuid.uuid4().hex[:6]}"
        volume = {
            "volume": {
                "name": volume_name,
                "size_gig": 10,
                "access_modes": ["ReadWriteOnce"],
                "storage_class": "standard",
                "node_affinity": {
                    "required": {
                        "node_selector_terms": [
                            {
                                "matchExpressions": [
                                    {
                                        "key": "kubernetes.io/hostname",
                                        "operator": "In",
                                        "values": [f"test_gcp_pom_{node_num}"]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
        volumes.append(volume)

    return volumes


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_fake_data_kikis(num_nodes, num_namespaces, num_pods, num_volumes, template_path, output_path):
    """
    Generates fake data for testing purposes based on a YAML template file.

    Args:
        num_nodes (int): The number of nodes to generate data for.
        num_namespaces (int): The number of namespaces to generate data for.
        num_pods (int): The number of pods to generate data for.
        num_volumes (int): The number of volumes to generate data for.
        template_path (str): The path to the YAML template file.
        output_path (str): The path to the output file.

    Returns:
        None
    """
    with open(template_path, "r") as file:
        template = file.read()

    template_dict = yaml.safe_load(template)

    # gap between nodes is 1000
    for i in range(num_nodes):
        node = {
            "node": {
                "node_name": f"test_gcp_kikis_{i+1+1000}",
                "cpu_cores": 10,
                "memory_gig": 10,
                "namespaces": generate_namespaces(num_namespaces, num_pods, num_volumes, i+1)
            }
        }
        template_dict["generators"][0]["OCPGenerator"]["nodes"].append(node)

    fake_data = yaml.dump(template_dict, sort_keys=False)

    with open(output_path, "w") as f:
        f.write(fake_data)

    print(f"Generated output file: {output_path}")


def generate_namespaces(num_namespaces, num_pods, num_volumes, node_num):
    namespaces = {}
    for i in range(num_namespaces):
        namespace = {
            f"test_namespace_{generate_random_string(6)}": {
                "pods": generate_pods(num_pods, i+1),
                "volumes": generate_volumes(num_volumes, i+1, node_num)
            }
        }
        namespaces.update(namespace)

    return namespaces


def generate_pods(num_pods, namespace_num):
    """
    Generate a list of pod dictionaries with the given number of pods and namespace number.

    Args:
        num_pods (int): The number of pods to generate.
        namespace_num (int): The namespace number to use in the pod labels.

    Returns:
        list: A list of pod dictionaries.
    """
    pods = []
    for i in range(num_pods):
        pod_name = f"test_pod_{generate_random_string(6)}"
        labels = f"label_app:test_app_{i+1}_ns{namespace_num}"
        pod = {
            "pod": {
                "pod_name": pod_name,
                "cpu_request": 5,
                "mem_request_gig": 4,
                "cpu_limit": 8,
                "mem_limit_gig": 8,
                "pod_seconds": 3600,
                "cpu_usage": {"full_period": 4},
                "mem_usage_gig": {"full_period": 3},
                "labels": labels
            }
        }
        pods.append(pod)

    return pods


def generate_volumes(num_volumes, namespace_num, node_num):
    """
    Generates a list of volumes with the given number of volumes, namespace number, and node number.

    Args:
        num_volumes (int): The number of volumes to generate.
        namespace_num (int): The namespace number to use in the volume names.
        node_num (int): The node number to use in the volume claims.

    Returns:
        list: A list of volumes, each represented as a dictionary.
    """
    volumes = []
    for i in range(num_volumes):
        volume_name = f"test_volume_{generate_random_string(6)}"
        volume_claim_name = f"test_claim_{generate_random_string(6)}"
        volume = {
            "volume": {
                "volume_name": volume_name,
                "storage_class": "gp2",
                "volume_request_gig": 7,
                "labels": "label_volume:test_volume",
                "volume_claims": [
                    {
                        "volume_claim": {
                            "volume_claim_name": volume_claim_name,
                            "pod_name": f"test_pod_{i+1}",
                            "labels": "label_volume:stor_test",
                            "capacity_gig": 10,
                            "volume_claim_usage_gig": {
                                "full_period": 6
                            }
                        }
                    }
                ]
            }
        }
        volumes.append(volume)

    return volumes


# Example usage: python3 generate.py template.yml output.yml nodes=1 namespaces=2 volumes=5 pods=2
if __name__ == "__main__":
    args = sys.argv[1:]
    template_path = args[0]
    output_path_kikis = "ocp_gcp_static_report_basic_kikis_perf.yml"
    output_path_pom = "ocp_gcp_static_report_basic_pom_perf.yml"
    params = {}
    for arg in args[2:]:
        key, value = arg.split("=")
        params[key] = int(value)

    generate_fake_data_pom(params.get("nodes", 0), params.get("namespaces", 0), params.get("pods", 0), params.get("volumes", 0), template_path, output_path_pom)
    generate_fake_data_kikis(params.get("nodes", 0), params.get("namespaces", 0), params.get("pods", 0), params.get("volumes", 0), template_path, output_path_kikis)
    # generate_compute_engine_generators(params.get("nodes", 0))

