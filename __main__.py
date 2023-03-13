from lib.k8s import k8s
from lib.utils import utils
import pulumi

gke_cluster = k8s.generate_k8s_cluster()
kubeconfig = utils.generate_kube_config(gke_cluster)

# Export some values for use elsewhere
pulumi.export("clusterName", gke_cluster.name)
pulumi.export("clusterId", gke_cluster.id)
pulumi.export("kubeconfig", kubeconfig)