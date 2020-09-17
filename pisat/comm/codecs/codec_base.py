
"""
TODO

* コーデックの型定義を簡単にしておく
* 自由度が出るようにはしておく

"""


from abc import ABC, abstractmethod


class CodecBase(ABC):

    @abstractmethod
    def encode(self, data):
        pass

    @classmethod
    @abstractmethod
    def encodec(cls, data):
        pass

    @abstractmethod
    def decode(self, data):
        pass

    @classmethod
    @abstractmethod
    def decodec(cls, data):
        pass


class CodecTagBase(ABC, CodecBase):

    @property
    @abstractmethod
    def tag(self):
        pass

    @tag.setter
    @abstractmethod
    def tag(self, tag):
        pass

    @classmethod
    @abstractmethod
    def encodec(cls, data, tags):
        pass

    @classmethod
    @abstractmethod
    def decodec(cls, data, tags):
        pass