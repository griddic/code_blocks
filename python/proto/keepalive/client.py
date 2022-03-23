import time

import grpc
import grpc._auth

from gen.pb_python import hello_pb2
from gen.pb_python import hello_pb2_grpc


def main():
    channel = grpc.secure_channel('localhost:50051',
                                  grpc.composite_channel_credentials(grpc.local_channel_credentials(),
                                                                     grpc.access_token_call_credentials("***")))
    stub = hello_pb2_grpc.UpperStub(channel)
    start = time.time()
    print(stub.Up(hello_pb2.Player(name="пЕтька"),
                  metadata=(("authorizationnnn", "Bearer bebearer"),),
                  ).name)
    duration = time.time() - start
    print(duration)


if __name__ == '__main__':
    main()
