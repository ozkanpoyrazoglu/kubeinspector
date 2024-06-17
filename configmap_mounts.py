import logging
from kubernetes import client

def check_configmap_mounts(v1: client.CoreV1Api):
    logger = logging.getLogger(__name__)
    
    logger.info("Podlar alınıyor...")
    pods = []
    pod_list = v1.list_pod_for_all_namespaces()
    logger.info(f"{len(pod_list.items)} adet pod bulundu.")
    
    configmap_mounts = []
    
    for pod in pod_list.items:
        for volume in pod.spec.volumes:
            if volume.config_map:
                configmap_name = volume.config_map.name
                mount_paths = [
                    container_volume_mount.mount_path
                    for container in pod.spec.containers
                    for container_volume_mount in container.volume_mounts
                    if container_volume_mount.name == volume.name
                ]
                if mount_paths:
                    configmap_mounts.append({
                        'pod_name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'configmap_name': configmap_name,
                        'mount_paths': ", ".join(mount_paths)
                    })
    
    return configmap_mounts
