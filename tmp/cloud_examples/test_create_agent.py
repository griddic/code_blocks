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
from common import generate_create_agent_request, wait_for_agent_to_be_ready, DEFAULT_AGENT_NAME_PREFIX



def test_agent_creation(sdk: yandexcloud.SDK):
    agent_service = sdk.client(AgentServiceStub)

    name = f'{DEFAULT_AGENT_NAME_PREFIX}{uuid.uuid4().hex[:5]}'
    request = generate_create_agent_request(name)
    agent_create_operation = agent_service.Create(request)
    agent = sdk.wait_operation_and_get_result(agent_create_operation, response_type=Agent, meta_type=CreateAgentMetadata, timeout=20*60).response

    assert agent.name == name

    wait_for_agent_to_be_ready(agent_service, agent.id)

    delete_operation = agent_service.Delete(DeleteAgentRequest(agent_id=agent.id))
    sdk.wait_operation_and_get_result(delete_operation)

    with pytest.raises(_InactiveRpcError) as err_info:
        agent_service.Get(GetAgentRequest(agent_id=agent.id))
    assert err_info.value.code() is StatusCode.NOT_FOUND





