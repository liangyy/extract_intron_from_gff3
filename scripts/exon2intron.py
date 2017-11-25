import argparse
parser = argparse.ArgumentParser(prog='exon2intron.py', description='''
    This script takes a bed.gz file which contains exons and prints the
    inferred intron according to exon id
''')
parser.add_argument('--i_exon_bed', help = '''
    Input file -- exon in bed format (the forth column is exon id)
''')
# parser.add_argument('--o_intron_bed', help = '''
#     Output file -- intron in bed format
# ''')args = parser.parse_args()

args = parser.parse_args()

import gzip

# get the number of exons for each transcript
exon_dic = {}
with gzip.open(args.i_exon_bed, 'rt') as f:
    for i in f:
        i = i.split('\t')
        exon_id = i[3]
        chrm = i[0]
        start = i[1]
        end = i[2]
        strand = i[5]
        transcript = exon_id.split(':')[1]
        exon_no = int(exon_id.split(':')[2])
        if transcript not in n_exon_dic:
            exon_dic[transcript] = {}
            exon_dic[transcript][exon] = [chrm, start, end, strand, transcript, exon_no]
        else:
            exon_dic[transcript][exon] = [chrm, start, end, strand, transcript, exon_no]

# print intronic region
# intron_dic = {}
o = gzip.open(args.o_intron_bed, 'wt')
for transcript in exon_dic.keys():
    exons = exon_dic[transcript]
    if max(exons.dic()) != len(exons.dic()):
        print('the number of exon is wrong at {transcript}'.format(transcript = transcript))
    else:
        strand = exon_dic[transcript][1][3]
        # intron_dic[transcript] = []
        start = None
        for i in range(len(exons.dic())):
            exon_id = i + 1
            exon = exons[exon_id]
            if exon[-1] == 1:
                if strand == '+':
                    start = exon[2]
                elif strand == '-':
                    start = exon[1]
            elif exon[-1] <= len(exons.dic()):
                if strand == '+':
                    end = exon[1]
                    o.write('\t'.join([exon[0], start, end,
                        transcript, '{id1}-{id2}'.format(id1 = i - 1, id2 = i), strand]) + '\n')
                    if exon[-1] < len(exons.dic()):
                        start = exon[2]
                elif strand == '-':
                    end = exon[2]
                    o.write('\t'.join([exon[0], end, start,
                        transcript, '{id1}-{id2}'.format(id1 = i - 1, id2 = i), strand]) + '\n')
                    if exon[-1] < len(exons.dic()):
                        start = exon[1]
o.close()
