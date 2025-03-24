from typing import Union, Annotated, Literal, Optional

from test_controller.main.models.enums.resource import ResourceType
from test_controller.main.models.spec import Specification
from test_controller.main.pydantic.config.model_config import BaseModelConfig
from pydantic import Tag, Discriminator, Field
from test_controller.main.models.metadata import Metadata


class CustomResource(BaseModelConfig):
    apiVersion: str
    kind: str
    metadata: Metadata
    custom_annotations: Optional[list[dict]] = Field(default=None)
    name: Optional[str] = Field(default=None)
    specs: Optional[Specification] = Field(default=None)

class PodResource(CustomResource):
    kind: Literal[ResourceType.POD]


class DeploymentResource(CustomResource):
    kind: Literal[ResourceType.DEPLOY]


def get_discriminator_value(v: str) -> str:
    return v['kind']


COMBINED_RESOURCE = Annotated[Union[
        Annotated[PodResource, Tag(ResourceType.POD.value)],
        Annotated[DeploymentResource, Tag(ResourceType.DEPLOY.value)]
    ], Discriminator(get_discriminator_value)]
