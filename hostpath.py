import logging
from kubernetes import client

def check_pvs(v1: client.CoreV1Api):
    logger = logging.getLogger(__name__)
    
    logger.info("Persistent Volumes (PV) alınıyor...")
    pvs = []
    pv_list = v1.list_persistent_volume()
    logger.info(f"{len(pv_list.items)} adet PV bulundu.")
    
    for pv in pv_list.items:
        if pv.spec.host_path:
            logger.info(f"HostPath bulunan PV: {pv.metadata.name}")
            pvs.append({
                'name': pv.metadata.name,
                'namespace': pv.metadata.namespace,
                'hostPath': pv.spec.host_path.path
            })
    
    return pvs
