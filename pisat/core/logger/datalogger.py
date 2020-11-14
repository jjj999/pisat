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

[info]
pisat.core.logger.SensorController
pisat.core.logger.LogQueue
pisat.core.logger.RefQueue
"""

from typing import Dict, Generic, Optional, Type, TypeVar

from pisat.base.component_group import ComponentGroup
from pisat.sensor.sensor_base import SensorBase
from pisat.core.logger.logque import LogQueue
from pisat.core.logger.refque import RefQueue
from pisat.core.logger.sensor_controller import SensorController
from pisat.model.linked_datamodel import LinkedDataModelBase


LinkedModel = TypeVar("LinkedModel")


class DataLogger(ComponentGroup, Generic[LinkedModel]):
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
                 modelclass: Optional[Type[LinkedModel]] = None,
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
        
        self._con = con
        self._que = que
        self._refque = RefQueue(maxlen=reflen)
        self._modelclass = None
        
        if modelclass is not None:
            self.set_model(modelclass)
        
        super().append(con, que, self._refque)
    
    @property
    def refqueue(self):
        return self._refque
    
    def append(self, *sensors) -> None:
        """Append and set Sensors or Adapters into SensorController
        
        Parameters
        ----------
            args : Tuple[Union[SensorBase, AdapterBase], ...]
                Any number of Sensors or Adapters
            
        See Also
        --------
            pisat.core.logger.SensorController : SensorController.append is used inside.
        """
        super().append(*sensors)
        self._con.append(*sensors)
        
    def remove(self, sensor: SensorBase) -> None:
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
        self._con.remove(sensor)
        
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
            pisat.core.logger.SensorController : SensorController.get_sensor is used inside.
        """
        return self._con.get_sensors()
    
    def set_model(self, modelclass: Type[LinkedModel]) -> None:
        if not issubclass(modelclass, LinkedDataModelBase):
            raise TypeError(
                "'modelclass' must be a subclass of LinkedDataModelBase."
            )
        self._modelclass = modelclass
                
    def read(self):
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
        model = self._con.read()
        self._que.append(model)
        
        if self._modelclass is None:
            self._refque.append(model)
            return model
        else:
            linked = self._modelclass(self.name)
            linked.sync(model)
            self._refque.append(linked)
            return linked
    
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
        