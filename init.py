import ray
if ray.is_initialized():
    ray.shutdown()
ray.cluster_resources()
