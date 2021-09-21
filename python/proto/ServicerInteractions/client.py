import time

import grpc

import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
import gen.pb_python.hello_pb2 as hello_pb2

import grpc._auth


def main():
    channel = grpc.insecure_channel('localhost:50051')

    stub = hello_pb2_grpc.HierStub(channel)

    print(stub.Hi(hello_pb2.Player(name="Алиса")).greet)
    print(stub.Hi(hello_pb2.Player(name="FPG")).greet)


if __name__ == '__main__':
    main()
