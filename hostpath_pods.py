import logging
from kubernetes import client

def check_hostpath_pods(v1: client.CoreV1Api, exclude_namespaces):
    logger = logging.getLogger(__name__)
    
    logger.info("Fetching pods...")
    pods = []
    pod_list = v1.list_pod_for_all_namespaces()
    logger.info(f"{len(pod_list.items)} pods found.")
    
    for pod in pod_list.items:
        if pod.metadata.namespace not in exclude_namespaces:
            for volume in pod.spec.volumes:
                if volume.host_path:
                    pods.append({
                        'pod_name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'hostPath': volume.host_path.path
                    })
    
    return pods
