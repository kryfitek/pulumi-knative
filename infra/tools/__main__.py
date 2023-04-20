from pulumi import StackReference, export
from pulumi_kubernetes import Provider
from modules.config import PulumiConfig
from modules.kong import Kong
from modules.knative import Knative
from modules.cert_manager import CertManager
from modules.tekton import Tekton

config = PulumiConfig()
config.showValues()
cluster_stack = StackReference(f"kryfitek/pp-k8s/" + config.environment)
k8s_provider = Provider(
    resource_name="k8s-provider",
    kubeconfig=cluster_stack.get_output("kubeconfig")
)
# cert_manager = CertManager()
# cert_manager.deploy(k8s_provider)
kong = Kong()
kong.deploy(k8s_provider)
# svc = knative.operator.get_resource('v1/Service', 'kong', 'kong')
# proxy_ip = svc.status.apply(lambda s: s.load_balancer.ingress[0].ip)
# export("proxy_ip", proxy_ip)
knative = Knative()
knative.deploy(k8s_provider)
tekton = Tekton()
tekton.deploy(k8s_provider)