from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Tekton:
    def __init__(self) -> None:
        self.pipelines = None
        self.triggers = None
        self.interceptors = None
        self.dashboard = None

    def deploy(self, k8s_provider):
        self.pipelines = ConfigGroup(
            "tekton-pipelines",
            files = [
                "manifests/tekton/pipelines.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider
            )
        )
        self.triggers = ConfigGroup(
            "tekton-triggers",
            files = [
                "manifests/tekton/triggers.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.pipelines
            )
        )
        self.dashboard = ConfigGroup(
            "tekton-dashboard",
            files = [
                "manifests/tekton/dashboard.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.triggers
            )
        )
        self.interceptors = ConfigGroup(
            "tekton-interceptors",
            files = [
                "manifests/tekton/interceptors.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.triggers
            )
        )