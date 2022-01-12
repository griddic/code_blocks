if __name__ == '__main__':
    try:
        # a = 1/0
        a = 10
    except Exception:
        a = 'ups'
        raise
    finally:
        print(a)
