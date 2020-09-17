#! python3
#
#
#
#


from pisat.comm.codecs import CodecTagBase

from typing import List, Tuple, Set, Dict, Union


Tags = Union[Set[str], List[str], Tuple[str]]
TagsX = Union[Tags, None]
DataNumber = Union[float, int]
DataTagNumber = Dict[Tags, DataNumber]


def isOKtag(tag:str)-> bool:

    for char in tag:

        if not ( ("A" <= char <= "Z") or ("a" <= char <= "z") or (char in ("_", "-")) ):
            return False

    return True


def isOKtags(tags:Tags)-> bool:

    judge = True

    for tag in tags:
        judge = judge and isOKtag(tag)

    return judge


class TagNotExsistError(Exception):
    """
    Exception raised when a tag is not in a set of tags
    """
    pass


class TagCharacterError(Exception):
    """
    Exception raised when a character of a tag is not appropriate
    """
    pass


class CodecTagNum(CodecTagBase):


    def __init__(self, tags:TagsX=None):

        # define variables 
        self.__tags:TagsX = None

        # set values of variables
        self.tags = tags


    @staticmethod
    def judge_tags(tags:Tags):

        if not isinstance(tags, (set, list, tuple)):
            raise TypeError("Specify the argument tag as a list or tuple object.")

        if not isOKtags(tags):
            raise TagCharacterError("A tag name has to consist of alphabets or '_' or '-'")


    @property
    def tags(self):
        return self.__tags


    @tags.settetr
    def tags(self, tags:Tags):
        CodecTagNum.judge_tags(tags)
        self.__tags = set(tags)


    @classmethod
    def encodec(cls, data:DataTagNumber, tags:Tags)-> str:

        cls.judge_tags(tags)
        
        if not isinstance(data, dict):
            raise TypeError("Specify the argument data as a dictionary object")

        data_encoded = ""
        for tag, val in data.items():

            if not isinstance(val, (float, int)):
                TypeError("Values of data have to be objects of float or int")

            tag, val = tuple(map(str, [tag, val]))

            if tag not in tags:
                raise TagNotExsistError("Cannot find specified tags from the tags variable")
            
            data_encoded += tag + val

        return data_encoded


    def encode(self, data:DataTagNumber)-> str:

        if isinstance(self.tag, type(None)):
            raise TagNotExsistError("The tags variable are not set yet")

        return CodecTagNum.encodec(data, self.tags)


    @classmethod
    def decodec(cls, data:str, tags:Tag)->dict:
        
        cls.judge_tags(tags)

        isTag = False
        isVal = False
        index_list = [0]

        for index, char in enumerate(data):
            if isOKtag(char):
                isTag = True
                if isVal:
                    index_list.append(index - 1)
                    isVal = False
            elif str.isdecimal(char):
                isVal = True
                if isTag:
                    index_list.append(index - 1)
                    isTag = False
            else:
                raise TagCharacterError("Given data includes an invailid character")

        index_list.append(len(data) - 1)

        data_decoded = {}
        for i in range(len(index_list) - 2):
            tag = data[index_list[i] : index_list[i + 1]]
            val = float(data[index_list[i + 1] : index_list[i + 2]])

            if tag not in tags:
                raise TagNotExsistError("Cannot find specified tags from the tags variable")

            data_decoded[tag] = val

        return data_decoded


    def decode(self, data:str)->dict:

        if isinstance(self.tag, type(None)):
            raise TagNotExsistError("The tags variable are not set yet")

        return CodecTagNum.decodec(data, self.tags)


    def decode_format(self, data:str)->dict:

        data_decoded = self.decode(data)
        for tag in self.tags:
            if tag not in data_decoded.keys:
                data_decoded[tag] = None
            
        return data_decoded