# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from gen.pb_python import hello_pb2 as hello__pb2


class UpperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Up = channel.unary_unary(
                '/upper.Upper/Up',
                request_serializer=hello__pb2.Player.SerializeToString,
                response_deserializer=hello__pb2.Player.FromString,
                )


class UpperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Up(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UpperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Up': grpc.unary_unary_rpc_method_handler(
                    servicer.Up,
                    request_deserializer=hello__pb2.Player.FromString,
                    response_serializer=hello__pb2.Player.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'upper.Upper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Upper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Up(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/upper.Upper/Up',
            hello__pb2.Player.SerializeToString,
            hello__pb2.Player.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)