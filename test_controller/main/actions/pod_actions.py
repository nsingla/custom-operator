from kubernetes import client

from test_controller.main.actions.base_actions import BaseActions
from test_controller.main.models.custom_resource import CustomResource, PodResource
from test_controller.main.utils.api_clients import ApiClientFactory

api_client: client.CoreV1Api = ApiClientFactory().core_v1_client


class PodActions(BaseActions):
    kind = "Pod"

    def __init__(self, custom_resource: PodResource):
        super().__init__(custom_resource)

    def check_existing_pods(self, namespace: str, name: str):
        pods: client.V1PodList = api_client.list_namespaced_pod(namespace=namespace)
        if len(list(filter(lambda pod: pod.metadata.name == name, pods.items))) > 0:
            return True
        return False

    def create_pod_body(self) -> client.V1Pod:
        containers = self.get_containers_object()
        secrets = self.get_secrets_object()
        metadata = self.get_metadata_object()
        spec = client.V1PodSpec(containers=containers,
                                restart_policy=self.custom_resource.specs.restart_policy.value,
                                image_pull_secrets=secrets)
        return client.V1Pod(api_version=self.api_version,
                            kind=self.kind,
                            metadata=metadata,
                            spec=spec)

    def create(self):
        if not self.check_existing_pods(self.namespace, self.custom_resource.metadata.name):
            pod_body = self.create_pod_body()
            response: client.V1Pod = api_client.create_namespaced_pod(namespace=self.namespace, body=pod_body)
            self.logger.info(f"Created a pod with name={response.metadata.name}")
            return response
        else:
            self.logger.info(f"Pod with name {self.custom_resource.metadata.name} already exists, so updating it")
            return self.update()

    def update(self):
        pod_body = self.create_pod_body()
        updated_pod = api_client.patch_namespaced_pod(namespace=self.namespace, name=self.custom_resource.metadata.name,
                                                      body=pod_body)
        self.logger.info(f"Pod with name={self.custom_resource.metadata.name} updated")
        return updated_pod

    def delete(self):
        api_client.delete_namespaced_pod(namespace=self.namespace, name=self.custom_resource.metadata.name)
        self.logger.info(f"Pod with name={self.custom_resource.metadata.name} deleted")
