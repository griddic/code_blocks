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

DEFAULT_AGENT_NAME_PREFIX = 'ete-'
    
def wait_for_agent_to_be_ready(agent_stub, agent_id, timeout=15 * 60):
    request = GetAgentRequest(agent_id=agent_id)
    step = 10
    for seconds in range(1, timeout, step):
        agent: Agent = agent_stub.Get(request)
        if agent.status == Status.READY_FOR_TEST:
            break
        time.sleep(step)
    else:
        raise Exception(f'can\'t wait for agent to be ready anymore. Waited {seconds=}')
    

def test_agent_creation():
    load_dotenv()
    token = os.getenv('YC_TOKEN')
    assert token, 'Token should be specified'
    sdk = yandexcloud.SDK(iam_token=token)
    agent_service = sdk.client(AgentServiceStub)

    name = f'{DEFAULT_AGENT_NAME_PREFIX}{uuid.uuid4().hex[:5]}'
    request = CreateAgentRequest(
        folder_id='b1g5mqk0rkb81u1kf2d4',
        name=name,
        compute_instance_params=CreateComputeInstance(
            zone_id='ru-central1-b',
            service_account_id='ajeiigp6grjoa1ip0e67',
            resources_spec={
                'memory': 2147483648,
                'cores': 2,
            },
            boot_disk_spec={
                'disk_spec': {'size': 16106127360},
                'auto_delete': True,
            },
            network_interface_specs=[
                {
                    'subnet_id': 'e2ldl4q7epi20bqdk00n',
                    'primary_v4_address_spec': {},
                    'security_group_ids': ['enp946pmuqhm52rjbn1r']
                },
            ],
            metadata={"ssh-keys": os.environ['AGENT_SSH_KEYS']},
        ),
    )
    agent_create_operation = agent_service.Create(request)
    agent = sdk.wait_operation_and_get_result(agent_create_operation, response_type=Agent, meta_type=CreateAgentMetadata, timeout=20*60).response

    assert agent.name == name

    wait_for_agent_to_be_ready(agent_service, agent.id)

    delete_operation = agent_service.Delete(DeleteAgentRequest(agent_id=agent.id))
    sdk.wait_operation_and_get_result(delete_operation)

    with pytest.raises(_InactiveRpcError) as err_info:
        agent_service.Get(GetAgentRequest(agent_id=agent.id))
    assert err_info.value.code() is StatusCode.NOT_FOUND





