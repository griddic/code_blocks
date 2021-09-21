class CC:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(type(exc_type), exc_type)
        print(type(exc_val), exc_val)
        print(type(exc_tb), exc_tb)
        return True


if __name__ == '__main__':
    with CC():
        pass
    print("===========")
    with CC():
        raise ValueError('ve')
