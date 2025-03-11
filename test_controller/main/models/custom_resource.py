from typing import Optional

from test_controller.main.pydantic.config.model_config import BaseModelConfig
from pydantic import Field
from test_controller.main.models.metadata import Metadata
from test_controller.main.models.enums.restart_policy import RestartPolicy
from test_controller.main.models.secret import Secret


class CustomResource(BaseModelConfig):
    apiVersion: str
    kind: str
    metadata: Metadata
    secrets: Optional[list[Secret]] = Field(default=None)
    restartPolicy: RestartPolicy
    image_tag: str
    image_name: str
    custom_annotations: Optional[list[dict]] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    name: str
    args: list[str]
    command: list[str]
