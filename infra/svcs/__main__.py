from pulumi import StackReference
from pulumi_kubernetes import Provider
from modules.config import PulumiConfig
from modules.helloworld import Helloworld
from modules.cicd import TektonPipelines

config = PulumiConfig()
config.showValues()
cluster_stack = StackReference(f"kryfitek/pp-k8s/" + config.environment)
k8s_provider = Provider(
    resource_name="k8s.provider",
    kubeconfig=cluster_stack.get_output("kubeconfig")
)
pipelines = TektonPipelines()
pipelines.deploy(k8s_provider)
Helloworld = Helloworld()
Helloworld.deploy(k8s_provider)