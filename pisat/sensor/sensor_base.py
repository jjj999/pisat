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

from pisat.base.component_group import ComponentGroup
from typing import Callable, List, Dict, Set, Tuple, Optional

from pisat.config.type import Logable
from pisat.base.component import Component
from pisat.handler.handler_base import HandlerBase


class HandlerMismatchError(Exception):
    """Raised if a given handler doesn't match required one."""
    pass


class HandlerNotSetError(Exception):
    """Raised if a hanler is not set when the handler is required."""
    pass


class SensorInterface(Component):
    """Interface which a senser should have. 
    
    The sensor system consists of objects of SensorBase 
    and SensorGroup, and SensorInterface forms their backbone. 
    SensorInterface is a Component.
    """

    @property
    def dnames(self) -> Tuple[str]:
        pass

    def has_dname(self, dname: str) -> bool:
        """Return if the sensor has given data names of its outputs.

        Parameters
        ----------
            dname : str
                Data name to be judged.

        Returns
        -------
            bool
                If the sensor has given data names of its outputs.
        """
        return True if dname in self.dnames else False

    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        """Read data of sensor as a list.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            List[Logable]
                Retreived data.
        """
        pass

    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Read data of sensor as a dictionary.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            Dict[str, Logable]
                A dictionary whose keys are data names and values are 
                retrieved data.
        """
        pass

    def make_readf(self, *dnames: Tuple[str, ...]) -> Callable:
        """Make a closure of the 'readf' method.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            Callable
                Closure of the 'readf' method.
        """
        def readf() -> List[Logable]:
            return self.readf(*dnames)
        return readf

    def make_read(self, *dnames: Tuple[str, ...]) -> Callable:
        """Make a closure of the 'read' method.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            Callable
                Closure of the 'read' method.
        """
        def read() -> Dict[str, Logable]:
            return self.read(*dnames)
        return read


class SensorGroup(SensorInterface, ComponentGroup):
    """A container of objects of SensorBase. 
    
    SensorGroup is a ComponentGroup and also a SensorInterface, 
    in other words, this class is like a sensor as a component group. 
    A sensor group can make users access to internal sensors 
    as a cluster of them, which means some methods of SensorGroup 
    behave like ones of SensorBase are executed all at once.
    """

    def __init__(self, 
                 *sensors: Tuple[SensorInterface, ...], 
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
        
        self._sensors: Set[SensorInterface] = set()
        self._closures_f: Tuple[Callable] = ()
        self._closures: Tuple[Callable] = ()
        self._DtoS: Dict[str, List[SensorInterface]] = {}
        self._StoD: Dict[SensorInterface, List[str]] = {}

        if len(sensors):
            self.append(*sensors)

    def __add__(self, sensor):
        self.append(sensor)
        return self

    def __iadd__(self, sensor):
        self.append(sensor)

    def extend(self, group):
        """Append internal sensors of given sensor group.

        Parameters
        ----------
            group : SensorGroup
                Sensor group which has sensors inside.
        """
        self.append(*tuple(group._StoD.keys()))

    def append(self, *sensors: Tuple[SensorInterface, ...]):
        """Append sensors inside.
        
        Parameters
        ----------
            *sensors : Tuple[SensorInterface, ...]
                Sensors to be included inside.

        Raises
        ------
            NotImplementedError
                Raised if given sensors are not instances of SensorInterface.
        """
        ComponentGroup.append(self, *sensors)

        for sensor in sensors:
            # check if each given sensor is a Sensor component
            if not isinstance(sensor, SensorInterface):
                raise NotImplementedError(
                    "A specified sensor object has not implemented the SensorInterface."
                )
                
            # NOTE
            #   1.  StoD will overwrite its dnames if a sensor already set up is given.
            #   2.  If user calls concentrate(), ignore() or remove(), and DtoS and
            #       StoD is updated, this method will work to reset the DtoS and
            #       StoD regarding given sensor.

            # update sensors set
            self._sensors.add(sensor)

            # update data2sensor map
            for dname in sensor.dnames:
                if self._DtoS.get(dname) is None:
                    self._DtoS[dname] = [sensor]
                else:
                    # avoid duplication
                    if sensor not in self._DtoS[dname]:
                        self._DtoS[dname].append(sensor)

            # update sensor2data map
            self._StoD[sensor] = list(sensor.dnames)

        self._configure_closures()

    # FIXME in more efficient way
    def _configure_closures(self):
        """Make closures depending on the current readability setting.
        """
        res_f = []
        res = []
        for sensor, reqs in self._StoD.items():
            # All data is required
            if len(sensor.dnames) == len(reqs):
                res_f.append(sensor.make_readf())
                res.append(sensor.make_read())
            # Ignore reading if required dnames are nothing
            elif not len(reqs):
                pass
            # When needed to handle a readability
            else:
                args = tuple(reqs)
                res_f.append(sensor.make_readf(*args))
                res.append(sensor.make_read(*args))

        self._closures_f = tuple(res_f)
        self._closures = tuple(res)
        
    def reset(self, 
              sensor: SensorInterface, 
              dname: Optional[str] = None):
        """Reset readability setting about given object.
        
        The methods resets readability setting changed by other operations in the past.
        If 'dname' is None, then all data of the given sensor is to be reset their 
        readabilities.

        Parameters
        ----------
            sensor : SensorInterface
                A sensor whose data readability is to be reset.
            dname : Optional[str], optional
                Data name to be reset, by default None

        Raises
        ------
            TypeError
                Raised if the given sensor is not an SensorInterface.
            ValueError
                Raised if the given sensor doesn't have the given dname.
            
        Notes
        -----
            'Readability' means whether a kind of data of sensor can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular sensors.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if dname is None:
            self.append(sensor)
        else:
            if dname in sensor.dnames:
                # update DtoS
                if self._DtoS.get(dname) is None:
                    self._DtoS[dname] = [sensor]
                else:
                    # avoid duplication
                    if sensor not in self._DtoS[dname]:
                        self._DtoS[dname].append(sensor)
                        
                # update StoD
                dnames_sensor = self._StoD.get(sensor)
                if dnames_sensor is None:
                    self._StoD[sensor] = [dname]
                elif dname is not dnames_sensor:
                    self._StoD[sensor].append(dname)
                    
            else:
                raise ValueError(
                    "'dname' must be included dnames of 'sensor'."
                )
                
    def reset_all(self):
        """Reset all readability setting.
        
        See Also
        --------
            SensorGroup.append : This method is used inside.
        """
        self.append(*tuple(self._sensors))
        
    def recollect(self, dname: str):
        """Reset the readability of given data name.

        Parameters
        ----------
            dname : str
                Data name whose readability is to be reset.
            
        See Also
        --------
            SensorGroup.reset : This method is used inside.
        """
        sensors = {sensor for sensor in self._sensors if dname in sensor.dnames}
        for sensor in sensors:
            self.reset(sensor, dname=dname)

    def concentrate(self, dname: str, sensor: SensorInterface):
        """Limit readability of given data to given object.
        
        The method changes readability setting of the given data as only data 
        emitted from the given 'sensor' is adopted as the data. This method only 
        makes sense when several object can read the given data. 

        Parameters
        ----------
            dname : str
                Data name.
            sensor : SensorInterface
                Sensor to be ignored, by default None.

        Raises
        ------
            TypeError
                Raised if the given sensor is not SensorInterface.
            ValueError
                Raised if the given sensor is not included in the sensor group.
            ValueError
                Raised if the given name is not included of the data names of 
                internal sensors.
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular sensors.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        sensors = self._DtoS.get(dname)
        if sensors is None:
            raise ValueError("The SensorGroup doesn't have the dname.")

        if sensor in sensors:
            # remove from StoD except the given sensor
            for s in sensors:
                if s is sensor:
                    continue
                else:
                    self._StoD[s].remove(dname)

            # remove from DtoS and rebuild
            self._DtoS[dname].clear()
            self._DtoS[dname].append(sensor)

            self._configure_closures()
        else:
            raise ValueError(
                "The SensorGroup doesn't have the sensor which has the dname."
            )

    def ignore(self,
               dname: str,
               sensor: SensorInterface = None):
        """Change readability of given data to be ignored.
        
        The method changes readability setting of the given data as ignored 
        when 'read' or 'readf' method is called. if 'sensor' is None, the given 
        data completely ignored, but if 'sensor' is given, then the given 'sensor' 
        is ignored as for reading the given data.

        Parameters
        ----------
            dname : str
                Data name.
            sensor : SensorInterface, optional
                sensor to be ignored, by default None

        Raises
        ------
            TypeError
                Raised if the given sensor is not SensorInterface.
            ValueError
                Raised if the given sensor is not included in the sensor group.
            ValueError
                Raised if the given name is not included of the data names of 
                internal sensors.
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular sensors.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        sensors = self._DtoS.get(dname)
        if sensors is None:
            raise ValueError("The SensorGroup doesn't have the dname.")

        if sensor is None:
            for s in sensors:
                self._StoD[s].remove(dname)
            self._DtoS.pop(dname)
        elif sensor in sensors:
            self._DtoS[dname].remove(sensor)
            self._StoD[sensor].remove(dname)
        else:
            raise ValueError(
                "The SensorGroup doesn't have the sensor which has the dname."
            )

        self._configure_closures()

    def remove(self, sensor: SensorInterface):
        """Remove given sensor from readabilities of all data.
        
        The method changes readability settings of all data as 'sensor' is ignored 
        when 'read' or 'readf' method is called. This means the given object is to 
        be completely removed and the method of 'sensor' is never called after 
        executing this method. If you want to recover the 'sensor', you can call 
        the 'reset' method.

        Parameters
        ----------
            sensor : SensorInterface
                Sensor to be removed.

        Raises
        ------
            ValueError
                Raised if the given sensor is not included in the sensor group.
            
        Notes
        -----
            'Readability' means whether a kind of data of Sensor can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular sensors.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        try:
            for dname in sensor.dnames:
                self._DtoS[dname].remove(sensor)
            self._StoD.pop(sensor)

            self._configure_closures()
        except ValueError:
            raise ValueError("The SensorGroup doesn't have the sensor.")
        
    def delete(self, sensor: SensorInterface):
        """Remove given sensor completely.
        
        This method removes the given sensor from internal sensors set. 
        Thus, Users cannot reset the readability of the sensor after 
        calling this method.

        Parameters
        ----------
            sensor : SensorInterface
                Sensor to be removed.
            
        See Also
        --------
            SensorGroup.remove : This method is used inside.
        """
        self.remove(sensor)
        self._sensors.discard(sensor)

    def get_sensor(self, dname: str) -> List[SensorInterface]:
        """Retrive sensors from given data name.

        Parameters
        ----------
            dname : str
                Data name to be searched.

        Returns
        -------
            List[SensorInterface]
                Result of searching.
        """
        collected = self._DtoS.get(dname)
        if collected is None:
            return []

        return collected

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   SensorInterface implementions                                           #
    #                                                                           #
    #   Notes                                                                   #
    #   1.  You might think the readf and read method should be implemented     #
    #       using list and dict comprehension, but as the result of some        #
    #       speed tests, we know not using the comprehensions is better         #
    #       as for speed in this case. Therefore, it doesn't have to fix        #
    #       the implementations below.                                          #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

    @property
    def dnames(self) -> Tuple[str]:
        return tuple(self._DtoS.keys())

    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        """Read data of sensor as a list.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            List[Logable]
                Retreived data.
        """
        result = []
        if len(dnames) == 0:
            for closure in self._closures_f:
                result.extend(closure())
        else:
            for dname in dnames:
                for sensor in self.get_sensor(dname=dname):
                    result.extend(sensor.readf(dname))

        return result

    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Read data of sensor as a dictionary.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            Dict[str, Logable]
                A dictionary whose keys are data names and values are 
                retrieved data.
        """
        result = {}
        if len(dnames) == 0:
            for closure in self._closures:
                result.update(closure())
        else:
            for dname in dnames:
                for sensor in self.get_sensor(dname=dname):
                    result.update(sensor.read(dname))

        return result

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   Additional methods                                                      #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

    def readf_from(self, *names: Tuple[str, ...]) -> List[Logable]:
        """Read data from sensors which given names match as a list.
        
        Parameters
        ----------
            *names : Tuple[str, ...]
                Component's names of sensors.

        Returns
        -------
            List[Logable]
                Result of retrieved data.
        """
        result = []
        if len(names) == 0:
            for closure in self._closures_f:
                result.extend(closure())
        else:
            for name in names:
                for sensor in self.get_component(name):
                    if sensor is not None:
                        result.extend(sensor.readf())

        return result

    def read_from(self, *names: Tuple[str, ...]) -> Dict[str, Logable]:
        """Read data from sensors which given names match as a dictionary.
        
        Parameters
        ----------
            *names : Tuple[str, ...]
                Component's names of sensors.

        Returns
        -------
            Dict[str, Logable]
                Result of retrieved data.
        """
        result = {}
        if len(names) == 0:
            for closure in self._closures:
                result.update(closure())
        else:
            for name in names:
                for sensor in self.get_component(name):
                    if sensor is not None:
                        result.update(sensor.read())

        return result


