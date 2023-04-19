from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs

class Cicd:
    def deploy(self, k8s_provider):
        cicd_ns = Namespace(
            "cicd",
            metadata=ObjectMetaArgs(
                name="cicd"
            ),
            opts = ResourceOptions(
                provider=k8s_provider
            )
        )
        tasks = ConfigGroup(
            "tasks",
            files = [
                "manifests/rbac/*.yaml",
                "manifests/secrets/*.yaml",
                "manifests/tasks/*.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=cicd_ns
            )
        )
        pipes = ConfigGroup(
            "pipes",
            files = [
                "manifests/pipelines/*.yaml",
                "manifests/triggers/*.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=tasks
            )
        )
        ConfigGroup(
            "runs",
            files = [
                "manifests/taskruns/*.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=pipes
            )
        )