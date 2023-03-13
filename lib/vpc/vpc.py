import pulumi_gcp as gcp
import pulumi

# Create a new network
gke_network = gcp.compute.Network(
    "gke-network",
    auto_create_subnetworks=False,
    description="Virtual network for GKE cluster(s)"
)

# Create a subnet in the new network
gke_subnet = gcp.compute.Subnetwork(
    "gke-subnet",
    ip_cidr_range="10.128.0.0/12",
    network=gke_network.id,
    private_ip_google_access=True
)

pulumi.export("networkName", gke_network.name)
pulumi.export("networkId", gke_network.id)