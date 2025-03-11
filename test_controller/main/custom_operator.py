from kubernetes import watch

from test_controller.main.constants import Constants
from test_controller.main.models.enums.kind import Kind
from test_controller.main.models.event import Event
from test_controller.main.models.enums.event_type import EventType
from test_controller.main.utils.api_clients import ApiClientFactory

api_client_factory = ApiClientFactory()
logger = api_client_factory.logger


def start_operator():
    logger.info("Starting Operator")

    resource_version = ""

    while True:
        stream = watch.Watch().stream(
            api_client_factory.custom_object_api_client.list_namespaced_custom_object,
            Constants.custom_group, Constants.api_version, Constants.namespace, Constants.custom_plural,
            resource_version=resource_version
        )
        for event in stream:
            event = Event(**event)
            event_type = event.type
            custom_resource = event.object

            action_class = Kind.get_kind_from_value(custom_resource.kind).action_class
            actions_object = action_class(custom_resource)

            match event_type:
                case EventType.ADDED:
                    logger.info(f"Received an event to create a resource of type={custom_resource.kind}")
                    actions_object.create()
                case EventType.UPDATED:
                    logger.info(f"Received an event to update a resource of type={custom_resource.kind}")
                    actions_object.update()
                    logger.info(f"Updated a resource of type={custom_resource.kind.name}")
                case EventType.DELETED:
                    logger.info(f"Deleted a resource of type={custom_resource.kind} and name={custom_resource.metadata.name}")
                    actions_object.delete()
                case _:
                    logger.info("Nothing to do here")

            # Update resource_version to resume watching from the last event
            resource_version = custom_resource.metadata.resourceVersion


if __name__ == "__main__":
    start_operator()
