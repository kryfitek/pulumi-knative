import pulumi
import json
from pulumi_gcp.config import project, region

class PulumiConfig:
    def __init__(self) -> None:
        gcp_config = pulumi.Config("gcp")
        self.gcp_project = gcp_config.require("project")
        self.gcp_region = gcp_config.get("region", "us-east1")
        base_config = pulumi.Config()
        self.environment = base_config.get("environment", "dev")
        self.nodes_per_zone = base_config.get_float("nodesPerZone", 1)
        self.machine_type = base_config.get("machine_type", "n1-standard-1")
        self.disk_size_gb = base_config.get_float("disk_size_gb", 30)
        self.resources_prefix = base_config.get("resources_prefix", "default")
    
    def showValues(self) -> None:
        print(json.dumps(self.__dict__, indent=4))

class KubeConfig:
  def generate(self, k8s_cluster):
      k8s_info = pulumi.Output.all(
          k8s_cluster.name, 
          k8s_cluster.endpoint, 
          k8s_cluster.master_auth
      )
      return k8s_info.apply(
          lambda info: """apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {0}
    server: https://{1}
  name: {2}
contexts:
- context:
    cluster: {2}
    user: {2}
  name: {2}
current-context: {2}
kind: Config
preferences: {{}}
users:
- name: {2}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      provideClusterInfo: true
""".format(info[2]['cluster_ca_certificate'], info[1], 'gke_{0}_{1}_{2}'.format(project, region, info[0])))