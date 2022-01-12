import logging

import grpc

from gen.pb_python import hello_pb2_grpc
from gen.pb_python import hello_pb2

import grpc._auth

from google.protobuf.timestamp_pb2 import Timestamp

def main():
    channel = grpc.secure_channel('localhost:50051',
                                  grpc.composite_channel_credentials(grpc.local_channel_credentials(),
                                                                     grpc.access_token_call_credentials("kokoko")))
    stub = hello_pb2_grpc.UpperStub(channel)
    ts = Timestamp()
    ts.GetCurrentTime()
    print(stub.Up(hello_pb2.Player(name="пЕтька",
                                   sex=hello_pb2.Player.Sex.MALE,
                                   created_at=ts,
                                   labels={
                                       'k1': 'v1',
                                       'k2': 'v2',
                                   },
                                   penis_length='big'
                                   ),
                  metadata=(("authorizationnnn", "Bearer bebearer"),),
                  timeout=5,
                  ).name)


if __name__ == '__main__':
    main()
    # logging.NOTSET
