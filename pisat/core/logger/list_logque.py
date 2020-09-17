
import csv
from typing import Deque, List, Optional, Tuple, Union

from pisat.config.type import Logable
from pisat.core.logger.logque import LogQueue


class ListLogQueue(LogQueue):
    """LogQueue to handling data with the format of list.

    An container class of data logged by logging classes such as 
    SensorController. This class also write cached data into a file 
    automatically in the way of thread-safe. This class is a Component.

    This class can only write the format List[str, Logable] or 
    Tuple[str, Logable] data. If you want to the format Dict[str, Logable], 
    then you can use DictLogQueue instead.
    
    See Also
    --------
        pisat.core.logger.LogQueue : Base class of this class.
        pisat.core.logger.DictLogQueue : 
            Implementation of the class handling data with the format Dict[str, Logable].
    """
    
    def __init__(self,
                 maxlen: int,
                 path: Optional[str] = None,
                 name: Optional[str] = None) -> None:
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
        super().__init__(maxlen, path=path, name=name)
        
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
        super().create_newfile(path=path, isexist=isexist)

        if isexist:
            with open(self._path, "wt") as f:
                pass
            
    def close(self) -> None:
        """Execute post-process of logging.

        Notes
        -----
            If the method is not called and a program finishes, 
            then some cached data may not be saved into a file.
        """
        super().close()

        with open(self._path, "at", newline="") as f:
            writer = csv.writer(f)
            while len(self._queue_sub):
                writer.writerow(self._queue_sub.popleft())
            while len(self._queue_main):
                writer.writerow(self._queue_main.popleft())
                
    def _update(self, d: Deque[Union[List[Logable], Tuple[Logable]]]) -> None:
        """subroutine to submit to the thread pool.

        The subroutine plays a role in writing data log which has been
        piled up because of continuous logging. In other words, this 
        method saves data in 'sub queue' into a file.

        Parameters
        ----------
            d : Deque[Union[List[Logable], Tuple[Logable]]]
                sub queue
        """
        with open(self._path, "at", newline="") as f:
            writer = csv.writer(f)
            while len(d) > 0:
                writer.writerow(d.popleft())