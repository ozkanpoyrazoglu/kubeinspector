import logging
from kubernetes import client

def check_network_policies(v1: client.NetworkingV1Api, exclude_namespaces):
    logger = logging.getLogger(__name__)
    
    logger.info("Fetching Network Policies...")
    network_policies = []
    network_policy_list = v1.list_network_policy_for_all_namespaces()
    logger.info(f"{len(network_policy_list.items)} Network Policies found.")
    
    for np in network_policy_list.items:
        if np.metadata.namespace not in exclude_namespaces:
            network_policies.append({
                'name': np.metadata.name,
                'namespace': np.metadata.namespace,
                'pod_selector': np.spec.pod_selector.match_labels if np.spec.pod_selector else 'None',
                'policy_types': np.spec.policy_types if np.spec.policy_types else 'None'
            })
    
    return network_policies
