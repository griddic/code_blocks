import asyncio
import logging
import concurrent.futures as futures

import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
import gen.pb_python.hello_pb2 as hello_pb2
import time
from functools import wraps

# import hello_pb2_grpc
# import hello_pb2

import grpc
import grpc_interceptor
from grpc_interceptor import exceptions
from grpc import RpcError
# from adm import run_separate


def print_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            print(res)
            return res
        except Exception as e:
            print(type(e), e)
            raise

    return wrapper


class Greeter(hello_pb2_grpc.UpperServicer):
    def __init__(self, server):
        self.server = server

    @print_error
    def Up(self, request, context: grpc.ServicerContext):
        # context.abort(grpc.StatusCode.UNAUTHENTICATED, "cococ")
        # context.abort_with_status(grpc.StatusCode.CANCELLED)
        # time.sleep(3)
        request.ByteSize()
        return hello_pb2.Player(name=str(request.name).upper())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         )
    hello_pb2_grpc.add_UpperServicer_to_server(Greeter(server), server)
    server.add_insecure_port('[::]:50051')

    h = server._state.generic_handlers[0]
    print("__>>>", h)
    server.start()

    # asyncio.run(run_separate())

    server.wait_for_termination()


def main():
    logging.basicConfig()
    serve()
    grpc.RpcError()


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    main()
