
import pulumi

# Get some provider-namespaced configuration values
provider_cfg = pulumi.Config("gcp")
gcp_project = provider_cfg.require("project")
gcp_region = provider_cfg.get("region", "us-east1")
# Get some additional configuration values
config = pulumi.Config()
nodes_per_zone = config.get_float("nodesPerZone", 1)