import pandas as pd
from pathlib import Path
from math import floor, log
from sys import getsizeof

dir_main = Path('/Users/neelagarwal/Desktop/CITIBike Data/')
dir_nyc = dir_main / 'NYC'
dir_jersey = dir_main / 'Jersey'

#################################################

def simplify_bytes(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(floor(log(size_bytes, 1024)))
    p = 1024 ** i
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])

def df_size(df: pd.DataFrame):
    print(simplify_bytes(getsizeof(df)))
    return None

#################################################

def iter_subfiles(year: int):
    parent = dir_nyc
    dir_year = parent / f'{year}'
    for dir_month in sorted(dir_year.iterdir()):
        dir_month: Path
        if dir_month.is_dir():
            for csv in sorted(dir_month.iterdir()):
                csv: Path
                if csv.is_file() and csv.suffix == '.csv':
                    yield csv.resolve()

# EOF

if __name__ == '__main__':
    print('Sorry this module is not available for direct execution.')