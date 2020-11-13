#! python3

"""

pisat.core.nav.context
~~~~~~~~~~~~~~~~~~~~~~
Context for navigation of an operational flow.
This class represents graph of a mission flow. A mission flow consists of 
several Nodes and their flags for moving other Nodes from the current Node. 
The flags are just returned values of Node.judge method, and when one of the 
values is given, a Context object should resolve the next Node uniquely. 

The pisat system is the system in which many Nodes, or many states, have 
relations to each other and a mission is going with occurring many transitions 
from a Node to another Node. In a Node, the system does what to operate scheduled 
by user while observing the transition flag. The way to transitions should be 
holded by a Context object and how to behave in a state should be defined in a Node.

[info]
pisat.core.nav.Node
"""

from typing import Dict, Any, Type, Union, Optional, List

from pisat.core.nav.node import Node
from pisat.model.linked_datamodel import LinkedDataModelBase


class ConditionMismatchError(Exception):
    "Raised when given condition doesn't match of given nodes."
    pass


class NotExistNextNodeError(Exception):
    "Raised when next node is called, but the node doesn't exist."
    pass


class Context:
    """Context for navigation of an operational flow.

    This class represents graph of a mission flow. A mission flow consists of 
    several Nodes and their flags for moving other Nodes from the current Node. 
    The flags are just returned values of Node.judge method, and when one of the 
    values is given, a Context object should resolve the next Node uniquely. 
    
    The pisat system is the system in which many Nodes, or many states, have 
    relations to each other and a mission is going with occurring many transitions 
    from a Node to another Node. In a Node, the system does what to operate scheduled 
    by user while observing the transition flag. The way to transitions should be 
    holded by a Context object and how to behave in a state should be defined in a Node.
    
    See Also
    --------
        pisat.core.nav.Node : Represents a node of the graph.
    """

    #   EXAMPLE OF STRUCTURE OF A FLOW
    #
    #   {
    #       ...,
    #       [node class: Node]: {
    #           [node.judge() return1]: [next node1 class: Node],
    #           [node.judge() return2]: [next node2 class: Node],
    #           [node.judge() return3]: [next node3 class: Node]
    #       },
    #       ...,
    #   }
    #
    #

    def __init__(self,
                 flow: Optional[Dict[Type[Node], Dict[Any, Union[Type[Node], None]]]] = None,
                 start: Optional[Type[Node]] = None):
        """
        Parameters
        ----------
            flow : Optional[Dict[Type[Node], Dict[Any, Union[Type[Node], None]]]], optional
                A mission flow, by default None.
            start : Optional[Type[Node]], optional
                Start Node in the flow, by default None.
                
        Raises
        ------
            Raised if two parameters both are not given at the same time.
                
        Notes
        -----
            The 'flow' argument must be the defined format as Examples show.
            The type of this flow is Dict[Node, Dict[Any, Union[Node, None]]].
            A user can specify the first Nodes, or keys of the flow dictionary, 
            for all Nodes used in a mission. The second Nodes, or values of values 
            of the flow, are goals from the first Nodes, which means the second 
            Nodes can be next Nodes of the first Nodes. Keys of the second Nodes 
            are values of flags for moving next Nodes from the current Node, 
            which the first Nodes can be. 
            
            The 'start' argument must be included the first Nodes of the flow 
            argument. A specified Node as the 'start' is called first by 
            the pisat system.
            
            Two arguments 'flow' and 'start' both must be given at the same 
            time. If not, ValueError is raised.
            
        Examples
        --------
            >> flow = {
                
                    Node1: {
                        1: Node2,
                        2: Node3,
                        3: Node1
                    }, 
                    
                    Node2: {
                        True: Node3,
                        False: Node2
                    },
                    
                    Node3: {
                        True: None,
                        False: Node3
                    }
                }
                
            >> # set flow and the start Node and initilize
            >> context = Context(flow, start=Node1)
        """

        self._flow: Dict[Type[Node], Dict[Any, Type[Node]]] = {}
        # start node must be only one.
        self._start: Type[Node] = None
        # end node is not necessarily only one.
        self._end: List[Type[Node]] = []
        
        # NOTE
        #   Context always holds Nodes as Classes.
        #   Instanciation of Nodes is held in the CanSat.
        self._current: Type[Node] = None
        self._pre: Type[Node] = None

        # 'flow' and 'start' must be given simultaneously.
        if flow is not None and start is not None:
            self.set_flow(flow, start)
        else:
            if flow is None and start is None:
                pass
            else:
                ValueError(
                    "'start' is also required when 'flow' is given," +
                    " and vice versa."
                )

    def set_node(self,
                 node: Type[Node],
                 dest: Dict[Any, Union[Type[Node], None]],
                 start: bool = False) -> None:
        """Set a Node and its destination.
        
        This method set a single Node. Consider using 'set_flow' method 
        if you want to set a Context object at once.

        Parameters
        ----------
            node : Type[Node]
                A Node which will be one of the first Node of the flow.
            dest : Dict[Any, Union[Type[Node], None]]
                Destination of the 'node'.
            start : bool, optional
                If the 'node' is the start Node or not, by default False

        Raises
        ------
            TypeError
                Raised if 'node' is not subclass of Node.
            TypeError
                Raised if values of 'dest' are not subclasses of Node.
            ValueError
                Raised if 'start' has been already set.
                
        Notes
        -----
            The 'dest' argument must follow the format as Examples show. 
            The format is same as values of the 'flow' argument of 
            'set_flow' method. 
            
        Examples
        --------
            >> context = Context()
            >> dest1 = {1: Node2, 2: Node3, 3: Node1}
            >> context.set_node(Node1, dest1, start=True)
            >>
            >> dest2 = {True: Node3, False: Node2}
            >> context.set_node(Node2, dest2)
            
        See Also
        --------
            pisat.core.nav.Context.set_flow : The method set a flow at once.
        """

        # check if given 'node' is appropriate.
        if not issubclass(node, Node):
            raise TypeError(
                "'node' must be a subclass of Node class"
            )

        # check if given 'destination' is appropriate.
        for goal in dest.values():
            if not (issubclass(goal, Node) or goal is None):
                raise TypeError(
                    "Values of 'dest' must be subclasses of Node class or None."
                )
                
        # check if a data model is given
        if not issubclass(node.model, LinkedDataModelBase) or node.model is not None:
            raise TypeError(
                f"'model' of Node must be a subclass of {LinkedDataModelBase.__name__} or None."
            )

        if start:
            # check if the start node is duplicated
            if self._start is None:
                self._start = node
                self._current = self._start
            else:
                raise ValueError(
                    "The Start Node has been already set."
                )

        self._flow[node] = dest

        for val in dest.values():
            if val is None:
                self._end.append(node)

    def set_flow(self,
                 flow: Dict[Type[Node], Dict[Any, Union[Type[Node], None]]],
                 start: Type[Node]) -> None:
        """Set a mission flow at once.

        Parameters
        ----------
        flow : Dict[Type[Node], Dict[Any, Union[Type[Node], None]]]
            A mission flow.
        start : Type[Node]
            The start Node in the flow.
            
        Notes
        -----
            The 'flow' argument must be the defined format as Examples show.
            The type of this flow is Dict[Node, Dict[Any, Union[Node, None]]].
            A user can specify the first Nodes, or keys of the flow dictionary, 
            for all Nodes used in a mission. The second Nodes, or values of values 
            of the flow, are goals from the first Nodes, which means the second 
            Nodes can be next Nodes of the first Nodes. Keys of the second Nodes 
            are values of flags for moving next Nodes from the current Node, 
            which the first Nodes can be. 
            
            The 'start' argument must be included the first Nodes of the flow 
            argument. A specified Node as the 'start' is called first by 
            the pisat system.
            
            Two arguments 'flow' and 'start' both must be given at the same 
            time. If not, ValueError is raised.
            
            If want, you can set a flow at the time of initialization of a Context. 
            The constructor of this class automatically calls the 'set_flow' method 
            inside if the 'flow' and 'start' both are given.
            
        Examples
        --------
            >> flow = {
                
                    Node1: {
                        1: Node2,
                        2: Node3,
                        3: Node1
                    }, 
                    
                    Node2: {
                        True: Node3,
                        False: Node2
                    },
                    
                    Node3: {
                        True: None,
                        False: Node3
                    }
                }
                
            >> # set flow and the start Node and initilize
            >> context = Context(flow, start=Node1)
        """

        for node, dest in flow.items():
            self.set_node(node, dest)

        # 'start' must be a Node.
        if not issubclass(start, Node):
            raise(
                "'start' must be a subclass of Node class."
            )

        # 'start' must be included in 'flow'.
        if start not in flow.keys():
            raise(
                "'start' isn't included in your 'flow'."
            )

        self._start = start
        self._current = self._start

    @property
    def current(self):
        return self._current

    @property
    def pre(self):
        return self._pre

    @property
    def destination(self):
        return self._flow[self._current]

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return tuple(self._end)

    def next(self, cond: Any) -> Type[Node]:
        """Output appropriate next Node from given condition.
        
        Users must set a flow using other methods before the method is 
        called. In most cases, users don't have to execute the method 
        explicitly because this method is called in a CanSat object 
        as a part of lifecycle handling. 

        Parameters
        ----------
        cond : Any
            A condition which is returned from Node.judge method.

        Returns
        -------
        Type[Node]
            Next Node.

        Raises
        ------
        ConditionMismatchError
            Raised if given condition does not match flags already set.
        NotExistNextNodeError
            Raised if the current Node does not have next nodes.
        """
        
        self._pre = self._current
        try:
            self._current = self._flow[self._current][cond]
            return self._current
        except KeyError:
            raise ConditionMismatchError(
                "Given condition {} is not found in the node" +
                "'{}'".format(cond, self.current.__name__)
            )
        except TypeError:
            raise NotExistNextNodeError(
                "The current Node '{}' doesn't have next node."
                .format(self._current.__name__)
            )
