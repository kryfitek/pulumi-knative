import pulumi
import pulumi_gcp as gcp
from config.config import PulumiConfig

class GkeCluster:
    def __init__(self) -> None:
        self.gke_cluster = None
        self.gke_nodepool_sa = None
        self.gke_nodepool = None
        
    def create(self, config, gke_network, gke_subnet):
        # Create a cluster in the new network and subnet
        self.gke_cluster = gcp.container.Cluster(
            "gke-cluster",
            name="gke-cluster",
            description="A GKE cluster",
            location=config.gcp_region,
            initial_node_count=1,
            network=gke_network.name,
            subnetwork=gke_subnet.name,
            networking_mode="VPC_NATIVE",
            remove_default_node_pool=True,
            node_config=gcp.container.ClusterNodeConfigArgs(
                disk_size_gb=config.disk_size_gb
            ),
            addons_config=gcp.container.ClusterAddonsConfigArgs(
                dns_cache_config=gcp.container.ClusterAddonsConfigDnsCacheConfigArgs(
                    enabled=True
                ),
            ),
            binary_authorization=gcp.container.ClusterBinaryAuthorizationArgs(
                evaluation_mode="PROJECT_SINGLETON_POLICY_ENFORCE"
            ),
            datapath_provider="ADVANCED_DATAPATH",
            ip_allocation_policy=gcp.container.ClusterIpAllocationPolicyArgs(
                cluster_ipv4_cidr_block="/14",
                services_ipv4_cidr_block="/20"
            ),
            master_authorized_networks_config=gcp.container.ClusterMasterAuthorizedNetworksConfigArgs(
                cidr_blocks=[gcp.container.ClusterMasterAuthorizedNetworksConfigCidrBlockArgs(
                    cidr_block="0.0.0.0/0",
                    display_name="All networks"
                )]
            ),
            private_cluster_config=gcp.container.ClusterPrivateClusterConfigArgs(
                enable_private_nodes=True,
                enable_private_endpoint=False,
                master_ipv4_cidr_block="10.100.0.0/28"
            ),
            release_channel=gcp.container.ClusterReleaseChannelArgs(
                channel="STABLE"
            ),
            workload_identity_config=gcp.container.ClusterWorkloadIdentityConfigArgs(
                workload_pool=f"{config.gcp_project}.svc.id.goog"
            )
        )

        # Create a GCP service account for the nodepool
        self.gke_nodepool_sa = gcp.serviceaccount.Account(
            "gke-nodepool-sa",
            account_id=pulumi.Output.concat(self.gke_cluster.name, "-np-1-sa"),
            display_name="Nodepool 1 Service Account"
        )

        # Create a nodepool for the cluster
        self.gke_nodepool = gcp.container.NodePool(
            "gke-nodepool",
            cluster=self.gke_cluster.id,
            node_count=config.nodes_per_zone,
            node_config=gcp.container.NodePoolNodeConfigArgs(
                oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
                service_account=self.gke_nodepool_sa.email,
                machine_type=config.machine_type,
                disk_size_gb=config.disk_size_gb
            )
        )