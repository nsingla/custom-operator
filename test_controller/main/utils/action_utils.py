from test_controller.main.actions.base_actions import BaseActions
from test_controller.main.actions.deploy_actions import DeployActions
from test_controller.main.actions.pod_actions import PodActions
from test_controller.main.models.enums.resource import ResourceType


class ActionUtils:

    kind_action_map: dict[ResourceType, BaseActions] = {
        ResourceType.POD.value: PodActions,
        ResourceType.DEPLOY.value: DeployActions,
    }

    @staticmethod
    def get_action_class(resource_type: ResourceType) -> BaseActions:
        return ActionUtils.kind_action_map[resource_type]