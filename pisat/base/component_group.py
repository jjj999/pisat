#! python3

"""

pisat.base.component_group
~~~~~~~~~~~~~~~~~~~~~~~~~~
The group of components.
This class represents a group of components, which means objects of 
this class hold some objects of Component inside. This class can 
make users access to internal components through some methods. 
Objects of this class is also a component.

[info]
pisat.base.Component
"""

from typing import Dict, Optional, Tuple
from pisat.base.component import Component


class ComponentGroup(Component):
    """The group of components in the pisat system.
    
    This class represents a group of components, which means objects of 
    this class hold some objects of Component inside. This class can 
    make users access to internal components through some methods. 
    Objects of this class is also a component.
    
    See Also
    --------
        pisat.base.Component : A component group holds some components.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            name : Optional[str], optional
                Name of the component, by default None
        """
        super().__init__(name=name)
        
        # Map from names to internal components
        self._NtoC: Dict[str, Component] = {}
        
    def append(self, *components: Tuple[Component, ...]):
        """Append components to the inside.
        
        Parameter
        ---------
            *components : Tuple[Component, ...]
                Components to be registered inside the component group.

        Raises
        ------
            NotImplementedError
                Raised if given objects are not components.
        """
        for component in components:
            if not isinstance(component, Component):
                raise NotImplementedError(
                    "A given object has not implemented Component class."
                )

            self._NtoC[component.name] = component
    
    def get_component(self, name: str) -> Optional[Component]:
        """Retrieve a component from its name.
        
        This method returns a None if the given name doesn't match 
        any names of internal components of the component group.

        Parameters
        ----------
            name : str
                Name of the component.

        Returns
        -------
            Optional[Component]
                Component whose name matches the given name if exists.

        Raises
        ------
            TypeError
                Raised if the given name is not str.
        """
        if not isinstance(name, str):
            raise TypeError(
                "'name' must be str."
            )
            
        return self._NtoC.get(name)

    def get_components(self, *names: Tuple[str, ...]) -> Dict[str, Component]:
        """Retrieve components from their names.
        
        This method returns the result as a dictionary, whose keys are 
        names of components and values are objects of Component. If no 
        given names match names of internal components, then a empty 
        dictionary is returned.
        
        This method uses the 'get_component' method inside.
        
        Parameters
        ----------
            *names : Tuple[str, ...]
                Names of components for retrieving.

        Returns
        -------
            Dict[str, Component]
                Components whose names match the given names if exists.
        """
        result = {}
        for name in names:
            obj = self.get_component(name)
            if obj is not None:
                result[name] = obj
                
        return result