import logging
import concurrent.futures as futures


# import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
# import gen.pb_python.hello_pb2 as hello_pb2
import hello_pb2_grpc
import hello_pb2


import grpc
import grpc_interceptor
from grpc_interceptor import exceptions
from grpc import RpcError


class Greeter(hello_pb2_grpc.UpperServicer):

    def Up(self, request, context: grpc.ServicerContext):
        # context.abort(grpc.StatusCode.UNAUTHENTICATED, "cococ")
        # context.abort_with_status(grpc.StatusCode.CANCELLED)
        return hello_pb2.Player(name=str(request.name).upper())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         )
    hello_pb2_grpc.add_UpperServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')

    h = server._state.generic_handlers[0]
    print("__>>>",h)
    server.start()
    server.wait_for_termination()


def main():
    logging.basicConfig()
    serve()
    grpc.RpcError()

if __name__ == '__main__':
    main()
