import grpc

import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
import gen.pb_python.hello_pb2 as hello_pb2

import grpc._auth


def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.UpperStub(channel)

    next_page_token = ''
    while True:
        res = stub.ListThousand(hello_pb2.ListRequests(page_size=17,
                                                       page_token=next_page_token))
        print(res.nums)
        print(res.next_page_token)
        next_page_token = res.next_page_token
        if not next_page_token:
            break


if __name__ == '__main__':
    main()
