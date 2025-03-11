from typing import Optional
from pydantic import Field

from test_controller.main.pydantic.config.model_config import BaseModelConfig


class Metadata(BaseModelConfig):
    annotations: Optional[dict[str, str]] = Field(default=None)
    creationTimestamp: Optional[str] = Field(default=None)
    generation: Optional[int] = Field(default=None)
    managedFields: Optional[list[dict]] = Field(default=None)
    name: str
    namespace: Optional[str] = Field(default=None)
    resourceVersion: Optional[str] = Field(default=None)
    uid: Optional[str] = Field(default=None)

    def model_dump(self, **kwargs):
        return {"name": self.name}
