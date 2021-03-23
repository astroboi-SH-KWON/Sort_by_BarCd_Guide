from time import clock

from Utils import Utils
from Process import SortByBarCdGuide
############### start to set env ################
# FILE PATH
# FASTQ_PATH = "D:/000_WORK/KimNahye/20200212/genomic_500ng.extendedFrags.fastq"
# FASTQ_PATH = "D:/000_WORK/KimNahye/20200212/genomic 500ng/genomic_500.extendedFrags_quater.fastq"
FASTQ_PATH = [
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/2.extendedFrags.fastq",
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/3.extendedFrags.fastq",
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/5.extendedFrags.fastq",
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/6.extendedFrags.fastq",
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/7.extendedFrags.fastq",
    "D:/000_WORK/KimNahye/20200302/200302_PCR switching_hi-seq/8.extendedFrags.fastq"
]
# FASTQ_PATH = "D:/000_WORK/KimNahye/20200212/genomic 500ng/test6_PAM_2.txt"
BARCODE_PATH = "D:/000_WORK/KimNahye/20200212/barcode.xlsx"

# Barcode seq rules , 'TTTTT' + 'NNNNNNN' + 'TTTG' + BARCODE (BARCODE_LEN basepair)
T_SEQ = ['TTTTT', 'TTTTTT']
N_SEQ = ['NNNNNNN', 'NNNNNNNN']
SEQ_After_Nseq = ['TTTG']
BARCODE_LEN = 15
BARCODE_SEQ_RULE = []
for seq0 in T_SEQ:
    for seq1 in N_SEQ:
        BARCODE_SEQ_RULE.append(seq0 + seq1 + SEQ_After_Nseq[0])

# quide seq rules , 'CACCG' + guide (BP_NUM basepair) + 'GTTC'
BEFORE_GUIDE = ['CACCG']
BP_NUM = [19]
AFTER_GUIDE = ['GTTC', 'GTTTC']

PREFIX = [
    FASTQ_PATH
    , BARCODE_PATH
    , BARCODE_LEN
    , BARCODE_SEQ_RULE
    , BEFORE_GUIDE
    , BP_NUM
    , AFTER_GUIDE
]

# result file path
RESULT_PATH = "D:/000_WORK/KimNahye/20200302/Gen_10ng"
############### end setting env ################


def main():
    srtByBcdGd = SortByBarCdGuide(PREFIX)
    # get INDEX and Barcode data as dictionary
    barcode_dict = srtByBcdGd.getIndexBarcode()
    # get sorted data from FASTQ
    for tmp_dict in srtByBcdGd.checkFASTQ(barcode_dict):
        util = Utils([RESULT_PATH, tmp_dict])
        util.make_excel()


start_time = clock()
print("start>>>>>>>>>>>>>>>>>>")
main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))