import pulumi_gcp as gcp

class GkeCluster:
    def __init__(self, util) -> None:
        self.gke_cluster = None
        self.gke_nodepool_sa = None
        self.gke_nodepool = None
        self.cluster_name = util.generateResourceName("cluster")
        self.sa_np_name = util.generateResourceName("np-sa")
        self.nodepool_name = util.generateResourceName("node-pool")
        
    def create(self, config, gke_network, gke_subnet):
        # Create a cluster in the new network and subnet
        self.gke_cluster = gcp.container.Cluster(
            self.cluster_name,
            name=self.cluster_name,
            description="GKE cluster for pulumi python",
            location=config.gcp_region,
            initial_node_count=1,
            network=gke_network.name,
            subnetwork=gke_subnet.name,
            remove_default_node_pool=True,
            node_config=gcp.container.ClusterNodeConfigArgs(
                disk_size_gb=config.disk_size_gb
            )
        )

        # Create a GCP service account for the nodepool
        self.gke_nodepool_sa = gcp.serviceaccount.Account(
            self.sa_np_name,
            account_id=self.sa_np_name,
            display_name="Nodepool 1 Service Account"
        )

        # Create a nodepool for the cluster
        self.gke_nodepool = gcp.container.NodePool(
            self.nodepool_name,
            name=self.nodepool_name,
            cluster=self.gke_cluster.id,
            node_count=config.nodes_per_zone,
            node_config=gcp.container.NodePoolNodeConfigArgs(
                oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
                service_account=self.gke_nodepool_sa.email,
                machine_type=config.machine_type,
                disk_size_gb=config.disk_size_gb
            )
        )