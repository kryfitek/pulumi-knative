# BEFORE STARTING
### Create a "Service Account" with the following project roles:
- roles/compute.viewer
- roles/compute.securityAdmin (only required if add_cluster_firewall_rules is set to true)
- roles/container.clusterAdmin
- roles/container.developer
- roles/iam.serviceAccountAdmin
- roles/iam.serviceAccountUser
- roles/resourcemanager.projectIamAdmin (only required if service_account is set to create)

### Activate the following APIs on the project where the Service Account was created:
- Compute Engine API - compute.googleapis.com
- Kubernetes Engine API - container.googleapis.com