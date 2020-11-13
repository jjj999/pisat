#! python3

"""

pisat.core.nav.post_event
~~~~~~~~~~~~~~~~~~~~~~~~~
A Event object with a object as package.
This class gives the way of communication between threads 
in multi-threading. This class extends threading.Event class 
and has almost same feature as the class, but this class 
can have a single package when the internal flag get True.

[info]
https://docs.python.org/ja/3/library/threading.html
"""

from threading import Event
from typing import Any


class PostEvent(Event):
    """A Event object with a object as package.
    
    This class gives the way of communication between threads 
    in multi-threading. This class extends threading.Event class 
    and has almost same feature as the class, but this class 
    can have a single package when the internal flag get True.
    
    See Also
    --------
        threading.Event : Base class of this class.
        https://docs.python.org/ja/3/library/threading.html
    """

    def __init__(self):
        super().__init__()
        self._package = None

    @property
    def package(self):
        return self._package

    def set(self, package: Any):
        """Set the internal flag to true and a package.

        All threads waiting for it to become true are awakened. 
        Threads that call wait() once the flag is true will not 
        block at all. This method also can set package as a kind 
        of message.

        Parameters
        ----------
        package : Any
            A package send to other threads.
        """
        self._package = package
        super().set()

    def clear(self):
        """Reset the internal flag to false and the internal package.

        Subsequently, threads calling wait() will block until set() 
        is called to set the internal flag to true again.
        
        The internal package is reset None.
        """
        self._package = None
        super().clear()
