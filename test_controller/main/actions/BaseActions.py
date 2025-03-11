import json
from abc import abstractmethod
from kubernetes import client

from test_controller.main.constants import Constants
from test_controller.main.models.custom_resource import CustomResource
from test_controller.main.utils.api_clients import ApiClientFactory

class BaseActions(object):
    api_version = "v1"

    def __init__(self, custom_resource: CustomResource):
        """
        Constructor for Base Actions class which is the parent call for all the actions.
        """
        self.custom_resource = custom_resource
        self.namespace = Constants.namespace
        api_factory = ApiClientFactory()
        self.logger = api_factory.logger

    @abstractmethod
    def create(self):
        """
        Abstract method to implement the create resource logic. This logic will be overwritten as per requirement for different
        actions.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Abstract method to implement the update resource logic. This will be overwritten for
        different actions.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Abstract method to implement the delete resource logic. This will be overwritten for
        different actions.
        """
        pass

    def get_metadata_object(self) -> client.V1ObjectMeta:
        annotations = dict()
        for annotation in self.custom_resource.custom_annotations:
            annotations.update(annotation)
        custom_metadata = CustomResource(**json.loads(self.custom_resource.metadata.annotations["kubectl.kubernetes.io/last-applied-configuration"])).metadata
        return client.V1ObjectMeta(namespace=self.namespace, name=custom_metadata.name,
                                       annotations=annotations)

    def get_containers_object(self) -> list[client.V1Container]:
        containers: list[client.V1Container] = list()
        if Constants.image_registry_url or self.custom_resource.image_url:
            image_url = self.custom_resource.image_url if self.custom_resource.image_url else Constants.image_registry_url
            image = "/".join([image_url, self.custom_resource.image_name])
        else:
            image = self.custom_resource.image_name
        image = ":".join([image, self.custom_resource.image_tag])
        containers.append(client.V1Container(name=self.custom_resource.name, image=image,
                                                    command=self.custom_resource.command,
                                                    args=self.custom_resource.args
                                                    )
                                 )
        return containers

    def get_secrets_object(self) -> list[client.V1LocalObjectReference]:
        secrets: list[client.V1LocalObjectReference] = list()
        for secret in self.custom_resource.secrets:
            secrets.append(client.V1LocalObjectReference(name=secret.name))
        return secrets
