from pydantic import Field

from test_controller.main.pydantic.config.model_config import BaseModelConfig

from test_controller.main.models.custom_resource import COMBINED_RESOURCE
from test_controller.main.models.enums.event_type import EventType


class Event(BaseModelConfig):
    type: EventType
    resource: COMBINED_RESOURCE = Field(alias="object")
    raw_object: dict