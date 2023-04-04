import pulumi
import json

class PulumiConfig:
    def __init__(self) -> None:
        gcp_config = pulumi.Config("gcp")
        self.gcp_project = gcp_config.require("project")
        self.gcp_region = gcp_config.get("region", "us-east1")
        base_config = pulumi.Config()
        self.nodes_per_zone = base_config.get_float("nodesPerZone", 1)
        self.machine_type = base_config.get("machine_type", "n1-standard-1")
        self.disk_size_gb = base_config.get_float("disk_size_gb", 30)
    
    def showValues(self) -> None:
        print(json.dumps(self.__dict__, indent=4))

class KubeConfig:
    def generate(self, gke_cluster):
        # Build a Kubeconfig to access the cluster
        return pulumi.Output.all(
            gke_cluster.master_auth.cluster_ca_certificate,
            gke_cluster.endpoint,
            gke_cluster.name).apply(lambda l:
            f"""apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {l[0]}
    server: https://{l[1]}
  name: {l[2]}
contexts:
- context:
    cluster: {l[2]}
    user: {l[2]}
  name: {l[2]}
current-context: {l[2]}
kind: Config
preferences: {{}}
users:
- name: {l[2]}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
      provideClusterInfo: true
""")