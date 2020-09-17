from pisat.comm.codecs.codec_tag_num import *

from typing import List


class CodecFlagTagNum(CodecTagNum):

    def __init__(self, len_flag:int, tags:TagsX=None):
        super().__init__(tags=tags)
        self.len_flag = len_flag


    @classmethod
    def encodec(cls, flag:str, data:DataTagNumber, tags:Tags)-> str:
        if not isinstance(flag, str):
            raise TypeError("The argument flag has to be an object of str")

        return flag + super().encodec(data, tags)
    

    def encode(self, flag:str, data:DataTagNumber)-> str:

        if isinstance(self.tags, type(None)):
            raise TagNotExsistError("The tags variable are not set yet")

        return CodecFlagTagNum.encodec(flag, data, self.tags)


    @classmethod
    def decodec(cls, data:str, tags:Tag, len_flag:int)-> List[str, dict]:
        flag = data[:len_flag]
        data_decoded = super().decodec(data[len_flag:], tags)
        return [flag, data_decoded]

    
    def decode(self, data:str)-> List[str, dict]:

        if isinstance(self.tags, type(None)):
            raise TagNotExsistError("The tags variable are not set yet")

        return CodecFlagTagNum.decodec(data, self.tags, self.len_flag)


    def decode_format(self, data):

        data_decoded = self.decode(data)
        for tag in self.tags:
            if tag not in data_decoded[1].keys:
                data_decoded[1][tag] = None
            
        return data_decoded