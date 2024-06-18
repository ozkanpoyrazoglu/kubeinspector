import logging
from kubernetes import client

def check_pvs(v1: client.CoreV1Api, exclude_namespaces):
    logger = logging.getLogger(__name__)
    
    logger.info("Fetching PVs...")
    pvs = []
    pv_list = v1.list_persistent_volume()
    logger.info(f"{len(pv_list.items)} PVs found.")
    
    for pv in pv_list.items:
        if pv.spec.host_path and pv.metadata.namespace not in exclude_namespaces:
            pvs.append({
                'name': pv.metadata.name,
                'namespace': pv.metadata.namespace,
                'hostPath': pv.spec.host_path.path
            })
    
    return pvs
