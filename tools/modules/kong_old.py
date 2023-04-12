from pulumi import ResourceOptions, FileAsset
from pulumi_kubernetes.yaml import ConfigGroup
from pulumi_kubernetes.core.v1 import Namespace
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

class Kong:

    def __init__(self) -> None:
        self.kong = None

    def deploy(self, k8s_provider, cert_manager):
        kong_namespace = Namespace(
            "kong-namespace",
            metadata=ObjectMetaArgs(
                name="kong"
            ),
            opts=ResourceOptions(
                provider=k8s_provider
            )
        )
        kong_secrets = ConfigGroup(
            "kong-secrets",
            files = [
                "manifests/kong/kong-secrets.yaml"
            ], opts = ResourceOptions(
                provider=k8s_provider,
                depends_on=[kong_namespace]
            )
        )
        self.kong = Release(
            "quickstart",
            ReleaseArgs(
                chart="kong",
                name="quickstart",
                namespace=kong_namespace.metadata.name,
                repository_opts=RepositoryOptsArgs(
                    repo="https://charts.konghq.com"
                ),
                value_yaml_files=[FileAsset("manifests/kong/kong-gateway-values.yaml")]
            ),
            opts = ResourceOptions(
                provider=k8s_provider,
                depends_on=[kong_namespace, kong_secrets, cert_manager]
            )
        )

# def remove_status(obj, opts):
#     if obj["kind"] == "CustomResourceDefinition":
#         del obj["status"]

# # Deploying Kong via Helm chart.
# kong_ingress = k8s.helm.v3.Chart(
#     "kong-ingress",
#     k8s.helm.v3.ChartOpts(
#         namespace=ns.metadata.name,
#         chart="kong",
#         fetch_opts=k8s.helm.v3.FetchOpts(
#             repo="https://charts.konghq.com"
#         ),
#         transformations=[remove_status],
#     ),
#     opts=pulumi.ResourceOptions(provider=k8s_provider, parent=ns),
# )
