from test_controller.main.pydantic.config.model_config import BaseModelConfig


class Secret(BaseModelConfig):
    name: str
