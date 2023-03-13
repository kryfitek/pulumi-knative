import pulumi

def generate_kube_config(gke_cluster):
    kubeconfig = pulumi.Output.json_dumps({
        "apiVersion": "v1",
        "clusters": [{
            "cluster": {
                "server": gke_cluster.endpoint,
                "certificate-authority-data": gke_cluster.master_auth.cluster_ca_certificate
            },
            "name": gke_cluster.name,
        }],
        "contexts": [{
            "context": {
                "cluster": gke_cluster.name,
                "user": gke_cluster.name,
            },
            "name": gke_cluster.name,
        }],
        "current-context": gke_cluster.name,
        "kind": "Config",
        "users": [{
            "name": gke_cluster.name,
            "user": {
                "exec": {
                    "apiVersion": "client.authentication.k8s.io/v1beta1",
                    "command": "gke-gcloud-auth-plugin",
                    "installHint": "Install gke-gcloud-auth-plugin for use with kubectl by following https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke",
                    "provideClusterInfo": True,
                },
            },
        }],
    })
    return kubeconfig