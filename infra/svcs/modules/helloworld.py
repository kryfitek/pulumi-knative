from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Helloworld:
    def __init__(self) -> None:
        self.helloworld = None

    def deploy(self, k8s_provider, services_ns):
        self.helloworld = ConfigGroup(
            "helloworld",
            files = [
                "manifests/helloworld/helloworld.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=services_ns
            )
        )