from pulumi import ResourceOptions, FileAsset
from pulumi_kubernetes.yaml import ConfigGroup
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

class CertManager:
    def __init__(self) -> None:
        self.cert_manager = None
        self.cert_issuer = None

    def deploy(self, k8s_provider):
        cert_namespace = Namespace(
            "cert-manager",
            metadata=ObjectMetaArgs(
                name="cert-manager"
            ),
            opts=ResourceOptions(
                provider=k8s_provider
            )
        )
        self.cert_manager = Release(
            "cert-manager",
            ReleaseArgs(
                name = "cert-manager",
                chart = "cert-manager",
                version = "v1.11.0",
                namespace = cert_namespace.metadata.name,
                repository_opts = RepositoryOptsArgs(
                    repo="https://charts.jetstack.io"
                ),
                value_yaml_files=[FileAsset("manifests/cert-manager/cert-manager-values.yaml")]
            ),
            opts = ResourceOptions(
                provider=k8s_provider,
                parent=cert_namespace
            )
        )
        self.cert_issuer = ConfigGroup(
            "cert-issuer",
            files = [
                "manifests/cert-manager/certificate-issuer.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                parent=self.cert_manager
            )
        )