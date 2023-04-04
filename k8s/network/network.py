import pulumi_gcp as gcp

class GkeNetwork:
    def __init__(self) -> None:
        self.gke_network = None
        self.gke_subnet = None

    def create(self) -> None:
        # Create a new network
        self.gke_network = gcp.compute.Network(
            "gke-network",
            name="gke-network",
            auto_create_subnetworks=False,
            description="A virtual network for your GKE cluster(s)"
        )
        
        # Create a subnet in the new network
        self.gke_subnet = gcp.compute.Subnetwork(
            "gke-subnet",
            name="gke-subnet",
            ip_cidr_range="10.128.0.0/12",
            network=self.gke_network.id,
            private_ip_google_access=True
        )