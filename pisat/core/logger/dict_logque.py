#! python3

"""

pisat.core.logger.dict_logque
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A container class of data logged by logging classes such as 
SensorController. This class also write cached data into a file 
automatically in the way of thread-safe. This class is a Component.

This class can only write the format Dict[str, Logable] data. If you 
want to the format List[Logable], then you can use LogQueue instead.
This class extends the LogQueue class, therefore has almost same 
interface, but this class needs data name (dnames) in order to indentify
what data is the data.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.LogQueue

"""

import csv
from typing import Deque, Dict, List, Optional, Tuple, Union

from pisat.config.type import Logable
from pisat.core.logger.logque import LogQueue
from pisat.util.about_time import get_time_stamp


class DictLogQueue(LogQueue):
    """Queue extended for using dict data.
    
    A container class of data logged by logging classes such as 
    SensorController. This class also write cached data into a file 
    automatically in the way of thread-safe. This class is a Component.

    This class can only write the format Dict[str, Logable] data. If you 
    want to the format List[Logable], then you can use ListLogQueue instead.
    
    This class extends the LogQueue class, therefore has almost same 
    interface, but this class needs data name (dnames) in order to indentify
    what data is the data.
    
    See Also
    --------
        pisat.core.logger.LogQueue : Base class of this class
        pisat.core.logger.ListLogQueue : 
            Implementation of the class handling data with the format List[Logable].
    """
    
    def __init__(self,
                 maxlen: int,
                 dnames: Union[Tuple[str], List[str]],
                 path: Optional[str] = None,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            maxlen : int
                Size of main queue, which is visible.
            dnames : Union[Tuple[str], List[str]]
                data names if you want to save, by default None.
            path : Optional[str], optional
                log file to be generated, by default None.
            name : Optional[str], optional
                name of this component, by default None.
        """
        
        self._dnames: Tuple[str] = tuple(dnames)
        super().__init__(maxlen, path=path, name=name)
        
    @property
    def dnames(self):
        return self._dnames
    
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
            self._path = get_time_stamp(self.FILE_NAME_DEFAULT, self.FILE_EXTENSION_DEFAULT)
        elif isinstance(path, str):
            self._path = path
        else:
            raise TypeError(
                "'path' must be str or None."
            )
            
        if isexist:
            with open(self._path, "wt") as f:
                writer = csv.DictWriter(f, self._dnames)
                writer.writeheader()
                
    def close(self) -> None:
        """Execute post-process of logging.

        Notes
        -----
            If the method is not called and a program finishes, 
            then some cached data may not be saved into a file.
        """
        self._thpool.shutdown()
        
        with open(self._path, "at", newline="") as f:
            writer = csv.DictWriter(f, self._dnames)
            while len(self._queue_sub):
                writer.writerow(self._queue_sub.popleft())
            while len(self._queue_main):
                writer.writerow(self._queue_main.popleft())
                
    def _update(self, d: Deque[Dict[str, Logable]]) -> None:
        """subroutine to submit to the thread pool.

        The subroutine plays a role in writing data log which has been
        piled up because of continuous logging. In other words, this 
        method saves data in 'sub queue' into a file.

        Parameters
        ----------
            d : Deque[Dict[str, Logable]]
                sub queue
        """
        with open(self._path, "at", newline="") as f:
            writer = csv.DictWriter(f, self._dnames)
            while len(d) > 0:
                writer.writerow(d.popleft())
                