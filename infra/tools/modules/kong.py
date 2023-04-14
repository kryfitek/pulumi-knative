from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Kong:
    def __init__(self) -> None:
        self.kong: ConfigGroup = None

    def deploy(self, k8s_provider):
        self.kong = ConfigGroup(
            "kong",
            files = [
                "manifests/kong/all-in-one-dbless.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider
            )
        )