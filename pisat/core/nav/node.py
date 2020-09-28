#! python3

"""

pisat.core.nav.Node
~~~~~~~~~~~~~~~~~~~
A state class in a mission.
This class represents a state in a mission and 
users can define several callback functions in the class, 
which are called at each scheduled time of the functions.
This class is initialized by pisat system, not by users, 
which means those users have to do are override the callback 
functions and define a mission graph as a Context.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.nav.Context
pisat.core.cansat.CanSat
"""

from typing import Dict, Any, Tuple

from pisat.config.type import Logable
from pisat.core.manager.component_manager import ComponentManager
from pisat.core.nav.post_event import PostEvent


class Node:
    """A state class in a mission.
    
    This class represents a state in a mission and 
    users can define several callback functions in the class, 
    which are called at each scheduled time of the functions.
    This class is initialized by pisat system, not by users, 
    which means those users have to do are override the callback 
    functions and define a mission graph as a Context.
    
    The methods that users can override are below:
    
    - enter
    - judge
    - control
    - catched
    - verify
    - exit
    
    These methods are relative to lifecycle of a Node object.
    For example, the enter method is called as soon as a Node object 
    is initialized and the exti method is called just before the Node 
    object is dead, which means the object is no more referenced by 
    pisat system. More information, see these methods docstrings or 
    the developer documents.
    
    Attributes
    ----------
        is_feed : bool
            Whether data logging is needed, default True
        DNAMES_JUDGED: Tuple[str]
            Data names to be used for the 'judge' callback
            
    Notes
    -----
        If is_feed is False, a CanSat object gives Node.judge method 
        empty dictionary.  
    
    See Also
    --------
        pisat.core.nav.Context : It represents a mission graph.
        pisat.core.cansat.CanSat : Operator of a mission.
        Developer documents : https://github.com/jjj999/pisat/docs/developer
    """
    
    is_feed: bool = True
    DNAMES_JUDGED: Tuple[str] = ()

    def __init__(self, 
                 manager: ComponentManager,
                 event: PostEvent) -> None:
        """
        Parameters
        ----------
            manager : ComponentManager
                The ComponentManager which is set to a CanSat object.
            event : PostEvent
                The manager of the event that the judge method has emitted something.
        """
        self.manager: ComponentManager = manager
        self.event: PostEvent = event

    def enter(self) -> None:
        """Setup a Node object.
        
        This method is called as soon as a object of this class is initialized. 
        Users can define some setup operations in the method, such as 
        getting some components to be needed using the ComponentManager. 
        
        This method is executed only once by pisat system, and at the time, 
        pisat system manages only one thread, which may be the main thread or 
        other thread derived from another application. Therefore, You don't 
        have to care about some multi-threading problems. 
        
        This method is usually used to prepare execution of the control method. 
        You can freely setup some objects and retrieving several components, but 
        it is recommended not to retrieve components used in or for the judge 
        method because the control method and the judge method are executed 
        at the same time using muti-threading. Thus, you would have some problems 
        if you reference the components used in both methods. Consider using 
        RefQueue if you want to obtain logged data.
        
        See Also
        --------
            pisat.core.logger.DataLogger.refqueue : A property retrieving the RefQueue object.
            pisat.core.logger.RefQueue : Small container with latest logged data.
        """
        pass

    def judge(self, data: Dict[str, Logable]) -> Any:
        """Judge whether this Node has to move another Node.
        
        This method recieves the result of data logging of one time and try to 
        judge whether the data deserves to exit the current Node and move to 
        another Node. The method is executed in the main method, or the same 
        method pisat system running, and ran at the same time of running 
        the control method.
        
        This method can return any type of objects but the objects have to 
        be set to a Context object. Thus you have to define this method and 
        register the returned values to a Context simultaineously. 
        
        Pisat system determines to move to next Node from the current Node if 
        a returned value of this method is not the value to move to itself. 
        This means also that if you don't set the value for the Node itself and 
        only set values for other Nodes, then the pisat system try to judge 
        only once in the Node and move to other Nodes.
        
        Returned values of the method must indicates next Nodes uniquely.

        Parameters
        ----------
            data : Dict[str, Logable]
                Data logged by DataLogger.
            
        See Also
        --------
            pisat.core.cansat.CanSat.feed : This method uses the judge method inside.
        """
        pass

    def control(self) -> None:
        """Execute what a robot have to do in the Node.
        
        This method is called in the thread generated by the pisat system, and 
        the method is executed at the same time of executing the judge method. 
        Users can define operations in the method about what a robot have to do 
        in the Node, for example moving the robot. 
        
        It is strongly recommended not to reference components used in or for the judge 
        method because the control method and the judge method are executed 
        at the same time using muti-threading. Hanlding such components can cause 
        several problems about multi-threading. You have to take care about this 
        problem in order to make your application thread-safe. Consider using RefQueue 
        if you want to obtain logged data. 
        
        See Also
        --------
            pisat.core.logger.DataLogger.refqueue : A property retrieving the RefQueue object.
            pisat.core.logger.RefQueue : Small container with latest logged data.
        """
        pass
    
    def catched(self):
        pass
    
    def verify(self) -> bool:
        return True
        
    def exit(self) -> None:
        """Clean up this Node.
        
        This method is called just before the Node is dead, which means the method 
        is the last method users can define in a Node. This method is executed 
        in the main thread and at the time the control thread (the thread executing 
        the control method) is no longer alive. 
        
        This method is not intended specific operations but you can use the method 
        as the place where a robot can do some operations with no considering 
        operating time. 
        """
        pass
    