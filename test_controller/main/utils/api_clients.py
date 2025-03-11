import logging

from kubernetes import client, config
from python_rest_client.logger.logger import Logger


class ApiClientFactory(object):
    """
    singleton class to initialize api clients.
    """

    _instance = None
    app_client: client.AppsV1Api = None
    core_v1_client: client.CoreV1Api = None
    custom_object_api_client: client.CustomObjectsApi = None
    logger: logging.Logger = None

    def __new__(cls):
        """
        This magic method is defined to create only one instance of the api clients across all the threads.
        """
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(ApiClientFactory, cls).__new__(cls)
            cls._instance.initialize_clients()
        return cls._instance

    def initialize_clients(self):
        """
        helper method to initialize all required clients.
        """
        config.load_kube_config()
        self.app_client = client.AppsV1Api()
        self.core_v1_client = client.CoreV1Api()
        self.custom_object_api_client = client.CustomObjectsApi()

        # initializing logging
        self.logger = Logger().logger
