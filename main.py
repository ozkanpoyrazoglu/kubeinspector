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
    parser.add_argument('-m', '--module', choices=['configmap', 'hostpath', 'hostpath_pods', 'network_policies', 'all'], default='all', help='Module to run: configmap, hostpath, hostpath_pods, network_policies, or all')
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Kubeconfig is loading now...")
    config.load_kube_config()
    logger.info("Kubeconfig loaded")
    
    logger.info("Kubernetes API client is creating now...")
    v1_core = client.CoreV1Api()
    v1_networking = client.NetworkingV1Api()
    logger.info("Kubernetes API client created")
    
    outputs = {}

    if args.module in ['hostpath', 'all']:
        # Check persistent volumes
        logger.info("Checking PV's now...")
        pvs = check_pvs(v1_core)
        logger.info(f"Found {len(pvs)} PV")
        outputs['pvs'] = (pvs, ['name', 'namespace', 'hostPath'])

    if args.module in ['hostpath_pods', 'all']:
        # hostPath volume kullanan podları kontrol et
        logger.info("HostPath volume kullanan podlar kontrol ediliyor...")
        hostpath_pods = check_hostpath_pods(v1_core)
        logger.info(f"{len(hostpath_pods)} adet hostPath volume kullanan pod bulundu.")
        outputs['hostpath_pods'] = (hostpath_pods, ['pod_name', 'namespace', 'hostPath'])
    
    if args.module in ['configmap', 'all']:
        # ConfigMap mount'larını kontrol et
        logger.info("ConfigMap mount'ları kontrol ediliyor...")
        configmap_mounts = check_configmap_mounts(v1_core)
        logger.info(f"{len(configmap_mounts)} adet ConfigMap mount'u bulundu.")
        outputs['configmap_mounts'] = (configmap_mounts, ['pod_name', 'namespace', 'configmap_name', 'mount_paths'])

    if args.module in ['network_policies', 'all']:
        # NetworkPolicy'leri kontrol et
        logger.info("NetworkPolicy'ler kontrol ediliyor...")
        network_policies = check_network_policies(v1_networking)
        logger.info(f"{len(network_policies)} adet NetworkPolicy bulundu.")
        outputs['network_policies'] = (network_policies, ['name', 'namespace', 'pod_selector', 'policy_types'])
    
    for key, (data, fieldnames) in outputs.items():
        if args.output == 'csv':
            # Sonuçları CSV'ye yaz
            write_output(f'{key}_output.csv', data, fieldnames)
        elif args.output == 'table':
            # Sonuçları tablo olarak yazdır
            print_table(data, fieldnames)

if __name__ == '__main__':
    main()
