#! python3

"""

pisat.core.logger.logger
~~~~~~~~~~~~~~~~~~~~~~~~
A top level class of data logging. This class integrates 
SensorController and LogQueue inside, and executes 
some transactions about data logging. This class also 
can be an entry-point of data logging for most users, for
example users can retrieve logged data in the way of thread-safe,
control data to read, and so on.

This class is a ComponentGroup.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.SensorController
pisat.core.logger.LogQueue
pisat.core.logger.RefQueue
"""

from typing import Deque, Dict, List, Optional, Union

from pisat.config.type import Logable
from pisat.base.component_group import ComponentGroup
from pisat.adapter.adapter_base import AdapterBase
from pisat.sensor.sensor_base import SensorBase
from pisat.core.logger.logque import LogQueue
from pisat.core.logger.refque import RefQueue
from pisat.core.logger.sensor_controller import SensorController


class DataLogger(ComponentGroup):
    """Basic data logger class.
    
    A top level class of data logging. This class integrates 
    SensorController and LogQueue inside, and executes 
    some transactions about data logging. This class also 
    can be an entry-point of data logging for most users, for
    example users can retrieve logged data in the way of thread-safe,
    control data to read, and so on.
    
    This class is a ComponentGroup.
    
    See Also
    --------
        pisat.core.logger.SensorController : 
            This class is used inside about reading data.
        pisat.core.logger.LogQueue : Base class of DictLogQueue.
        pisat.core.logger.RefQueue : This class is used inside for retrieving logged data.
    """

    def __init__(self, 
                 con: SensorController,
                 que: LogQueue,
                 reflen: int = 100,
                 name: Optional[str] = None):
        """
        Parameters
        ----------
            con : SensorController
                A SensorController object readable data.
            que : LogQueue
                A LogQueue object as a container.
            reflen : int, optional
                size of inner RefQueue object, by default 100
            name : Optional[str], optional
                name of this Component, by default None
        """
        super().__init__(name=name)
        
        self._con: SensorController = con
        self._que: LogQueue = que
        self._refque: RefQueue = RefQueue(maxlen=reflen)
        
        super().append(con, que, self._refque)
        
    @property
    def dnames(self):
        return self._con.dnames
    
    @property
    def refqueue(self):
        return self._refque
    
    def append(self, *args) -> None:
        """Append and set Sensors or Adapters into SensorController
        
        Parameters
        ----------
            args : Tuple[Union[SensorBase, AdapterBase], ...]
                Any number of Sensors or Adapters
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.append is used inside.
        """
        super().append(*args)
        self._con.append(*args)
        
    def reset(self, obj: Union[SensorBase, AdapterBase], dname: Optional[str] = None) -> None:
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
                
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
            This feature of DataLogger derived from SensorController, 
            originally SensorGroup and AdapterGroup.
    
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.reset is used inside.
        """
        self._con.reset(obj, dname)
        
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
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.reset_all is used inside.
        """
        self._con.reset_all(sensor=sensor, adapter=adapter)
        
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
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.recollect is used inside.
        """
        self._con.recollect(dname, sensor=sensor, adapter=adapter)
        
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
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
            This feature of DataLogger derived from SensorController, 
            originally SensorGroup and AdapterGroup.
        
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.concentrate is used inside.
        """
        self._con.concentrate(dname, obj)
        
    def ignore(self, dname: str, obj: Union[None, SensorBase, AdapterBase] = None) -> None:
        """Change readability of given data to be ignored.
        
        The method changes readability setting of the given data as ignored 
        when 'read' method is called. if 'obj' is None, the given data completely 
        ignored, but if 'obj' is given, then the given 'obj' is ignored as for 
        reading the given data.

        Parameters
        ----------
            dname : str
                Data Name.
            obj : Union[None, SensorBase, AdapterBase], optional
                Sensor or Adapter to be ignored, by default None
                
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
            This feature of DataLogger derived from SensorController, 
            originally SensorGroup and AdapterGroup.
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.ignore is used inside.
        """
        self._con.ignore(dname, obj)
        
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
                
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
            This feature of DataLogger derived from SensorController, 
            originally SensorGroup and AdapterGroup.
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.remove is used inside.
        """
        self._con.remove(obj)
        
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
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor or Adapter can be 
            read. The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.delete is used inside.
        """
        self._con.delete(obj)
        
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
            pisat.core.logger.SensorController : SensorController.get_sensor is used inside.
        """
        return self._con.get_sensor(dname)
    
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
            pisat.core.logger.SensorController : SensorController.get_adapter is used inside.
        """
        return self._con.get_adapter(dname)
                
    def read(self, *dnames) -> Dict[str, Logable]:
        """Execute transaction for reading, caching and saving data log.

        Returns
        -------
            Dict[str, Logable]
                logged data.
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.read is used inside.
            pisat.core.logger.LogQueue : LogQueue.append is used inside.
            pisat.core.logger.RefQueue : RefQueue.append is used inside.
        """
        data = self._con.read(*dnames)
        self._que.append(data)
        self._refque.append(data)
        return data
    
    def close(self):
        """Execute post-process of logging.

        Notes
        -----
            If the method is not called and a program finishes, 
            then some cached data may not be saved into a file.
            
        See Also
        --------
            pisat.core.logger.LogQueue : LogQueue.close is used inside.
        """
        self._que.close()
    
    def __len__(self):
        return len(self._que)
        
    def __getitem__(self, key):
        return self._que[key]
    
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
        