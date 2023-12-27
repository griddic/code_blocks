from grpc import StatusCode
import pytest
import yandexcloud
from dotenv import load_dotenv
import os

from yandex.cloud.loadtesting.api.v1.agent_service_pb2_grpc import AgentServiceStub
from yandex.cloud.loadtesting.api.v1.agent_service_pb2 import GetAgentRequest, CreateAgentRequest, CreateAgentMetadata, DeleteAgentRequest
from yandex.cloud.loadtesting.api.v1.agent.create_compute_instance_pb2 import CreateComputeInstance
from yandex.cloud.loadtesting.api.v1.agent.status_pb2 import Status
from yandex.cloud.loadtesting.api.v1.agent.agent_pb2 import Agent
import uuid
import time
from grpc._channel import _InactiveRpcError

@pytest.fixture
def sdk():
    load_dotenv()
    token = os.getenv('YC_TOKEN')
    assert token, 'Token should be specified'
    sdk = yandexcloud.SDK(iam_token=token)
    return sdk