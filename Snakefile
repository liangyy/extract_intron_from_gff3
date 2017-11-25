# this module takes gff3 input
# in which exon contains CDS + UTR (GENCODE uses this format)
# input: gff3
# output: intron in bed format

rule gff3_unzip:
    input:
        lambda wildcards: config[wildcards.name]['gff3']
    output:
        temp('temp/{name}__gff3')
    shell:
        'zcat {input[0]} > {output[0]}'

rule gff32bed:
    input:
        'temp/{name}__gff3'
    output:
        temp('temp/{name}__bed.gz')
    shell:
        'gff2bed < {input[0]} | gzip > {output[0]}'
rule extraxt_exon:
    input:
        'temp/{name}__bed.gz'
    output:
        'exon/{name}__exon.bed.gz'
    shell:
        'python scripts/grep_by_column.py {input]} 8 | gzip > {output[0]}'

rule get_intron:
    input:
        'exon/{name}__exon.bed.gz'
    output:
        'intron/{name}__intron.bed.gz'
    logs:
        'logs/{name}__exon2intron.log'
    shell:
        'python scripts/exon2intron.py --i_exon_bed {input[0]} --o_intron_bed {output[0]} > {logs[0]}'
