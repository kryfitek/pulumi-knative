from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Clock:
    def __init__(self) -> None:
        self.clock = None

    def deploy(self, k8s_provider, services_ns):
        self.clock = ConfigGroup(
            "clock",
            files = [
                "manifests/clock/clock.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=services_ns
            )
        )