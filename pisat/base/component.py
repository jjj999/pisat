#! python3

"""

pisat.core.base.component
~~~~~~~~~~~~~~~~~~~~~~~~~
The class defines what a component of pisat is.
The purpose of this class is to make common interfaces 
of objects used in the pisat sytem. Many classes in 
pisat inheritance this class.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.
"""

from typing import Optional


class Component:
    """The class defines what a component of pisat is.
    
    The purpose of this class is to make common interfaces 
    of objects used in the pisat sytem. Many classes in 
    pisat inheritance this class.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            name : Optional[str], optional
                Name of the component, by default None.

        Raises
        ------
            TypeError
                Raised if the 'name' is not str or None.
        """
        if not (name is None or isinstance(name, (str))):
            raise TypeError(
                "'name' must be str or None."
            )
            
        self._name = name
        
    @property
    def name(self):
        if self._name is None:
            return self.__class__.__name__
        else:
            return self._name
            
    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(
                "'name' must be str."
            )
        self._name = name