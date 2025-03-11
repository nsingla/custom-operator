from enum import Enum

from test_controller.main.actions.deploy_actions import DeployActions
from test_controller.main.actions.pod_actions import PodActions


class Kind(Enum):
    TEST_POD = "TestPod", PodActions
    TEST_DEPLOYMENT = "TestDeployment", DeployActions

    @property
    def name(self):
        return self.value[0]

    @property
    def action_class(self):
        return self.value[1]

    @classmethod
    def get_kind_from_value(cls, kind: str):
        for name, member in Kind.__members__.items():
            if member.name == kind:
                return member