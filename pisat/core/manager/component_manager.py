#! python3

"""

pisat.core.manager.component_manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A manager of components for searching internal components.
This class gives accessibility to internal components and 
users can retreive the components by using some methods 
of this class. 
 
"""

from typing import Dict, Optional, Tuple, Type

from pisat.base.component import Component
from pisat.base.component_group import ComponentGroup


class ComponentManager(ComponentGroup):
    """A manager of components for searching internal components.
    
    This class gives accessibility to internal components and 
    users can retreive the components by using some methods 
    of this class. 
    """
    
    def __init__(self,
                 *components: Component,
                 recursive: bool = False,
                 name: Optional[str] = None):
        """
        Parameters
        ----------
            *components : Tuple[Component, ...]
                Components to register
            recursive : bool, optional
                If registers inner components recursively, by default False
            name : Optional[str], optional
                Name of this component, by default None
            
        Notes
        -----
            If the 'recursive' argument is False, then only given components 
            are registerd into this object, which means this object recognizes 
            only given components and you can retreive only the components. 
            If the 'recursive' argument is True and some objects of the ComponentGroup 
            exsist, then the internal components of the component groups 
            are also set to this object. 
            
            This constructor uses 'append' method inside. If you want to 
            register components dynamically, you can use the 'append' method 
            instead. 
            
        Examples
        --------
            >> # SensorGroup is one of the component groups
            >> sensor_group = SensorGroup(sensor1, sensor2)
            >> manager = ComponentManager(sensor_group)
            >> manager.list()
            (SensorGroup,)
            >> 
            >> manager = ComponentManager(sensor_group, recursive=True)
            >> manager.list()
            (SensorGroup, Sensor1, Sensor2)
        """
        super().__init__(name=name)

        if len(components) > 0:
            self.append(*components, recursive=recursive)

    def append(self,
               *components: Tuple[Component, ...],
               recursive: bool = False):
        """
        Parameters
        ----------
            *components : Tuple[Component, ...]
                Components to register
            recursive : bool, optional
                If registers inner components recursively, by default False
            name : Optional[str], optional
                Name of this component, by default None
            
        Notes
        -----
            If the 'recursive' argument is False, then only given components 
            are registerd into this object, which means this object recognizes 
            only given components and you can retreive only the components. 
            If the 'recursive' argument is True and some objects of the ComponentGroup 
            exsist, then the internal components of the component groups 
            are also set to this object. 
            
        Examples
        --------
            >> manager = ComponentManager()
            >>
            >> # SensorGroup is one of the component groups
            >> sensor_group = SensorGroup(sensor1, sensor2)
            >> manager = manager.append(sensor_group)
            >> manager.list()
            (SensorGroup,)
            >> 
            >> manager = manager.append(sensor_group, recursive=True)
            >> manager.list()
            (SensorGroup, Sensor1, Sensor2)
        """
        super().append(*components)
        
        if not recursive:
            return
        
        def search_recursive(group: ComponentGroup, 
                             result: Dict[str, Component]):
            for name, member in group._NtoC.items():
                result[name] = member
                if isinstance(member, ComponentGroup):
                    search_recursive(member, result)
        
        result = {}
        for component in self._NtoC.values():
            if isinstance(component, ComponentGroup):
                search_recursive(component, result)
                
        self._NtoC.update(result)

    def search(self, objtype: Type) -> Tuple[str]:
        """Search registered components whose type given type matches.
        
        This method recieves a type of components and returns names of 
        components which matches the type. 
        
        Consider using the methods named 'get_component' or 'get_components' 
        if you want to get Component objects from names of components. 
        The methods are implemented in ComponentGroup class.

        Parameters
        ----------
            objtype : Type
                Subclass of Component class.

        Returns
        -------
            Tuple[str]
                Registered components whose type the given type matches.

        Raises
        ------
            TypeError
                Raised the given type is not a subclass of Component class.
                
        See Also
        --------
            pisat.base.ComponentGroup.get_component : 
                This method searches Component objects from names of the components.
        """
        if not issubclass(objtype, Component):
            raise TypeError(
                "'objtype' must be subclass of Component."
            )
        
        result = []
        for name, obj in self._NtoC.items():
            if isinstance(obj, objtype):
                result.append(name)

        return tuple(result)

    def list(self) -> Tuple[str]:
        """List names of registered components.

        Returns
        -------
            Tuple[str]
                List of names
        """
        return tuple(self._NtoC.keys())

    def detail(self) -> Dict[str, str]:
        """Represents detail of registered components as a dictionary.

        Returns
        -------
            Dict[str, str]
                Dictionary whose keys are names of components and values are 
                class names of the components.
        """
        return {name: obj.__class__.__name__ for name, obj in self._NtoC.items()}
