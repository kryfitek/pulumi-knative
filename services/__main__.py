from pulumi import StackReference
from pulumi_kubernetes import Provider
from modules.config import PulumiConfig

config = PulumiConfig()
config.showValues()
cluster_stack = StackReference(f"kryfitek/pp-k8s/" + config.environment)
k8s_provider = Provider(
    resource_name="k8s.provider",
    kubeconfig=cluster_stack.get_output("kubeconfig")
)