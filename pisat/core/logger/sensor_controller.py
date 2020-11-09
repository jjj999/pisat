#! python3

"""

pisat.core.logger.sensor_controller
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A controller of multiple Sensor and Adapter classes.
This class integrates Sensor and Adapter classes and 
control as two types of classes make cooperation. 
This means that SensorController operates some kind of 
transaction about retrieving multiple data with 
sets of Sensors and Adapters. 

This class is a ComponentGroup.

In most cases, a user should use the class to be wrapped 
in DataLogger class beacause SensorController have no 
inner container for holding data logged like LogQueue.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.DataLogger
pisat.core.logger.LogQueue
"""

from typing import Dict, Generic, List, Set, Tuple, Type, TypeVar, Union, Optional

from pisat.base.component_group import ComponentGroup
from pisat.model.linked_datamodel import LinkedDataModelBase
from pisat.sensor.sensor_base import SensorBase


LinkedModel = TypeVar("LinkedModel", LinkedDataModelBase)


class SensorController(ComponentGroup, Generic[LinkedModel]):
    """Controller of SensorGruop and AdapterGroup.
    
    A controller of multiple Sensor and Adapter classes.
    This class integrates Sensor and Adapter classes and 
    control as two types of classes make cooperation. 
    This means that SensorController operates some kind of 
    transaction about retrieving multiple data with 
    sets of Sensors and Adapters. 

    This class is a ComponentGroup.

    In most cases, a user should use the class to be wrapped 
    in DataLogger class beacause SensorController have no 
    inner container for holding data logged like LogQueue.
    
    See Also
    --------
        pisat.core.logger.DataLogger : Wrapper class of this class.
        pisat.core.logger.LogQueue : Container class of logged data.
    """

    def __init__(self,
                 modelclass: Type[LinkedModel],
                 name: Optional[str] = None):
        """
        Parameters
        ----------
            sgroup : SensorGroup
                SensorGroup of Sensor objects.
            agroup : Optional[AdapterGroup], optional
                AdapterGroup of Adapter objects, by default None
            name : Optional[str], optional
                name of this Component, by default None
        """
        super().__init__(name=name)

        if not issubclass(modelclass, LinkedDataModelBase):
            raise TypeError(
                f"'modelclass' must be a subclass of {LinkedDataModelBase.__name__}"
            )
            
        self._sensors: Set[SensorBase] = set()
        self._modelclass = modelclass

    def __len__(self):
        return len(self._sensors)

    def append(self, *sensors: SensorBase):
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
        super().append(self, *sensors)

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
        model = self._modelclass(self.name)
        data = [sensor.read() for sensor in self._sensors]
        model.sync(*data)
        return model

    def get_sensors(self) -> Dict[str, SensorBase]:
        """Search Sensor objects from data name.

        Parameters
        ----------
            dname : str
                Data name to search.

        Returns
        -------
            List[SensorBase]
                Searched Sensor objects.
            
        See Also
        --------
            pisat.sensor.sensor.SensorGroup : SensorGroup.get_sensor is used inside.
        """
        return {sensor.name: sensor for sensor in self._sensors}
