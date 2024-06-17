import logging
from kubernetes import client

def check_network_policies(v1: client.NetworkingV1Api):
    logger = logging.getLogger(__name__)
    
    logger.info("NetworkPolicy'ler alınıyor...")
    network_policies = []
    network_policy_list = v1.list_network_policy_for_all_namespaces()
    logger.info(f"{len(network_policy_list.items)} adet NetworkPolicy bulundu.")
    
    for np in network_policy_list.items:
        network_policies.append({
            'name': np.metadata.name,
            'namespace': np.metadata.namespace,
            'pod_selector': np.spec.pod_selector.match_labels if np.spec.pod_selector else 'None',
            'policy_types': np.spec.policy_types if np.spec.policy_types else 'None'
        })
    
    return network_policies
