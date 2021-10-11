import base64
import hashlib
import json
import logging
import concurrent.futures as futures

import gen.pb_python.hello_pb2_grpc as hello_pb2_grpc
import gen.pb_python.hello_pb2 as hello_pb2

import grpc


class Crypter:
    def encrypt(self, string) -> str:
        return string

    def decrypt(self, string) -> str:
        return string


class Pager:
    def __init__(self, crypter):
        self.crypter = crypter

    def next_page_token(self, offset, filters_hash):
        raw = json.dumps((offset, filters_hash))
        coded: str = self.crypter.encrypt(raw)
        encoded = base64.encodebytes(coded.encode('utf-8'))
        return encoded.decode('utf-8')

    def parse_next_page_token(self, next_page_token: str):
        decoded = base64.decodebytes(next_page_token.encode('utf-8'))
        decrypted = self.crypter.decrypt(decoded.decode('utf-8'))
        return json.loads(decrypted)


class InvalidPageRequest(Exception):
    pass


class Pager1:
    def __init__(self, page_token, page_size, filter, crypter):
        self.crypter = crypter
        self.filter_hash = get_hash(filter or '')
        first_page = not page_token
        if first_page:
            self._offset = 0
        else:
            self._offset, filter_hash = self._parse_next_page_token(page_token)
            if filter_hash != self.filter_hash:
                raise InvalidPageRequest('following page request should be with the same filter')
        self._page_size = page_size
        self._shift = None

    @property
    def offset(self):
        return self._offset

    @property
    def page_size(self):
        return self._page_size

    def _parse_next_page_token(self, next_page_token: str):
        decoded = base64.decodebytes(next_page_token.encode('utf-8'))
        decrypted = self.crypter.decrypt(decoded.decode('utf-8'))
        return json.loads(decrypted)

    def set_shift(self, shift):
        self._shift = shift

    @property
    def next_page_token(self):
        assert self._shift is not None
        if self._shift == 0:
            return ''
        raw = json.dumps((self.offset + self._shift, self.filter_hash))
        coded: str = self.crypter.encrypt(raw)
        encoded = base64.encodebytes(coded.encode('utf-8'))
        return encoded.decode('utf-8')



def get_hash(string: str):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


# if __name__ == '__main__':
#     pager = Pager(Crypter())
#     args = (0, 'eee')
#     token = pager.next_page_token(*args)
#     print(token)
#
#     new_args = pager.parse_next_page_token(token)
#     print(new_args)


class Greeter(hello_pb2_grpc.UpperServicer):
    def ListThousand(self, request: hello_pb2.ListRequests, context: grpc.ServicerContext):
        pager = Pager1(request.page_token, request.page_size or 100, request.filters, Crypter())

        nums = list(range(pager.offset, min(pager.offset + pager.page_size, 1000)))
        pager.set_shift(len(nums))

        ans = hello_pb2.Numbers(nums=nums,
                                next_page_token=pager.next_page_token)
        print("посчитались")
        return ans
        print("ответ вернули, но продолжаем закрывать ресурсы")



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
    main()