class SensorBase(SensorInterface):
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
    must override some attributes and methods, at least, DATA_NAMES, 
    DEFAULT_VALUES, readf and read. More information, see the references of 
    attributes and methods.
    
    Attributes
    ----------
        DATA_NAMES : Tuple[str]
            Data namees the sensor outputs.
        DEFAULT_VALUES : Dict[str, Logable]
            Default output values.
            
    Notes
    -----
        DATA_NAMES must be same as keys of output of the 'read' method. 
        
        DEFAULT_VALUES has same interface of the 'read' method. This 
        attribute are emitted as a return values in the debug mode. 
        The debug mode can be used if the argument 'debug' is set as True 
        in the constructor. 
    """

    DATA_NAMES: Tuple[str] = ()
    DEFAULT_VALUES: Dict[str, Logable] = {}

    def __init__(self, 
                 handler: Optional[HandlerBase] = None, 
                 debug: bool = False,
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            handler : Optional[HandlerBase], optional
                Handler object if required, by default None
            debug : bool, optional
                If the debug mode is valid, by default False
            name : Optional[str], optional
                Name of the component, by default None
        """
        super().__init__(name=name)
        
        #   NOTE
        #       SensorBase does not force to use a handler
        #       in its subclasses. If you want not to use
        #       any handler, you should override __init__.
        
        self._handler: Optional[HandlerBase] = handler
        self._debug: bool = debug
            
    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, sensor):
        return SensorGroup(self, sensor)

    def __iadd__(self, sensor):
        return self.__add__(self, sensor)

    @property
    def dnames(self) -> Tuple[str]:
        return self.DATA_NAMES

    def readf(self, *dnames: Tuple[str, ...]) -> List[Logable]:
        """Read data of sensor as a list.
        
        This method is an abstract method. Implementation of the 
        method must return elements of data in order of the given 'dnames'. 
        If any 'dnames' are not given, the implementation must return 
        all readable data in order of 'DATA_NAMES'
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            List[Logable]
                Retreived data.
        """
        if self._debug:
            if len(dnames) == 0:
                return [val for val in self.DEFAULT_VALUES.values()]
            else:
                return [self.DEFAULT_VALUES[dname] for dname in dnames]
        else:
            pass

    def read(self, *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Read data of sensor as a dictionary.
        
        This method is an abstract method. Implementation of the method 
        must return all readable data if any 'dnames' are given. 
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be read.

        Returns
        -------
            Dict[str, Logable]
                A dictionary whose keys are data names and values are 
                retrieved data.
        """
        if self._debug:
            if len(dnames) == 0:
                return self.DEFAULT_VALUES
            else:
                return {dname: self.DEFAULT_VALUES[dname] for dname in dnames}
        else:
            pass
