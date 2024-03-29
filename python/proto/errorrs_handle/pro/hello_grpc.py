# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: hello.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import hello_pb2


class UpperBase(abc.ABC):

    @abc.abstractmethod
    async def Up(self, stream: 'grpclib.server.Stream[hello_pb2.Player, hello_pb2.Player]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/upper.Upper/Up': grpclib.const.Handler(
                self.Up,
                grpclib.const.Cardinality.UNARY_UNARY,
                hello_pb2.Player,
                hello_pb2.Player,
            ),
        }


class UpperStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Up = grpclib.client.UnaryUnaryMethod(
            channel,
            '/upper.Upper/Up',
            hello_pb2.Player,
            hello_pb2.Player,
        )
