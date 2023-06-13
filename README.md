# cost-mgmt-perf
This project is add profiling to cost management service

# running fake data generator
ansible-playbook playbook_copy_tc_ingest_ocp_on_gcp_static.yml -e nodes=10 -e namespaces=1 -e pods=1 -e volumes=1

This test creates 10 nodes each node is associated with 1 namespace. Each namespace contains 1 pod and 1 volume
After generating yml files for two clusters pom and kiki the playbook will automatically copies to IQE test container 

# test the generated fake data
ansible-playbook playbook_run_test_ingest_ocp_on_gcp_static.yml  -e nodes=10

this test run test ingest_ocp_on_gcp_static with two clusters. It profiles the test case and generates log files which are copied 
to local directory test_n_{node}_nam_{namespace}_p_{pod}_v_{volume}

# to parse the results into table and graph corresponding python scripts are placed in this repo
python3 parse_results_to_table.py test_n_{node}_nam_{namespace}_p_{pod}_v_{volume}

This generates a test results table

Similarly, to generate matplot lib graph for the results run this command
python3 parse_results_to_graph.py test_n_{node}_nam_{namespace}_p_{pod}_v_{volume}


