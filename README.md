# cost-mgmt-perf
This project is to add profiling to cost management services running in perf-cluster namespace hccm-perf

# 1 running fake data generator
E.g. ansible-playbook playbook_copy_tc_ingest_ocp_on_gcp_static.yml -e nodes=10 -e namespaces=1 -e pods=1 -e volumes=1

This test creates 10 nodes each node is associated with 1 namespace. Each namespace contains 1 pod and 1 volume
It generats yml files for two clusters pom and kiki and the playbooks are copied to IQE test container 

# 2 test the generated fake data
ansible-playbook playbook_run_test_ingest_ocp_on_gcp_static.yml -e nodes=10

this test run tests ingest_ocp_on_gcp_static with the files generated using step 1. It profiles the test case functions and generates log files that 
are copied to local directory test_n_{node}_nam_{namespace}_p_{pod}_v_{volume} is created during run.

# 3 parse the results into table or matplot graph 
python3 parse_results_to_table.py <local_generated_directory_from_step_2> 

This generates a test results table

Similarly, to generate matplot lib graph for the results run this command

python3 parse_results_to_graph.py <local_generated_directory_from_step_2> 


