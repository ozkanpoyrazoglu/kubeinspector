import argparse
import logging
from kubernetes import client, config
from hostpath import check_pvs
from hostpath_pods import check_hostpath_pods
from configmap_mounts import check_configmap_mounts
from network_policies import check_network_policies
from log_setup import setup_logging
from output_writer import write_output, print_table

def main():
    parser = argparse.ArgumentParser(description='Kubernetes resource checker')
    parser.add_argument('-o', '--output', choices=['csv', 'table'], default='csv', help='Output format: csv or table')
    parser.add_argument('-m', '--module', choices=['configmap', 'hostpath', 'hostpath_pods', 'network_policies', 'services', 'all'], default='all', help='Module to run: configmap, hostpath, hostpath_pods, network_policies, services, or all')
    parser.add_argument('-e', '--exclude-namespace', nargs='*', default=[], help='Namespaces to exclude')
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Loading Kubernetes config...")
    config.load_kube_config()
    logger.info("Kubernetes config loaded.")
    
    logger.info("Creating Kubernetes API client...")
    v1_core = client.CoreV1Api()
    v1_networking = client.NetworkingV1Api()
    logger.info("Kubernetes API client created.")
    
    outputs = {}

    if args.module in ['hostpath', 'all']:
        logger.info("Checking PVs...")
        pvs = check_pvs(v1_core, args.exclude_namespace)
        logger.info(f"{len(pvs)} PVs with hostPath found.")
        outputs['pvs'] = (pvs, ['name', 'namespace', 'hostPath'])

    if args.module in ['hostpath_pods', 'all']:
        logger.info("Checking pods using hostPath volumes...")
        hostpath_pods = check_hostpath_pods(v1_core, args.exclude_namespace)
        logger.info(f"{len(hostpath_pods)} pods using hostPath volumes found.")
        outputs['hostpath_pods'] = (hostpath_pods, ['pod_name', 'namespace', 'hostPath'])
    
    if args.module in ['configmap', 'all']:
        logger.info("Checking ConfigMap mounts...")
        configmap_mounts = check_configmap_mounts(v1_core, args.exclude_namespace)
        logger.info(f"{len(configmap_mounts)} ConfigMap mounts found.")
        outputs['configmap_mounts'] = (configmap_mounts, ['pod_name', 'namespace', 'configmap_name', 'mount_paths'])

    if args.module in ['network_policies', 'all']:
        logger.info("Checking Network Policies...")
        network_policies = check_network_policies(v1_networking, args.exclude_namespace)
        logger.info(f"{len(network_policies)} Network Policies found.")
        outputs['network_policies'] = (network_policies, ['name', 'namespace', 'pod_selector', 'policy_types'])

    
    for key, (data, fieldnames) in outputs.items():
        if args.output == 'csv':
            write_output(f'{key}_output.csv', data, fieldnames)
        elif args.output == 'table':
            print_table(data, fieldnames)

if __name__ == '__main__':
    main()
