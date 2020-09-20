#! python3

"""

pisat.comm.formatter.tnsf
~~~~~~~~~~~~~~~~~~~~~~~~~
tnsf -> tag-number simple format

[author]
AUTHOR NAME, ORGANIZATION NAME

[info]
OTHER INFORMATION
    
"""

from io import FileIO
from typing import Dict, List, Union

from pisat.config.type import Logable


class tnsf:
    
    @classmethod
    def dump(cls, obj: Dict[str, Logable]) -> bytes:
        pass
    
    @classmethod
    def dumps(cls, obj: Dict[str, Logable]) -> str:
        pass
    
    @classmethod
    def load(cls, fp: FileIO) -> List[Dict[str, Logable]]:
        pass
    
    @classmethod
    def loads(cls, raw: Union[str, bytes, bytearray]) -> List[Dict[str, Logable]]:
        pass
    