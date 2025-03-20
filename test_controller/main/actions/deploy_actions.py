from kubernetes import client

from test_controller.main.actions.base_actions import BaseActions
from test_controller.main.models.custom_resource import CustomResource, DeploymentResource
from test_controller.main.utils.api_clients import ApiClientFactory

api_client: client.AppsV1Api = ApiClientFactory().app_client


class DeployActions(BaseActions):
    kind = "Deployment"

    def __init__(self, custom_resource: DeploymentResource):
        super().__init__(custom_resource)

    def check_existing_deployments(self, name: str):
        deployments: client.V1DeploymentList = api_client.list_namespaced_deployment(namespace=self.namespace)
        if len(list(filter(lambda deployment: deployment.metadata.name == name, deployments.items))) > 0:
            return True
        return False

    def create_deployment_body(self) -> client.V1Deployment:
        containers = self.get_containers_object()
        secrets: list[client.V1LocalObjectReference] = self.get_secrets_object()
        metadata = self.get_metadata_object()
        spec = client.V1DeploymentSpec(containers=containers,
                                       restart_policy=self.custom_resource.specs.restart_policy.value,
                                       image_pull_secrets=secrets)
        return client.V1Deployment(api_version=self.api_version, kind=self.kind, metadata=metadata, spec=spec)

    def create(self):
        if not self.check_existing_deployments(self.namespace, self.custom_resource.metadata.name):
            body = self.create_deployment_body()
            response: client.V1Deployment = api_client.create_namespaced_deployment(namespace=self.namespace, body=body)
            self.logger.info(f"Created a resource of type={response.kind} with name={response.metadata.name}")
            return response
        else:
            self.logger.info(
                f"Deployment with name {self.custom_resource.metadata.name} already exists, so updating it")
            return self.update()

    def update(self):
        pod_body = self.create_deployment_body(self.custom_resource)
        updated_deployment = api_client.patch_namespaced_deployment(namespace=self.namespace,
                                                                    name=self.custom_resource.metadata.name,
                                                                    body=pod_body)
        self.logger.info(f"Deployment with name={self.custom_resource.metadata.name} updated")
        return updated_deployment

    def delete(self):
        api_client.delete_namespaced_deployment(namespace=self.namespace, name=self.custom_resource.metadata.name)
        self.logger.info(f"Deplpoyment with name={self.custom_resource.metadata.name} deleted")
