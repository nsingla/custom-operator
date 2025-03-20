from typing import Optional

from pydantic import Field

from test_controller.main.models.enums.restart_policy import RestartPolicy
from test_controller.main.models.secret import Secret
from test_controller.main.pydantic.config.model_config import BaseModelConfig


class Specification(BaseModelConfig):
    secrets: Optional[list[Secret]] = Field(default=None)
    restart_policy: Optional[RestartPolicy] = Field(alias="restartPolicy", default=None)
    image_tag: str
    image_name: str
    image_url: Optional[str] = Field(default=None)
    name: str
    args: Optional[list[str]]
    command: Optional[list[str]]
