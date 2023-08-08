import yandexcloud
from dotenv import load_dotenv
import os

from yandex.cloud.resourcemanager.v1.cloud_service_pb2 import ListCloudsRequest
from yandex.cloud.resourcemanager.v1.cloud_service_pb2_grpc import CloudServiceStub
from yandex.cloud.loadtesting.api.v1.agent_service_pb2_grpc import AgentServiceStub
from yandex.cloud.loadtesting.api.v1.agent_service_pb2 import GetAgentRequest
def test_false():
    load_dotenv()
    token = os.getenv('YC_TOKEN')
    assert token, token
    sdk = yandexcloud.SDK(iam_token=token)
    agent_service = sdk.client(AgentServiceStub)
    agent = agent_service.Get(GetAgentRequest(agent_id='ff6s7jgzfyprbtahxfd8'))
    assert agent.name == 'ligreen-agent'

