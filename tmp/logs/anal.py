from collections import defaultdict
from pathlib import Path
import json
import shutil
import yaml

def main():
    file_name = '/Users/griddic/errors-2023-08-15.txt'
    parsed_dir = Path('.parsed')
    shutil.rmtree(parsed_dir)
    with open('interest.log', 'w') as out:
        with open(file_name) as inn:
            count = defaultdict(int)
            for line in inn.readlines():
                s = line.find('{')
                data = json.loads(line[s:])
                if code:=data.get('rpc_code', None):
                    count[code] += 1
                    path: Path = parsed_dir / code / f'{data["time"]}.log'
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(str(path), 'w') as sifa:
                        yaml.dump(data, sifa)
    print(count)

if __name__=='__main__':
    main()