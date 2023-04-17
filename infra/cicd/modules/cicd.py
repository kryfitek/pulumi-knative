from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class Cicd:
    def deploy(self, k8s_provider):
        cicd = ConfigGroup(
            "cicd",
            files = [
                "manifests/rbac/*.yaml",
                "manifests/secrets/*.yaml",
                "manifests/tasks/*.yaml",
                "manifests/pipelines/*.yaml",
                "manifests/triggers/*.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider
            )
        )
        ConfigGroup(
            "runs",
            files = [
                "manifests/taskruns/*.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=cicd
            )
        )