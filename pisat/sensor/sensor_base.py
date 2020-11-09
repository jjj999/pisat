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

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.SensorController
"""

from typing import Generic, Set, Tuple, Optional, Type, TypeVar

from pisat.base.component import Component
from pisat.base.component_group import ComponentGroup
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
    

class SensorGroup(SensorBase, ComponentGroup, Generic[LinkedModel]):
    """A container of objects of SensorBase. 
    
    SensorGroup is a component group and also a sensor, 
    in other words, this class is like a sensor as a component group. 
    A sensor group can make users access to internal sensors 
    as a cluster of them, which means some methods of SensorGroup 
    behave like ones of SensorBase are executed all at once.
    """

    def __init__(self, 
                 model: Type[LinkedModel], 
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            *sensors : Tuple[SensorInterface, ...]
                Sensors to be included inside.
            name : Optional[str], optional
                Name of the component, by default None
        """
        ComponentGroup.__init__(self, name=name)
        
        if not issubclass(model, LinkedDataModelBase):
            raise TypeError(
                f"'model' must be a subclass of {LinkedDataModelBase.__name__}."
            )
        
        self._sensors: Set[SensorBase] = set()
        self._model = model
        
    def __len__(self):
        return len(self._sensors)

    def extend(self, group):
        """Append internal sensors of given sensor group.

        Parameters
        ----------
            group : SensorGroup
                Sensor group which has sensors inside.
        """
        self.add(*tuple(group._sensors))

    def add(self, *sensors: Tuple[SensorBase, ...]):
        """Append sensors inside.
        
        Parameters
        ----------
            *sensors : Tuple[SensorBase, ...]
                Sensors to be included inside.

        Raises
        ------
            NotImplementedError
                Raised if given sensors are not instances of SensorBase.
        """
        ComponentGroup.append(self, *sensors)

        for sensor in sensors:
            if not isinstance(sensor, SensorBase):
                raise NotImplementedError(
                    "Components of 'sensors' must be SensorBase."
                )

            self._sensors.add(sensor)

    def remove(self, sensor: SensorBase):
        """Remove given sensor from the group.

        Parameters
        ----------
            sensor : SensorBase
                Sensor to be removed.

        Raises
        ------
            ValueError
                Raised if the given sensor is not included in the sensor group.
        """
        try:
            self._sensors.remove(sensor)
        except KeyError:
            raise ValueError("The SensorGroup doesn't have the sensor.")

    def read(self) -> LinkedModel:
        """Read data of sensor as a dictionary.

        Returns
        -------
            LinkedDataModelBase
                A data model which has retrieved data from the sensor.
        """
        model = self._model(self.name)
        data = [sensor.read() for sensor in self._sensors]
        model.sync(*data)
        return model
        