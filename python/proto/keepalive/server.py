import concurrent.futures as futures
import logging
import time

import grpc

import gen.pb_python.hello_pb2 as hello_pb2
import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc


class Greeter(hello_pb2_grpc.UpperServicer):
    def Up(self, request, context: grpc.ServicerContext):
        request: hello_pb2.Player
        time.sleep(2)
        return hello_pb2.Player(name=str(request.name).upper())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=(('grpc.keepalive_timeout_ms', 1000),))
    hello_pb2_grpc.add_UpperServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')

    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    serve()
