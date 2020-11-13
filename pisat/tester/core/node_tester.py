
from typing import Any, Dict, Optional, Sequence, Tuple, Type

from pisat.tester.tester_base import Tester
from pisat.tester.core.util import simulate_judge_from, simulate_judge_from_all
from pisat.core.nav.node import Node
from pisat.core.nav.post_event import PostEvent
from pisat.core.manager.component_manager import ComponentManager
from pisat.core.logger.datalogger import DataLogger


class InappropriateDestinationError(Exception):
    """Raised if inappropriate destination of Node is found."""
    pass


class NodeTester(Tester):
    
    def __init__(self,
                 node: Type[Node],
                 manager: ComponentManager,
                 my_flag: Optional[Any] = None,
                 dlogger: Optional[DataLogger] = None) -> None:
        
        self._node: Type[Node] = node
        self._manager: ComponentManager = manager
        self._my_flag = my_flag
        self._dlogger: Optional[DataLogger] = dlogger
        self._event: PostEvent = PostEvent()
        
        self._current: Optional[Node] = None
        
    def setup(self, manager: Optional[ComponentManager] = None):
        if manager is not None:
            self._manager = manager
        self._event.clear()
        self._current = self._node(self._manager, self._event)
        self._current.enter()
        
    def simulate_judge(self, 
                       data,
                       manager: Optional[ComponentManager] = None) -> int:
        """Simulate Node.judge callback from given data and find the index 
        on which a flag is detected.
        
        This method executes the judge callback of the internal Node with 
        given data and returns the result as the index on which an internal 
        flag is triggered. If any flags are not triggered, then the method
        returns -1, and if the flag to myself is not given at initialization, 
        then this method always returns 0.

        Parameters
        ----------
            data : Sequence[Dict[str, Logable]]
                Data for simulating
            manager : Optional[ComponentManager], optional
                ComponentManager if needed to update, by default None

        Returns
        -------
            int
                The index on which an internal flag is triggered.
        """
        if self._my_flag is None:
            return 0
        
        self.setup(manager=manager)
        
        for i, d in enumerate(data):
            judged = self._current.judge(d)
            if judged != self._my_flag:
                return i
        else:
            return -1
    
    def simulate_judge_all(self,
                           data,
                           manager: Optional[ComponentManager] = None) -> Tuple[Any]:
        """Simulate Node.judge callback by feeding given all data.

        This method executes the judge callback of the internal Node with 
        given data and collects the results of the judge callback.

        Parameters
        ----------
            data : Sequence[Dict[str, Logable]]
                Data for simulating
            manager : Optional[ComponentManager], optional
                ComponentManager if needed to update, by default None

        Returns
        -------
            Tuple[Any]
                Returned results from the judge callback.
        """
        
        self.setup(manager=manager)
        
        result = []
        for d in data:
            result.append(self._current.judge(d))
            
        return tuple(result)
    
    def simulate_judge_from(self,
                            path: str,
                            dnames: Optional[Sequence[str]] = None,
                            manager: Optional[ComponentManager] = None) -> int:
        """Simulate Node.judge callback with given data file and find the index 
        on which a flag is detected.
        
        This method executes the judge callback of the internal Node with 
        data in given file and returns the result as the index on which an internal 
        flag is triggered. If any flags are not triggered, then the method
        returns -1, and if the flag to myself is not given at initialization, 
        then this method always returns 0.

        Parameters
        ----------
            path : str
                Path of a csv file.
            dnames : Optional[Sequence[str]], optional
                Data names if the csv file doesn't have them, by default None
            manager : Optional[ComponentManager], optional
                ComponentManager if needed to update, by default None

        Returns
        -------
            int
                The index on which an internal flag is triggered.
                
        Raises
        ------
            ValueError
                path must reprents path of a csv file.
        """
        self.setup(manager=manager)
        try:
            return simulate_judge_from(self._current.judge, self._my_flag, path, dnames=dnames)
        except ValueError:
            return 0
        
    def simulate_judge_from_all(self,
                                path: str,
                                dnames: Optional[Sequence[str]] = None,
                                manager: Optional[ComponentManager] = None) -> Tuple[Any]:
        """Simulate Node.judge callback by feeding all data from given file.

        This method executes the judge callback of the internal Node with 
        data in given file and collects the results of the judge callback.

        Parameters
        ----------
            path : str
                Path of a csv file.
            dname : Optional[Sequence[str]], optional
                Data names if the csv file doesn't have them, by default None
            manager : Optional[ComponentManager], optional
                ComponentManager if needed to update, by default None

        Returns
        -------
            Tuple[Any]
                Returned results from the judge callback.

        Raises
        ------
            ValueError
                path must reprents path of a csv file.
        """
        self.setup(manager=manager)
        return simulate_judge_from_all(self._current.judge, path, dnames=dnames)
        