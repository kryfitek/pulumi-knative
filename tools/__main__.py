from pulumi import StackReference, export
from pulumi_kubernetes import Provider
from modules.config import PulumiConfig
from modules.kong import Kong
from modules.knative import Knative
from modules.cert_manager import CertManager

config = PulumiConfig()
config.showValues()
cluster_stack = StackReference(f"kryfitek/pp-k8s/" + config.environment)
k8s_provider = Provider(
    resource_name="k8s-provider",
    kubeconfig=cluster_stack.get_output("kubeconfig")
)
k8s_provider_ss = Provider(
    resource_name="k8s-provider-ss",
    kubeconfig=cluster_stack.get_output("kubeconfig"),
    enable_server_side_apply=True
)
# cert_manager = CertManager()
# cert_manager.deploy(k8s_provider)
# # kong = Kong()
# # kong.deploy(k8s_provider)
# svc = kong.kong.get_resource('v1/Service', 'kong/kong-proxy')
# proxy_ip = svc.status.apply(lambda s: s.load_balancer.ingress[0].ip)
# export("proxy_ip", proxy_ip)
knative = Knative()
knative.deploy(k8s_provider, k8s_provider_ss)