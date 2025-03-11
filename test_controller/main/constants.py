import os


class Constants:
    # Custom Resource Config
    custom_group = os.environ.get("group", "test.com")
    custom_plural = os.environ.get("plural", "testpods")

    # General Kube Config
    api_version = os.environ.get("apiVersion", "v1")
    namespace = os.environ.get("namespace", "default")

    # Resource Specific Config
    image_registry_url = os.environ.get("image_url", "")
