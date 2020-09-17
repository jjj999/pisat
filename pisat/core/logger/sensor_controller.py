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

from typing import Dict, List, Tuple, Union, Optional

from pisat.config.type import Logable
from pisat.base.component_group import ComponentGroup
from pisat.sensor.sensor_base import SensorBase, SensorGroup
from pisat.adapter.adapter_base import AdapterBase, AdapterGroup


class SensorController(ComponentGroup):
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
                 sgroup: SensorGroup,
                 agroup: Optional[AdapterGroup] = None,
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

        self._sgroup: SensorGroup = sgroup
        self._agroup: AdapterGroup = agroup
        
        if agroup is None:
            self._agroup = AdapterGroup()
            
        super().append(self._sgroup, self._agroup)

    @property
    def dnames(self):
        return self._sgroup.dnames + self._agroup.dnames

    def append(self, *args) -> None:
        """Append and set Sensors or Adapters
        
        Parameters
        ----------
            args : Tuple[Union[SensorBase, AdapterBase], ...]
                Any number of Sensors or Adapters

        Raises
        ------
            TypeError
                Raised if not Sensor or Adapter class is given.
        """
        super().append(*args)
        
        sensors = []
        adapters = []
        for arg in args:
            if isinstance(arg, SensorBase):
                sensors.append(arg)
            elif isinstance(arg, AdapterBase):
                adapters.append(arg)
            else:
                raise TypeError(
                    "Appendable objects must be SensorBase or AdapterBase."
                )

        self._sgroup.append(*tuple(sensors))
        self._agroup.append(*tuple(adapters))
        
    def reset(self, 
              obj: Union[SensorBase, AdapterBase], 
              dname: Optional[str] = None) -> None:
        """Reset readability setting about given object.
        
        The methods resets readability setting changed by other operations in the past.
        If 'dname' is None, then all data of the given object is to be reset their 
        readabilities.

        Parameters
        ----------
            obj : Union[SensorBase, AdapterBase]
                SensorBase or AdapterBase whose data readability is to be reset.
            dname : Optional[str], optional
                Data name to be reset, by default None

        Raises
        ------
            TypeError
                Raised if not Sensor or Adapter class is given.
                
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        
        if isinstance(obj, SensorBase):
            self._sgroup.reset(obj, dname=dname)
        elif isinstance(obj, AdapterBase):
            self._agroup.reset(obj, dname=dname)
        else:
            raise TypeError(
                "'obj' should be an implemantion of SensorBase and AdapterBase"
            )
            
    def reset_all(self, sensor: bool = True, adapter: bool = True):
        """Reset all readability setting.

        Parameters
        ----------
            sensor : bool, optional
                If reset readabilities of internal sensors, by default True
            adapter : bool, optional
                If reset readabilities of internal adapters, by default True
        
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if sensor:
            self._sgroup.reset_all()
        if adapter:
            self._agroup.reset_all()
            
    def recollect(self, dname: str, sensor: bool = True, adapter: bool = True):
        """Reset the readability of given data name.

        Parameters
        ----------
            dname : str
                Data name whose readability is to be reset.
            sensor : bool, optional
                If reset readabilities of internal sensors, by default True
            adapter : bool, optional
                If reset readabilities of internal adapters, by default True
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if sensor:
            self._sgroup.recollect(dname)
        if adapter:
            self._agroup.recollect(dname)

    def concentrate(self, dname: str, obj: Union[SensorBase, AdapterBase]) -> None:
        """Limit readability of given data to given object.
        
        The method changes readability setting of the given data as only data 
        emitted from the given 'obj' is adopted as the data. This method only 
        makes sense when several object can read the given data. 

        Parameters
        ----------
            dname : str
                Data name.
            obj : Union[SensorBase, AdapterBase]
                Sensor or Adapter to be concentrated.

        Raises
        ------
            TypeError
                Raised if not Sensor or Adapter class is given.
                
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """

        if isinstance(obj, SensorBase):
            self._sgroup.concentrate(dname, obj)
            if dname in self._agroup.dnames:
                self._agroup.ignore(dname)
        elif isinstance(obj, AdapterBase):
            self._agroup.concentrate(dname, obj)
            if dname in self._sgroup.dnames:
                self._sgroup.ignore(dname)
        else:
            raise TypeError(
                "'obj' should be an implemantion of SensorBase and AdapterBase"
            )

    def ignore(self, dname: str, obj: Union[None, SensorBase, AdapterBase] = None) -> None:
        """Change readability of given data to be ignored.
        
        The method changes readability setting of the given data as ignored 
        when 'read' method is called. if 'obj' is None, the given data completely 
        ignored, but if 'obj' is given, then the given 'obj' is ignored as for 
        reading the given data.

        Parameters
        ----------
            dname : str
                Data name.
            obj : Union[None, SensorBase, AdapterBase], optional
                Sensor or Adapter to be ignored, by default None.

        Raises
        ------
            ValueError
                Raised if the given object doen't have the given data name.
            TypeError
                Raised if not Sensor or Adapter class is given.

        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """

        if obj is None:
            nothas = True
            if self._sgroup.has_dname(dname):
                self._sgroup.ignore(dname)
                nothas = False
            if self._agroup.has_dname(dname):
                self._agroup.ignore(dname)
                nothas = False

            if nothas:
                raise ValueError(
                    "The sensorcontraller doesn't have the dname.")

        elif isinstance(obj, SensorBase):
            self._sgroup.ignore(dname, obj)
        elif isinstance(obj, AdapterBase):
            self._agroup.ignore(dname, obj)
        else:
            raise TypeError(
                "'obj' must be SensorBase or AdapterBase or None."
            )

    def remove(self, obj: Union[SensorBase, AdapterBase]) -> None:
        """Remove given object from readabilities of all data.
        
        The method changes readability settings of all data as 'obj' is ignored 
        when 'read' method is called. This means the given object is to be completely 
        removed and the method of 'obj' is never called after executing this method. 
        If you want to recover the 'obj', you can call 'reset' method.

        Parameters
        ----------
            obj : Union[SensorBase, AdapterBase]
                Sensor or Adapter to be removed

        Raises
        ------
            TypeError
                Raised if not Sensor or Adapter class is given.

        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if isinstance(obj, SensorBase):
            self._sgroup.remove(obj)
        elif isinstance(obj, AdapterBase):
            self._agroup.remove(obj)
        else:
            raise TypeError(
                "'obj' should be an implemantion of SensorBase and AdapterBase"
            )
            
    def delete(self, obj: Union[SensorBase, AdapterBase]) -> None:
        """Remove given object completely.
        
        This method removes the given object from internal sensors set 
        if the object is a sensor, else from internal adapters set. 
        Thus, Users cannot reset the readability of the object after 
        calling this method.

        Parameters
        ----------
            obj : Union[SensorBase, AdapterBase]
                Sensor or Adapter to be removed.

        Raises
        ------
            TypeError
                Raised if not Sensor or Adapter class is given.
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if isinstance(obj, SensorBase):
            self._sgroup.delete(obj)
        elif isinstance(obj, AdapterBase):
            self._agroup.delete(obj)
        else:
            raise TypeError(
                "'obj' should be an implemantion of SensorBase and AdapterBase"
            )
            
    def get_sensor(self, dname: str) -> List[SensorBase]:
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
        return self._sgroup.get_sensor(dname)
        
    def get_adapter(self, dname: str) -> List[AdapterBase]:
        """Search Adapter objects from data name.

        Parameters
        ----------
            dname : str
                Data name to search.

        Returns
        -------
            List[AdapterBase]
                Searched Adapter objects.
            
        See Also
        --------
            pisat.adapter.AdapterGroup : AdapterGroup.get_adapter is used inside.
        """
        return self._agroup.get_adapter(dname)

    def search(self, *dnames) -> Tuple[str]:
        """Search sensor data required to calculate with registered adapters
        
        Patameters
        ----------
            dnames : Tuple[str, ...]
                Data names to be required for internal adapters.

        Returns
        -------
            Tuple[str]
                Serched result.
        """
        searched = []
        for dname in dnames:
            # search from set of sensors
            if dname in self._sgroup.dnames:
                searched.append(dname)

            # search from set of adapters
            elif dname in self._agroup.dnames:
                for adapter in self._agroup._DtoA[dname]:
                    searched.extend(adapter.requires[dname])

        return tuple(searched)

    def read(self, *dnames) -> Dict[str, Logable]:
        """Execute the transaction of reading Sensors' data and calculating Adapters' data. 
        
        Parameters
        ----------
            dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
        Dict[str, Logable]
            Data logged.
        """
        res = {}

        if not len(dnames):
            sensor_vals = self._sgroup.read()
            res.update(sensor_vals)
            res.update(self._agroup.supply(sensor_vals))
            return res

        else:
            sensor_vals = self._sgroup.read(*self.search(*dnames))
            res.update(sensor_vals)
            res.update(self._agroup.supply(sensor_vals))
            return res
