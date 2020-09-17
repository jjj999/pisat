#! python3

"""

pisat.core.cansat.cansat
~~~~~~~~~~~~~~~~~~~~~~~~
A top level class of mission.
This class manages a mission by scheduling lifecycle of a Node,
using given Context information.

This class is the mission executor, so it is deprecated for users
to call methods of the class except of 'run' method.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.nav.Context
pisat.core.nav.Node
pisat.core.logger.DataLogger
pisat.core.logger.SystemLogger
pisat.core.manager.ComponentManager
"""

from threading import Thread
from typing import Any, Dict, Optional, Type

from pisat.config.type import Logable
from pisat.core.manager.component_manager import ComponentManager
from pisat.core.logger.datalogger import DataLogger
from pisat.core.logger.systemlogger import SystemLogger
from pisat.core.nav.node import Node
from pisat.core.nav.context import Context
from pisat.core.nav.post_event import PostEvent


class CanSat:
    """A top level class of mission.
    
    This class manages a mission by scheduling lifecycle of a Node,
    using given Context information.

    This class is the mission executor, so it is deprecated for users
    to call methods of the class except of 'run' method.

    See Also
    --------
        pisat.core.nav.Context : Represents graph of a mission flow.
        pisat.core.nav.Node : Represents a state in a mission.
        pisat.core.logger.DataLogger : Logger collecting Sensor and Adapter data.
        pisat.core.logger.SystemLogger : Logger registering system log.
        pisat.core.manager.ComponentManager : Container of Components as a search engine.
    """
    
    TIMEOUT_CONTROL_THREAD = 1.
    
    # Default log messages
    MESSAGE_NODE_ENTER = "enter"
    MESSAGE_NODE_JUDGE_START = "start judge"
    MESSAGE_NODE_JUDGE_DETECTED = "detected"
    MESSAGE_NODE_JUDGE_FINISH = "finish judge"
    MESSAGE_NODE_JUDGE_RESTART = "restart judge"
    MESSAGE_NODE_VERIFY_SUCCEEDED = "verify succeeded"
    MESSAGE_NODE_VERIFY_FAILED = "verify failed"
    MESSAGE_NODE_CONTROL_START = "start control"
    MESSAGE_NODE_CONTROL_FINISH = "finish control"
    MESSAGE_NODE_EXIT = "exit"
    
    def __init__(self, 
                 context: Context,
                 manager: ComponentManager,
                 dlogger: Optional[DataLogger] = None,
                 slogger: Optional[SystemLogger] = None) -> None:
        """
        Parameters
        ----------
            context : Context
                Mission context set with several Nodes or a single Node.
            manager : ComponentManager
                ComponentManager set with several Components to use in the mission.
            dlogger : Optional[DataLogger], optional
                DataLogger for logging Sensor and Adapter data, by default None
            slogger : Optional[SystemLogger], optional
                SystemLogger for logging system log, by default None

        Raises
        ------
            TypeError
                Raised if 'context' is not Context.
            TypeError
                Raised if 'manager' is not ComponentManager.
            TypeError
                Raised if 'dlogger' is not DataLogger.
            TypeError
                Raised if 'slogger' is not SystemLogger.
        """
        if not isinstance(context, Context):
            raise TypeError(
                "'context' must be Context, but {} was given."
                .format(context.__class__.__name__)
            )
        if not isinstance(manager, ComponentManager):
            raise TypeError(
                "'manager' must be ComponentManager, but {} was given."
                .format(manager.__class__.__name__)
            )
        
        self._context: Context = context
        self._manager: ComponentManager = manager
        self._dlogger: Optional[DataLogger] = dlogger
        self._slogger: Optional[SystemLogger] = slogger
        
        self._current: Type[Node] = self._context.current
        self._destination: Dict[Any, Type[Node]] = self._context.destination
        
        self._buf: Dict[str, Logable] = {}
        self._event: PostEvent = PostEvent()
        self._node: Node = self._current(self._manager, self._event)
        
        #   NOTE
        #       DataLogger and SystemLogger have to be given explicitly.
        
        self._is_feed: bool = True
        self._is_logging: bool = True
        
        if self._dlogger is None:
            self._is_feed = False
        else:
            if not isinstance(self._dlogger, DataLogger):
                raise TypeError(
                    "'dlogger' must be DataLogger."
                )
                
        if self._slogger is None:
            self._is_logging = False
        else:
            if not isinstance(self._slogger, SystemLogger):
                raise TypeError(
                    "'slogger' must be SystemLogger."
                )
                
    def log(self, node: Type[Node], msg: str):
        """Logging system log related with given Node.

        Parameters
        ----------
            node : Type[Node]
                Node class
            msg : str
                Message logged

        Raises
        ------
            TypeError
                Raised if 'node' is not subclass of Node.
        """
        if not issubclass(node, Node):
            raise TypeError(
                "'node' must be a subclass of Node."
            )
        
        if self._slogger is not None:
            msg = "{} : {}".format(node.__name__, msg)
            self._slogger.info(msg)
        
    def enter(self):
        """Execute 'enter' method of the current Node.
        
        This method is called as soon as last Node is dead and new 
        Node object is created. A user should override Node.enter 
        method if wants to set something up.
        """
        self._node.enter()
        
    def feed(self) -> Any:
        """Execute the transaction for data logging and flag observation.
        
        This method reads data from DataLogger if it is set, gives 
        'judge' method of the current Node the result, and returns
        returned value from the judge method. Therefore, frequency of 
        execution of this method means sampling rate of the machine. 
        
        This method feeds empty dictionary to the judge method of the 
        current Node when a DataLogger object is not given in the time of  
        initialization of a CanSat object or when the class variable 'is_feed' of 
        the current Node is set as False. If a DataLogger object is not set, 
        then retrieving data is always ignored in all Nodes, even if 'is_feed' 
        variables of some Nodes are set as True.

        Returns
        -------
            Any
                Result of giving Node.judge logged data.
        """
        # self._is_feed         --> CanSat setting
        # self._current.is_feed --> Node setting
        if self._current.is_feed and self._is_feed:
            data = self._dlogger.read()
            for dname in data.keys():
                self._buf[dname] = data[dname]
                
            return self._node.judge(self._buf)
        else:
            return self._node.judge({})
            
    def exit(self):
        """Execute 'exit' method of the current Node.
        
        This method is called just befor the current Node is dead.
        A user can override Node.exit and schedule executing the method.
        """
        self._node.exit()
        self._buf.clear()
        
    def cycle(self) -> Any:
        """Execute lifecycle of the current Node
        
        This method operates lifecycle fo the current Node and 
        outputs the reason of death.

        Returns
        -------
            Any
                Flag the current Node emitted for moving next Node.
        """
        self.log(self._current, self.MESSAGE_NODE_ENTER)
        self.enter()
        
        th_control = Thread(target=self._node.control)
        self.log(self._current, self.MESSAGE_NODE_CONTROL_START)
        th_control.start()
        
        self.log(self._current, self.MESSAGE_NODE_JUDGE_START)
        while True:
            judged = self.feed()
            
            if self._destination[judged] is not self._current:
                break
        self.log(self._current, 
                 "{} {}".format(self.MESSAGE_NODE_JUDGE_DETECTED, judged))
        
        self.log(self._current, self.MESSAGE_NODE_JUDGE_FINISH)
        self._event.set(judged)
        
        while th_control.is_alive():
            th_control.join(timeout=self.TIMEOUT_CONTROL_THREAD)
        self.log(self._current, self.MESSAGE_NODE_CONTROL_FINISH)
        
        self.exit()
        self._event.clear()
        self.log(self._current, self.MESSAGE_NODE_EXIT)
        
        return judged
        
            
    def run(self):
        """Run scheduled mission.
        
        This method is an only entry-point for starting a mission.
        In most case, users would use only this method of the class
        because the other methods are usually called in the method.
        """
        try:
            while True:
                judged = self.cycle()
                # update context
                if self._current in self._context.end and self._destination[judged] is None:
                    break
                else:
                    node_next = self._context.next(judged)
                    self._current = self._context.current
                    self._destination = self._context.destination
                    self._node = node_next(self._manager, self._event)
        except KeyboardInterrupt:
            pass
        finally:
            self._dlogger.close()