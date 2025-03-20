from enum import Enum

from test_controller.main.constants import Constants


class ResourceType(Enum):
    POD = Constants.custom_resource_prefix + "Pod"
    DEPLOY = Constants.custom_resource_prefix + "Deploy"