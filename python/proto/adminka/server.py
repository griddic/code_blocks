import asyncio
import concurrent.futures as futures
import logging
import threading

import grpc
from grpc_reflection.v1alpha import reflection

import gen.pb_python.hello_pb2 as hello_pb2
import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc

import gen.pb_python.admin_pb2 as admin_pb2
import gen.pb_python.admin_pb2_grpc as admin_pb2_grpc

from adm import Admin, adminized


# import hello_pb2_grpc
# import hello_pb2


class Greeter(hello_pb2_grpc.UpperServicer):
    def __init__(self, parent_logger):
        self.logger = parent_logger.getChild('Greater')

    def Up(self, request, context: grpc.ServicerContext):
        logging.debug(request.name)
        return hello_pb2.Player(name=str(request.name).upper())


def serve():
    pool = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(pool)
    logger = logging.getLogger('server')
    hello_pb2_grpc.add_UpperServicer_to_server(Greeter(logger), server)
    server.add_insecure_port('[::]:50051')

    server.start()

    with adminized(logging.INFO):
        server.wait_for_termination()


def main():
    serve()


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    main()
