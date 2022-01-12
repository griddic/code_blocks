import sys
import traceback

if __name__ == '__main__':
    uri = sys.argv[1]
    with open('sub.log', 'w') as out:
        while True:
            try:
                inp = input()
                print(uri, inp, file=out)
                print(uri, inp, file=sys.stdout)
            except EOFError:
                print('NoMoreData', file=out)
                break
            except Exception as e:
                print(e, file=out)
                print(traceback.format_exc(), file=out)
