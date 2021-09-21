import logging
import concurrent.futures as futures

import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
import gen.pb_python.hello_pb2 as hello_pb2

import grpc


class Greeter(hello_pb2_grpc.HierServicer):
    def __init__(self):
        self._previous = None

    def Hi(self, request: hello_pb2.Player, context: grpc.ServicerContext):
        greet_from_previous = f"(здесь был: {self._previous})" if self._previous else ""
        self._previous = request.name
        return hello_pb2.Greetings(greet=f"Привет,  {request.name}! {greet_from_previous}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), )
    hello_pb2_grpc.add_HierServicer_to_server(Greeter(), server)
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
    main()
