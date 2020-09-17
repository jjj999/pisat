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

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.DictLogQueue

"""


from typing import Any, Deque, Optional
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import math

from pisat.base.component import Component
from pisat.util.about_time import get_time_stamp


class LogQueue(Component):
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

    FILE_NAME_DEFAULT = "datalog"
    FILE_EXTENSION_DEFAULT = "csv"

    THREAD_MAX_WORKERS = 1

    def __init__(self,
                 maxlen: int,
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

        self._limit_main: int = maxlen
        self._limit_sub: int = 0
        self._path: str = get_time_stamp(
            self.FILE_NAME_DEFAULT, self.FILE_EXTENSION_DEFAULT) if not path else path
        self._thpool: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=self.THREAD_MAX_WORKERS)

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

        len_sub: int = self._calc_sublen(self._limit_main)
        self._queue_main: Deque[Any] = deque(
            maxlen=self._limit_main + self.LEN_ADDING_TAIL)
        self._queue_sub1: Deque[Any] = deque(
            maxlen=len_sub + self.LEN_ADDING_TAIL)
        self._queue_sub2: Deque[Any] = deque(
            maxlen=len_sub + self.LEN_ADDING_TAIL)
        self._queue_sub: Deque[Any] = self._queue_sub1
        self._limit_sub: int = len_sub

        self.create_newfile(self._path)

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

    def _exchange_subque(self) -> Deque[Any]:
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
            self._path = get_time_stamp(
                self.FILE_NAME_DEFAULT, self.FILE_EXTENSION_DEFAULT)
        elif isinstance(path, str):
            self._path = path
        else:
            raise TypeError(
                "'path' must be str or None."
            )

    def close(self) -> None:
        """Execute post-process of logging.

        This method must be implemented in subclasses as all data 
        is saved into a file with no contradiction.
        """
        self._thpool.shutdown()

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
    def append(self, x: Any) -> None:
        """Append data.

        Parameters
        ----------
            x : Any
                Data.
        """
        self._queue_main.append(x)

        if len(self._queue_main) >= self._limit_main:
            self._queue_sub.append(self._queue_main.popleft())

            if len(self._queue_sub) >= self._limit_sub:
                self.update()

    def _update(self, d: Deque[Any]) -> None:
        """subroutine to submit to the thread pool.
        
        This method must be implemented in subclasses as all given data 
        is saved into a file and given sub queue is cleared up.

        The subroutine plays a role in writing data log which has been
        piled up because of continuous logging. In other words, this 
        method saves data in 'sub queue' into a file.

        Parameters
        ----------
            d : Deque[Any]
                sub queue
        """
        pass

    def update(self) -> None:
        """Exchange sub queue and save the old one.
        """
        d = self._exchange_subque()
        self._thpool.submit(self._update, d)
