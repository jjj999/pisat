#! python3

"""

pisat.sensor.sensor.sensor_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The module which defines what a sensor is.
All classes in the module define sensor system.

SensorInterface represents the interface which a senser 
should have. The sensor system consists of objects of SensorBase 
and SensorGroup, and SensorInterface forms their backbone. 
SensorInterface is a Component.

SensorGroup represents a container of objects of SensorBase. 
SensorGroup is a ComponentGroup and also a SensorInterface, 
in other words, this class is like a sensor as a component group. 
A sensor group can make users access to internal sensors 
as a cluster of them, which means some methods of SensorGroup 
behave like ones of SensorBase are executed all at once.

SensorBase represents an element of the sensor set. 
Diversity of the sensor system is one of the classes of SensorBase. 
In the pisat system (or the sensor system) a sensor means 
an object of the SensorBase. The SensorBase should be inheritanced 
in most cases. A sensor represents a supplier of information about 
data retrieved from the sensor hardware. The main methods of the 
SensorBase are 'read' or 'readf' methods. These methods give users 
interfaces to retreive data of the hardware. Users can use 
some logging classes like SensorController and DataLogger in order to 
execute retreiving data from multiple sensor objects, and in the logging 
classes, sensors can be cooperated with sensors.

[info]
pisat.core.logger.SensorController
"""

from typing import Generic, Optional, TypeVar

from pisat.base.component import Component
from pisat.model.datamodel import DataModelBase
from pisat.model.linked_datamodel import LinkedDataModelBase
from pisat.handler.handler_base import HandlerBase


Model = TypeVar("Model", DataModelBase)
LinkedModel = TypeVar("LinkedModel", LinkedDataModelBase)


class HandlerMismatchError(Exception):
    """Raised if a given handler doesn't match required one."""
    pass


class HandlerNotSetError(Exception):
    """Raised if a hanler is not set when the handler is required."""
    pass


class SensorBase(Component, Generic[Model]):
    """An element of the sensor set. 
    
    Diversity of the sensor system is one of the classes of SensorBase. 
    In the pisat system (or the sensor system) a sensor means 
    an object of the SensorBase. The SensorBase should be inheritanced 
    in most cases. A sensor represents a supplier of information about 
    data retrieved from the sensor hardware. The main methods of the 
    SensorBase are 'read' or 'readf' methods. These methods give users 
    interfaces to retreive data of the hardware. Users can use 
    some logging classes like SensorController and DataLogger in order to 
    execute retreiving data from multiple sensor objects, and in the logging 
    classes, sensors can be cooperated with sensors.
    
    This class is an abstract class of sensors. Subclasses of this class 
    must override the read method. More information, see the references of 
    this class.
    """

    def __init__(self, 
                 handler: Optional[HandlerBase] = None, 
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            handler : Optional[HandlerBase], optional
                Handler object if required, by default None
            name : Optional[str], optional
                Name of the component, by default None
        """
        super().__init__(name=name)
        
        #   NOTE
        #       SensorBase does not force to use a handler
        #       in its subclasses. If you want not to use
        #       any handler, you should override __init__.
        
        self._handler: Optional[HandlerBase] = handler
        
    def read(self) -> Model:
        """Read data of sensor.
        
        This method is an abstract method. Implementation of the method 
        must return all readable data as a DataModel. 

        Returns
        -------
            DataModelBase
                A data model which has retrieved data from the sensor.
        """
        pass
        