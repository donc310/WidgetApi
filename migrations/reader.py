import os
import csv
from pathlib import Path


def readMyFiles(Fname, fpath='data'):
    data = []
    _dir = Path(fpath)
    filepath = _dir.resolve()
    if Fname not in os.listdir(filepath):
        print(f'File {Fname} does not exist in {filepath}')
        raise FileExistsError()
    for root, dirs, files in os.walk(filepath, topdown=False):
        for _file in files:
            if _file == Fname and _file.endswith(".csv"):
                datafile = (os.path.join(root, _file))
                with open(datafile, 'r', encoding='utf-8') as csvfile:
                    fileDialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                    dictReader = csv.DictReader(csvfile, dialect=fileDialect)
                    for row in dictReader:
                        entry = dict(row)
                        if Fname == 'base.csv':
                            entry['ChainID'] = float(entry['ChainID'])
                            entry['Frequent'] = int(entry['Frequent'])
                            entry['Moderate'] = int(entry['Moderate'])
                            entry['Mild'] = int(entry['Mild'])
                        data.append(entry)
    return data

