import logging
from kubernetes import client

def check_configmap_mounts(v1: client.CoreV1Api, exclude_namespaces):
    logger = logging.getLogger(__name__)
    
    logger.info("Fetching pods with ConfigMap mounts...")
    configmap_mounts = []
    pod_list = v1.list_pod_for_all_namespaces()
    logger.info(f"{len(pod_list.items)} pods found.")
    
    for pod in pod_list.items:
        if pod.metadata.namespace not in exclude_namespaces:
            for volume in pod.spec.volumes:
                if volume.config_map:
                    mount_paths = [mount.mount_path for mount in pod.spec.containers[0].volume_mounts if mount.name == volume.name]
                    configmap_mounts.append({
                        'pod_name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'configmap_name': volume.config_map.name,
                        'mount_paths': ', '.join(mount_paths)
                    })
    
    return configmap_mounts
