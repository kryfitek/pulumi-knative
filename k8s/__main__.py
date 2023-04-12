import pulumi
from modules.utils import Util
from modules.network import GkeNetwork
from modules.cluster import GkeCluster
from modules.config import PulumiConfig, KubeConfig

config = PulumiConfig()
config.showValues()
util = Util(config.resources_prefix, config.environment)
network = GkeNetwork()
network.create(util)
cluster = GkeCluster(util)
cluster.create(config, network.gke_network, network.gke_subnet)

pulumi.export("networkName", network.gke_network.name)
pulumi.export("networkId", network.gke_network.id)
pulumi.export("clusterName", cluster.gke_cluster.name)
pulumi.export("clusterId", cluster.gke_cluster.id)
pulumi.export("kubeconfig", KubeConfig().generate(cluster.gke_cluster))
pulumi.export("clusterIP", cluster.gke_cluster.endpoint)