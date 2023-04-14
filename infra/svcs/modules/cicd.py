from pulumi import ResourceOptions
from pulumi_kubernetes.yaml import ConfigGroup

class TektonPipelines:
    def deploy(self, k8s_provider):
        pipelines = ConfigGroup(
            "tekton_pipelines",
            files = [
                "manifests/cicd/pipelines/pipeline.yaml"
            ], opts = ResourceOptions(
                provider = k8s_provider
            )
        )
        # This is for running the pipeline, may be replaced by a trigger
        # ConfigGroup(
        #     "tekton_pipelines_run",
        #     files = [
        #         "manifests/cicd/pipelines/pipelinerun.yaml"
        #     ], opts = ResourceOptions(
        #         provider = k8s_provider,
        #         parent = pipelines
        #     )
        # )