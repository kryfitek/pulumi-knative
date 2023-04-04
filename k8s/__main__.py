import pulumi
from network.network import GkeNetwork
from cluster.cluster import GkeCluster
from config.config import PulumiConfig, KubeConfig

config = PulumiConfig()
config.showValues()
network = GkeNetwork()
network.create()
cluster = GkeCluster()
cluster.create(config, network.gke_network, network.gke_subnet)

pulumi.export("networkName", network.gke_network.name)
pulumi.export("networkId", network.gke_network.id)
pulumi.export("clusterName", cluster.gke_cluster.name)
pulumi.export("clusterId", cluster.gke_cluster.id)
pulumi.export("kubeconfig", KubeConfig().generate(cluster.gke_cluster))