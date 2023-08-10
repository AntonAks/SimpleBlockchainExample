import hashlib
import json
import os


blockchain_dir = os.curdir + "/blocks"
try:
    os.mkdir(blockchain_dir)
except FileExistsError:
    pass


def get_hash(filename) -> str:
    """
    :param filename: filename with block 
    :return: hash from a block
    """
    with open(f'{blockchain_dir}/{filename}', 'rb') as file:
        _hash = hashlib.sha256(file.read()).hexdigest()
        return _hash


def check_integrity() -> None:
    """
    This function checks hash consistency in all blocks
    :return: None 
    """
    files = sorted([int(i) for i in os.listdir(blockchain_dir)])
    for f in files[1:]:
        with open(f'{blockchain_dir}/{f}', 'rb') as _f:
            _dict = json.load(_f)
            current_hash = _dict['prev_hash']
            current_block_num = _dict['block_num']

            if current_hash == get_hash(current_block_num - 1):
                pass
            else:
                print(f"ERROR - Block {current_block_num - 1} is Corrupted")


def write_block(name: str, vote: str, prev_hash: str = "") -> None:
    """
    This function creates file (block) in blocks folder
    
    :param name: some person name
    :param vote: another name
    :param prev_hash: hash from previous block
    :return: None
    """

    files = sorted([int(i) for i in os.listdir(blockchain_dir)])

    if len(files) == 0:
        filename = 0
    else:
        last_file = files[-1]
        filename = str(last_file + 1)
        prev_hash = get_hash(str(last_file))

    data = {
        "block_num": int(filename),
        "name_from": name,
        "vote": vote,
        "prev_hash": prev_hash
    }

    with open(f'{blockchain_dir}/{filename}', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"block {filename} created")


if __name__ == '__main__':
    write_block(name='Anton', vote='Misha')
    write_block(name='Misha', vote='Anton')
    write_block(name='Olga', vote='Oleg')
    write_block(name='Kira', vote='Misha')
    write_block(name='Olga', vote='Anton')
    write_block(name='Misha', vote='Oleg')
    write_block(name='Misha', vote='Olga')
    write_block(name='Oleg', vote='Anton')
    check_integrity()
