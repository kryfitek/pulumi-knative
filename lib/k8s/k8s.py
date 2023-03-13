from ..config import config
from ..vpc import vpc
import pulumi
import pulumi_gcp as gcp

def generate_k8s_cluster():
    # Create a cluster in the new network and subnet
    gke_cluster = gcp.container.Cluster(
        "gke-cluster",
        addons_config=gcp.container.ClusterAddonsConfigArgs(
            dns_cache_config=gcp.container.ClusterAddonsConfigDnsCacheConfigArgs(
                enabled=True
            ),
        ),
        binary_authorization=gcp.container.ClusterBinaryAuthorizationArgs(
            evaluation_mode="PROJECT_SINGLETON_POLICY_ENFORCE"
        ),
        datapath_provider="ADVANCED_DATAPATH",
        description="GKE cluster",
        initial_node_count=1,
        ip_allocation_policy=gcp.container.ClusterIpAllocationPolicyArgs(
            cluster_ipv4_cidr_block="/14",
            services_ipv4_cidr_block="/20"
        ),
        location=config.gcp_region,
        master_authorized_networks_config=gcp.container.ClusterMasterAuthorizedNetworksConfigArgs(
            cidr_blocks=[gcp.container.ClusterMasterAuthorizedNetworksConfigCidrBlockArgs(
                cidr_block="0.0.0.0/0",
                display_name="All networks"
            )]
        ),
        network=vpc.gke_network.name,
        networking_mode="VPC_NATIVE",
        private_cluster_config=gcp.container.ClusterPrivateClusterConfigArgs(
            enable_private_nodes=True,
            enable_private_endpoint=False,
            master_ipv4_cidr_block="10.100.0.0/28"
        ),
        remove_default_node_pool=True,
        release_channel=gcp.container.ClusterReleaseChannelArgs(
            channel="STABLE"
        ),
        subnetwork=vpc.gke_subnet.name,
        workload_identity_config=gcp.container.ClusterWorkloadIdentityConfigArgs(
            workload_pool=f"{config.gcp_project}.svc.id.goog"
        )
    )

    # Create a GCP service account for the nodepool
    gke_nodepool_sa = gcp.serviceaccount.Account(
        "gke-nodepool-sa",
        account_id=pulumi.Output.concat(gke_cluster.name, "-np-1-sa"),
        display_name="Nodepool 1 Service Account"
    )

    # Create a nodepool for the cluster
    gcp.container.NodePool(
        "gke-nodepool",
        cluster=gke_cluster.id,
        node_count=config.nodes_per_zone,
        node_config=gcp.container.NodePoolNodeConfigArgs(
            oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            service_account=gke_nodepool_sa.email
        )
    )
    return gke_cluster