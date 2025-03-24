from enum import Enum

from test_controller.main.constants import Constants


class ResourceType(str, Enum):
    POD = Constants.custom_resource_prefix + "Pod"
    DEPLOY = Constants.custom_resource_prefix + "Deploy"

    @property
    def name(self):
        return self.value

    @property
    def action_class(self):
        from test_controller.main.actions.deploy_actions import DeployActions
        from test_controller.main.actions.pod_actions import PodActions
        kind_action_map: dict = {
            ResourceType.POD.value: PodActions,
            ResourceType.DEPLOY.value: DeployActions,
        }
        return kind_action_map[self.value]

