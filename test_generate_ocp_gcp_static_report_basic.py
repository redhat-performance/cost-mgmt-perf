import os
import yaml
import unittest
from generate_ocp_gcp_static_report_basic import generate_fake_data_pom

class TestGenerateFakeDataPom(unittest.TestCase):
    def setUp(self):
        self.template_path = "template.yml"
        self.output_path = "output.yml"
        self.num_nodes = 1
        self.num_namespaces = 2
        self.num_pods = 2
        self.num_volumes = 5

    def tearDown(self):
        os.remove(self.output_path)

    def test_generate_fake_data_pom(self):
        generate_fake_data_pom(self.num_nodes, self.num_namespaces, self.num_pods, self.num_volumes, self.template_path, self.output_path)

        with open(self.output_path, "r") as f:
            output_dict = yaml.safe_load(f)

        self.assertEqual(len(output_dict["generators"][0]["OCPGenerator"]["nodes"]), self.num_nodes)

        for node in output_dict["generators"][0]["OCPGenerator"]["nodes"]:
            self.assertEqual(len(node["node"]["namespaces"]), self.num_namespaces)

            for namespace in node["node"]["namespaces"].values():
                self.assertEqual(len(namespace["pods"]), self.num_pods)
                self.assertEqual(len(namespace["volumes"]), self.num_volumes)