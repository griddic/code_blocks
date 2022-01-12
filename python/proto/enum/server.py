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
    @print_error
    def Up(self, request, context: grpc.ServicerContext):
        request: hello_pb2.Player
        sex = request.sex
        print(sex)
        return hello_pb2.Player(name=str(request.name).upper())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         )
    hello_pb2_grpc.add_UpperServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')

    h = server._state.generic_handlers[0]
    print("__>>>", h)
    server.start()

    server.wait_for_termination()


def main():
    logging.basicConfig()
    serve()
    grpc.RpcError()


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    main()
