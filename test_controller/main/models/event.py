from test_controller.main.pydantic.config.model_config import BaseModelConfig

from test_controller.main.models.custom_resource import CustomResource
from test_controller.main.models.enums.event_type import EventType


class Event(BaseModelConfig):
    type: EventType
    object: CustomResource
    raw_object: dict