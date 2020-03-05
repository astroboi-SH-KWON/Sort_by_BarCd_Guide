import pandas as pd

class clsSortByBarCdGuide():

    def __init__(self):
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
        ############### end setting env ################

        self.FASTQ_PATH = FASTQ_PATH
        self.BARCODE_PATH = BARCODE_PATH

        self.BARCODE_LEN = BARCODE_LEN
        self.BARCODE_SEQ_RULE = BARCODE_SEQ_RULE

        self.BEFORE_GUIDE = BEFORE_GUIDE
        self.BP_NUM = BP_NUM
        self.AFTER_GUIDE = AFTER_GUIDE

    #
    """
    getIndexBarcode : get INDEX and Barcode data as dictionary
    :param
         BARCODE_PATH
    :return
        dict_object : { INDEX : Barcode }
    """
    def getIndexBarcode(self):
        return pd.read_excel(self.BARCODE_PATH, index_col=[0]).to_dict().get('Barcode')

    """
    checkGuideSeq : check Guide Seq by BEFORE_GUIDE and AFTER_GUIDE
    :param 
        rawStr : FASTQ raw String
    :return 
        guide_str : Guide sequence
    """
    def checkGuideSeq(self, raw_str):
        for str0 in self.BEFORE_GUIDE:
            try:
                idx0 = raw_str.index(str0) + len(str0)
                for str1 in self.AFTER_GUIDE:
                    try:
                        idx1 = raw_str[idx0:].index(str1)
                        return raw_str[idx0:idx0 + idx1]
                    except Exception:
                        continue
            except Exception:
                continue
        return ''

    """
    checkSeqByChar : match sequences by char
    :param
        seq_char :
        target_char : 
    :return
        boolean
    """
    def checkSeqByChar(self,seq_char, target_char):
        flag = False
        if target_char == 'N':
            return True
        elif target_char in 'ACGTU':
            if seq_char == target_char:
                return True
        """
        add more rules of "ACTGU"
        """
        # elif target_char == 'R':
        #     if seq_char in 'AG':
        #         return True
        return flag

    """
    match : match sequence by barcode rules
    :param
        i : index of raw_seq
        j : index of brcd_rule
        seq_str :
        brcd_rule : barcode rule from BARCODE_SEQ_RULE
    :return
        boolean
    """
    def match(self,i, j, seq_str, brcd_rule):
        if len(seq_str) < i + len(brcd_rule):
            return False
        if self.checkSeqByChar(seq_str[i], brcd_rule[j]):
            if j == (len(brcd_rule) - 1):
                return True
            else:
                return self.match(i + 1, j + 1, seq_str, brcd_rule)
        return False

    """
    checkBcdSeq : check Barcode_seq from raw_str after guide_str by BARCODE_SEQ_RULE
    :param
        barcode_dict : INDEX and Barcode data from getIndexBarcode
        result_dict : 
        raw_str : raw FASTQ_seq from FASTQ_PATH
        guide_str : guide_str from checkGuideSeq
    :return
        dict_object : { INDEX : { Barcode : { guide_seq : [ raw_str ... ] } } }
    """
    def checkBcdSeq(self, barcode_dict, result_dict, raw_str, guide_str):
        sliced_str = raw_str[raw_str.index(guide_str) + len(guide_str):]
        # out of whole loop once getting data into result_dict
        flag = False
        for brcd_rule in self.BARCODE_SEQ_RULE:
            if flag:
                break
            for i in range(len(sliced_str)):
                if flag:
                    break
                for j in range(len(brcd_rule)):
                    if self.match(i, j, sliced_str, brcd_rule):
                        try:
                            tmpStr = sliced_str[i + len(brcd_rule): i + len(brcd_rule) + self.BARCODE_LEN]
                            keys = [key0 for key0, val in barcode_dict.items() if val == tmpStr]
                            key = keys[0]
                            # if key == '':
                            #     print('NULL :::::::::::::::::::::::::'+rowStr)
                            if key in result_dict.keys():
                                tmp_dict0 = result_dict[key]
                                tmp_dict1 = tmp_dict0[barcode_dict[key]]
                                if guide_str in tmp_dict1.keys():
                                    tmp_dict1[guide_str].append(raw_str)
                                else:
                                    tmp_dict1[guide_str] = []
                                    tmp_dict1[guide_str].append(raw_str)
                                flag = True
                            else:
                                tmp_list = []
                                tmp_list.append(raw_str)
                                tmp_dict = {barcode_dict[key]: {guide_str: tmp_list}}
                                result_dict[key] = tmp_dict
                                flag = True
                            break
                        except Exception:
                            # TODO: break or continue??
                            break
                    else:
                        break
        return result_dict

    #
    """
    checkFASTQ : get sorted data from FASTQ
    :param 
        barcode_dict from getIndexBarcode
    :return
        dict_object : { INDEX : { Barcode : { guide_seq : [ raw_str ... ] } } }  
    """
    def checkFASTQ(self, barcode_dict):
        result_dict = {}
        null_dict = {}
        for path in self.FASTQ_PATH:
            print(path)
            with open(path) as Fastq1:
                for i, rawStr in enumerate(Fastq1):
                    i = i + 1
                    rawStr = rawStr.replace('\n', '').upper()
                    if i % 4 == 2:
                        guide_str = self.checkGuideSeq(rawStr)
                        for j in self.BP_NUM:
                            if len(guide_str) == j:
                                result_dict = self.checkBcdSeq(barcode_dict, result_dict, rawStr,guide_str)
                            else:
                                null_dict = self.checkBcdSeq(barcode_dict, null_dict, rawStr, guide_str)
        return result_dict, null_dict



