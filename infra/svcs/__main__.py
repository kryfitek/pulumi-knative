from pulumi import StackReference, ResourceOptions
from pulumi_kubernetes import Provider
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from modules.config import PulumiConfig
from modules.helloworld import Helloworld
from modules.clock import Clock

config = PulumiConfig()
config.showValues()
cluster_stack = StackReference(f"kryfitek/pp-k8s/" + config.environment)
k8s_provider = Provider(
    resource_name="k8s.provider",
    kubeconfig=cluster_stack.get_output("kubeconfig")
)
services_ns = Namespace(
    "services",
    metadata=ObjectMetaArgs(
        name="services"
    ),
    opts=ResourceOptions(
        provider=k8s_provider
    )
)
helloworld = Helloworld()
helloworld.deploy(k8s_provider, services_ns)
clock = Clock()
clock.deploy(k8s_provider, services_ns)