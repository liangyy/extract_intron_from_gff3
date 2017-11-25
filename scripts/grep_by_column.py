import argparse
parser = argparse.ArgumentParser(prog='grep_by_column.py', description='''
    This script takes an input file, column index to grep and the string
    to grep
''')
parser.add_argument('--read_method', default = 'zcat', help = '''
    Specify the method to read input file (default is `zcat`)
''')
parser.add_argument('file')
parser.add_argument('icol', type = int)
parser.add_argument('string')
args = parser.parse_args()

import os

cmd = '''{read} {file} | \
awk -F"\\t" '{{if (${icol} == "{string}") print $0;}}' \
'''.format(file = args.file,
            icol = args.icol,
            string = args.string,
            read = args.read_method)
# print(cmd)
os.system(cmd)
