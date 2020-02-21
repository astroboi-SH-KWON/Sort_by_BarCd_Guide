from time import clock

from Util import clsUtil
from Sort_by_BarCd_Guide import clsSortByBarCdGuide


def Main():
    srtByBcdGd = clsSortByBarCdGuide()
    # get INDEX and Barcode data as dictionary
    barcode_dict = srtByBcdGd.getIndexBarcode()
    # get sorted data from FASTQ
    for tmp_dict in srtByBcdGd.checkFASTQ(barcode_dict):
        util = clsUtil(tmp_dict)
        util.make_excel()


start_time = clock()
print("start>>>>>>>>>>>>>>>>>>")
Main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))