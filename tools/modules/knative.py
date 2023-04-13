from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Knative:
    def __init__(self) -> None:
        self.operator = None
        self.serving = None

    def deploy(self, k8s_provider):
        self.operator = ConfigGroup(
            "knative-operator",
            files = [
                "manifests/knative/operator.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider
            )
        )
        self.serving = ConfigGroup(
            "knative-serving",
            files = [
                "manifests/knative/serving.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.operator
            )
        )