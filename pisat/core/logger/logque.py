#! python3

"""

pisat.core.logger.logque
~~~~~~~~~~~~~~~~~~~~~~~~
A container class of data logged by logging classes such as 
SensorController. This class also write cached data into a file 
automatically in the way of thread-safe. This class is a Component.

This class can only write the format List[str, Logable] or 
Tuple[str, Logable] data. If you want to the format Dict[str, Logable], 
then you can use DictLogQueue instead.

[info]
pisat.core.logger.DictLogQueue

"""

from collections import deque
from concurrent.futures import ThreadPoolExecutor
import csv
import math
from typing import Deque, Generic, Optional, TypeVar

from pisat.base.component import Component
from pisat.model.datamodel import DataModelBase
from pisat.util.about_time import get_time_stamp


Model = TypeVar("Model")


class LogQueue(Component, Generic[Model]):
    """Queue to manage data log with multiple threads.

    An abstract container class of data logged by logging classes such as 
    SensorController. This class also write cached data into a file 
    automatically in the way of thread-safe. This class is a Component.
    
    See Also
    --------
        pisat.core.logger.ListLogQueue : 
            Implementation of the class handling data with the format List[Logable].
        pisat.core.logger.DictLogQueue : 
            Implementation of the class handling data with the format Dict[str, Logable].
    """

    LEN_ADDING_TAIL = 10
    LEN_STANDARD_SMALL = 1000
    LEN_STANDARD_BIG = 10000
    LEN_MIN_SUB = 500
    LEN_MAX_SUB = 1000

    FILE_EXTENSION_DEFAULT = "csv"

    THREAD_MAX_WORKERS = 1

    def __init__(self,
                 modelclass: Model,
                 maxlen: int = 10000,
                 path: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Parameters
        ----------
            maxlen : int
                Size of the main queue.
            path : Optional[str], optional
                log file to be generated, by default None.
            name : Optional[str], optional
                name of this component, by default None.
        """
        super().__init__(name)
        
        if not issubclass(modelclass, DataModelBase):
            raise TypeError(
                "'modelclass' must a subclass of DataModelBase."
            )

        self._modelclass = modelclass

        self._limit_main: int = maxlen
        self._limit_sub: int = 0
        self._path = path
        self._thpool: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=self.THREAD_MAX_WORKERS)
        self._dnames = None
        self._first = True
        
        if path is None:
            self._path = get_time_stamp(self._modelclass.__name__, self.FILE_EXTENSION_DEFAULT)

        #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
        #   Inner Queues                                                            #
        #       : main, sub1, sub2                                                  #
        #                                                                           #
        #   Note                                                                    #
        #       1.  The 'main', 'sub1' and 'sub2' are all static.                   #
        #       2.  The 'sub' is reference to sub1 or sub2. The reference is to     #
        #           be changed in the _exchange_subque() when a sub is filled       #
        #           because of appending data.                                      #
        #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

        len_sub = self._calc_sublen(self._limit_main)
        self._queue_main: Deque[Model] = deque(maxlen=self._limit_main + self.LEN_ADDING_TAIL)
        self._queue_sub1: Deque[Model] = deque(maxlen=len_sub + self.LEN_ADDING_TAIL)
        self._queue_sub2: Deque[Model] = deque(maxlen=len_sub + self.LEN_ADDING_TAIL)
        self._queue_sub: Deque[Model] = self._queue_sub1
        self._limit_sub: int = len_sub

        self.create_newfile(self._path)
        
    @property
    def modelclass(self):
        return self._modelclass

    @classmethod
    def _calc_sublen(cls, len_main: int) -> int:
        """Calculate appropriate size of sub queues

        Returns
        -------
            int
                Calculated size.
        """
        if len_main < cls.LEN_STANDARD_SMALL:
            return cls.LEN_MIN_SUB
        elif len_main > cls.LEN_STANDARD_BIG:
            return cls.LEN_MAX_SUB
        else:
            return cls.LEN_MIN_SUB + \
                (cls.LEN_MAX_SUB - cls.LEN_MIN_SUB) * \
                int(math.log10(len_main / cls.LEN_STANDARD_SMALL))

    def _exchange_subque(self) -> Deque[Model]:
        """Exchange the reference of subque.

        Returns
        -------
            deque
                A subque set as the subque before this method is called.
        """
        if self._queue_sub is self._queue_sub1:
            self._queue_sub = self._queue_sub2
            return self._queue_sub1

        else:
            self._queue_sub = self._queue_sub1
            return self._queue_sub2

    def __len__(self):
        return len(self._queue_main)

    def __getitem__(self, key):
        return self._queue_main[key]

    @property
    def path(self):
        return self._path
    
    def create_newfile(self, 
                       path: Optional[str] = None, 
                       isexist: bool = False) -> None:
        """Creates new file for saving data log.
        
        The created file is used for the file into which data log is saved.
        The old file is never used for it.

        Parameters
        ----------
            path : Optional[str], optional
                New file to create or set, by default None.
            isexist : bool, optional
                whether the file exists, by default False.
        """
        if path is None:
            self._path = get_time_stamp(self._modelclass.__name__, self.FILE_EXTENSION_DEFAULT)
        elif isinstance(path, str):
            self._path = path
        else:
            raise TypeError(
                "'path' must be str or None."
            )
            
        if not isexist:
            self._first = True
            with open(self._path, "wt") as f:
                pass
            
    def _write(self, que: Deque[Model]) -> None:
        if not len(que):
            return
        
        with open(self._path, "at", newline="") as f:
            if self._first:
                self._dnames = que[0].extract().keys()
                
            writer = csv.DictWriter(f, self._dnames)
            if self._first:
                writer.writeheader()
                self._first = False
                
            while len(que):
                writer.writerow(que.popleft().extract())
                
    def close(self) -> None:
        """Execute post-process of logging.

        Notes
        -----
            If the method is not called and a program finishes, 
            then some cached data may not be saved into a file.
        """
        self._thpool.shutdown()
        self._write(self._queue_sub)
        self._write(self._queue_main)

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Context Manager                                                         #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Data Appending                                                          #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    def append(self, *x: Model) -> None:
        """Append data.

        Parameters
        ----------
            x : Any
                Data.
        """
        # Configure specified model using given data.
        model = self._modelclass(self.name)
        model.sync(*x)
        self._queue_main.append(model)

        if len(self._queue_main) >= self._limit_main:
            self._queue_sub.append(self._queue_main.popleft())

            if len(self._queue_sub) >= self._limit_sub:
                self.update()

    def update(self) -> None:
        """Exchange sub queue and save the old one.
        """
        d = self._exchange_subque()
        self._thpool.submit(self._write, d)
