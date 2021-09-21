import grpc

import hello_pb2_grpc
import hello_pb2

import grpc._auth


def main():
    channel = grpc.insecure_channel('localhost:50051', grpc.access_token_call_credentials("kokoko"))
    # channel = grpc.secure_channel('localhost:50051', grpc.access_token_call_credentials("kokoko"))
    channel = grpc.secure_channel('localhost:50051',
                                  grpc.composite_channel_credentials(grpc.local_channel_credentials(),
                                                                     grpc.access_token_call_credentials("kokoko")))
    stub = hello_pb2_grpc.UpperStub(channel)

    print(stub.Up(hello_pb2.Player(name="пЕтька"), metadata=(("authorizationnnn", "Bearer bebearer"),) ).name)
    stub.Up(hello_pb2.Player(name="пЕтька")).Unpack()


if __name__ == '__main__':
    main()
