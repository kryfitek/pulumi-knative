from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup
from pulumi_kubernetes.core.v1 import ConfigMapPatch, ConfigMapPatchArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaPatchArgs

class Knative:
    def __init__(self) -> None:
        self.knative_serving = None
        self.kourier = None

    def deploy(self, k8s_provider, k8s_provider_ss):
        knative_crds = ConfigGroup(
            "knative-crds",
            files = [
                "manifests/knative/serving-crds.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider
            ), resource_prefix="crds"
        )
        self.knative_serving = ConfigGroup(
            "knative-serving",
            files = [
                "manifests/knative/serving-core.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=knative_crds
            )
        )
        self.kourier = ConfigGroup(
            "kourier",
            files = [
                "manifests/knative/kourier.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.knative_serving
            )
        )
        patch = ConfigMapPatch(
            "config-network",
            args=ConfigMapPatchArgs(
                metadata=ObjectMetaPatchArgs(
                    name="config-network",
                    namespace="knative-serving"
                ),
                data={"ingress-class":"kourier.ingress.networking.knative.dev"}
            ), opts = ResourceOptions(
                provider=k8s_provider_ss,
                parent=self.kourier
            )
        )