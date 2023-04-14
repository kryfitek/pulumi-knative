import pulumi_gcp as gcp

class GkeNetwork:
    def __init__(self) -> None:
        self.gke_network = None
        self.gke_subnet = None

    def create(self, util) -> None:
        # Create a new network
        network_name = util.generateResourceName("network")
        self.gke_network = gcp.compute.Network(
            network_name,
            name=network_name,
            auto_create_subnetworks=False,
            description="A virtual network for your GKE cluster(s)"
        )
        
        # Create a subnet in the new network
        subnet_name = util.generateResourceName("subnet")
        self.gke_subnet = gcp.compute.Subnetwork(
            subnet_name,
            name=subnet_name,
            ip_cidr_range="10.128.0.0/12",
            network=self.gke_network.id,
            private_ip_google_access=True
        )