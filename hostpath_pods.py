import logging
from kubernetes import client

def check_hostpath_pods(v1: client.CoreV1Api):
    logger = logging.getLogger(__name__)
    
    logger.info("Podlar alınıyor...")
    pods = []
    pod_list = v1.list_pod_for_all_namespaces()
    logger.info(f"{len(pod_list.items)} adet pod bulundu.")
    
    for pod in pod_list.items:
        for volume in pod.spec.volumes:
            if volume.host_path:
                logger.info(f"HostPath volume kullanan pod bulundu: {pod.metadata.name} (Namespace: {pod.metadata.namespace})")
                pods.append({
                    'pod_name': pod.metadata.name,
                    'namespace': pod.metadata.namespace,
                    'hostPath': volume.host_path.path
                })
    
    return pods
