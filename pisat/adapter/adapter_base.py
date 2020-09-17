#! python3

"""

pisat.adapter.adapter_base
~~~~~~~~~~~~~~~~~~~~~~~~~~
The module which defines what an adapter is.
The classes in the module all define adapter system. 

AdapterInterface represents the interface which an adapter 
should have. The adapter system consists of objects of AdapterBase 
and AdapterGroup, and AdapterInterface forms their backbone. 
AdapterInterface is a Component.

AdapterGroup represents a container of objects of AdapterBase. 
AdapterGroup is a ComponentGroup and also a AdapterInterface, 
in other words, this class is like an adapter as component group. 
An adapter group can make users access to internal adapters 
as a cluster of them, which means some methods of AdapterGroup 
behave like ones of AdapterBase are executed all at once. 

AdapterBase represents an element of the adapter set. 
Diversity of the adapter system is one of the classes of AdapterBase. 
In the pisat system (or the adapter system) an adapter means 
an object of the AdapterBase. The AdapterBase should be inheritanced 
in most cases. An adapter represents a calculator which recieve some 
required values and output the result calculated from the input values. 
In almost all cases, adapters are abstracted by logging classes, 
especially SensorController. The logging classes combine sensors and 
adapters inside, and the output data from the sensors are given to 
the adapters, finally users can get the result of adapters' output and 
sensors'. 

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pisat.core.logger.SensorController
"""

from typing import Callable, Dict, List, Optional, Set, Tuple

from pisat.config.type import Logable
from pisat.base.component import Component
from pisat.base.component_group import ComponentGroup


class AdapterInterface(Component):
    """Interface which an adapter should have.
    
    The adapter system consists of objects of AdapterBase 
    and AdapterGroup, and AdapterInterface forms their backbone. 
    AdapterInterface is a Component.
    """

    @property
    def dnames(self) -> Tuple[str]:
        pass
    
    @property
    def requires(self) -> Dict[str, Tuple[str]]:
        pass
    
    def has_dname(self, dname: str) -> bool:
        """Return if the adapter has given data names of its outputs.

        Parameters
        ----------
            dname : str
                Data name to be judged.

        Returns
        -------
            bool
                If the adapter has given data names of its outputs.
        """
        return True if dname in self.dnames else False

    def supply(self, 
               data: Dict[str, Logable], 
               *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Calculate other data from given data.
        
        This method is the main method of AdapterInterface and an 
        abstract method. 

        Parameters
        ----------
            data : Dict[str, Logable]
                Data for calculation.
            *dnames : Tuple[str, ...]
                Data names to be calculated.

        Returns
        -------
            Dict[str, Logable]
                Data calculated.
        """
        pass

    def make_supply(self, *dnames: Tuple[str, ...]) -> Callable:
        """Make a closure of the 'supply' method.
        
        Parameters
        ----------
            *dnames : Tuple[str, ...]
                Data names to be calculated.

        Returns
        -------
            Callable
                Closure of the 'supply' method.
        """
        def supply(data: Dict[str, Logable]) -> Dict[str, Logable]:
            return self.supply(data, *dnames)
        return supply


class AdapterGroup(AdapterInterface, ComponentGroup):
    """A container of objects of AdapterBase. 
    
    AdapterGroup is a ComponentGroup and also a AdapterInterface, 
    in other words, this class is like an adapter as component group. 
    An adapter group can make users access to internal adapters 
    as a cluster of them, which means some methods of AdapterGroup 
    behave like ones of AdapterBase are executed all at once. 
    """

    def __init__(self, 
                 *adapters: Tuple[AdapterInterface, ...], 
                 name: Optional[str] = None) -> None:
        """
        Parameters
        ----------
            *adapters : Tuple[AdapterInterface, ...]
                Adapters to be included inside.
            name : Optional[str], optional
                Name of the component, by default None.
        """
        ComponentGroup.__init__(self, name=name)
        
        self._adapters: Set[AdapterInterface] = set()
        self._closures: Tuple[Callable] = ()
        self._DtoA: Dict[str, List[AdapterInterface]] = {}
        self._AtoD: Dict[AdapterInterface, List[str]] = {}

        if len(adapters):
            self.append(*adapters)

    def __add__(self, adapter):
        self.append(adapter)
        return self

    def __iadd__(self, adapter):
        return self.__add__(adapter)

    def extend(self, group) -> None:
        """Append internal adapters of given adapter group.

        Parameters
        ----------
            group : AdapterGroup
                Adapter group which has adapters inside.
        """
        self.append(*tuple(group._AtoD.keys()))

    def append(self, *adapters: Tuple[AdapterInterface, ...]) -> None:
        """Append adapters inside.
        
        Parameters
        ----------
            *adapters : Tuple[AdapterInterface, ...]
                Adapters to be included inside.

        Raises
        ------
            NotImplementedError
                Raised if given adapters are not instances of AdapterInterface.
        """
        ComponentGroup.append(self, *adapters)

        for adapter in adapters:
            if not isinstance(adapter, AdapterInterface):
                raise NotImplementedError(
                    "A given adapter object has not implemented the AdapterInterface."
                )

            # NOTE
            #   1.  AtoD will overwrite its dnames if a adapter already set up is given.
            #   2.  If user calls concentrate(), ignore() or remove(), and DtoA and
            #       AtoD is updated, this method will work to reset the DtoA and
            #       AtoD regarding given adapter.
            
            # update adapters set
            self._adapters.add(adapter)

            # update data2adapter map
            for dname in adapter.dnames:
                if self._DtoA.get(dname) is None:
                    self._DtoA[dname] = [adapter]
                else:
                    # avoid duplication
                    if adapter not in self._DtoA[dname]:
                        self._DtoA[dname].append(adapter)

            # update adapter2data map
            self._AtoD[adapter] = list(adapter.dnames)
            
        self._configure_closures()
        
    def _configure_closures(self):
        """Make closures depending on the current readability setting.
        """
        # TODO Think more reasonable algorism.
        res = []
        for adapter, reqs in self._AtoD.items():
            if len(adapter.dnames) == len(reqs):
                res.append(adapter.make_supply())
            else:
                res.append(adapter.make_supply(*tuple(reqs)))

        self._closures = tuple(res)
        
    def reset(self, 
              adapter: AdapterInterface, 
              dname: Optional[str] = None):
        """Reset readability setting about given object.
        
        The methods resets readability setting changed by other operations in the past.
        If 'dname' is None, then all data of the given adapter is to be reset their 
        readabilities.

        Parameters
        ----------
            adapter : AdapterInterface
                An adapter whose data readability is to be reset.
            dname : Optional[str], optional
                Data name to be reset, by default None

        Raises
        ------
            TypeError
                Raised if the given adapter is not an AdapterInterface.
            ValueError
                Raised if the given adapter doesn't have the given dname.
            
        Notes
        -----
            'Readability' means whether a kind of data of Adapter can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular adapters.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if not isinstance(adapter, AdapterInterface):
            raise TypeError(
                "'adapter' must be AdapterInterface."
            )
        
        if dname is None:
            self.append(adapter)
        else:
            if dname in adapter.dnames:
                # update DtoS
                if self._DtoA.get(dname) is None:
                    self._DtoA[dname] = [adapter]
                else:
                    # avoid duplication
                    if adapter not in self._DtoA[dname]:
                        self._DtoA[dname].append(adapter)
                        
                # update StoD
                dnames_adapter = self._AtoD.get(adapter)
                if dnames_adapter is None:
                    self._AtoD[adapter] = [dname]
                elif dname is not dnames_adapter:
                    self._AtoD[adapter].append(dname)
            else:
                raise ValueError(
                    "'dname' must be included dnames of 'adapter'."
                )
                
    def reset_all(self):
        """Reset all readability setting.
        
        See Also
        --------
            AdapterGroup.append : This method is used inside.
        """
        self.append(*tuple(self._adapters))
        
    def recollect(self, dname: str):
        """Reset the readability of given data name.

        Parameters
        ----------
            dname : str
                Data name whose readability is to be reset.
            
        See Also
        --------
            AdapterGroup.reset : This method is used inside.
        """
        adapters = {adapter for adapter in self._adapters if dname in adapter.dnames}
        for adapter in adapters:
            self.reset(adapter, dname=dname)

    def concentrate(self, dname: str, adapter: AdapterInterface):
        """Limit readability of given data to given object.
        
        The method changes readability setting of the given data as only data 
        emitted from the given 'adapter' is adopted as the data. This method only 
        makes sense when several object can read the given data. 

        Parameters
        ----------
            dname : str
                Data name.
            adapter : AdapterInterface
                Adapter to be ignored, by default None.

        Raises
        ------
            TypeError
                Raised if the given adapter is not AdapterInterface.
            ValueError
                Raised if the given adapter is not included in the adapter group.
            ValueError
                Raised if the given name is not included of the data names of 
                internal adapters.
            
        Notes
        -----
            'Readability' means whether a kind of data of Adapter can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular adapters.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if not isinstance(adapter, AdapterInterface):
            raise TypeError(
                "'adapter' must be AdapterInterface."
            )
        
        adapters = self._DtoA.get(dname)
        if adapters is None:
            raise ValueError("The 'adapter' is not included in the adapter group.")

        if adapter in adapters:
            # remove from AtoD except the given adapter
            for a in adapters:
                if a is adapter:
                    continue
                else:
                    self._AtoD[a].remove(dname)

            # remove from AtoS and rebuild
            self._DtoA[dname].clear()
            self._DtoA[dname].append(adapter)
            
            self._configure_closures()

        else:
            raise ValueError(
                "The AdapterGroup doesn't have the adapter which has the dname."
            )

    def ignore(self,
               dname: str,
               adapter: AdapterInterface = None):
        """Change readability of given data to be ignored.
        
        The method changes readability setting of the given data as ignored 
        when 'supply' method is called. if 'adapter' is None, the given data 
        completely ignored, but if 'adapter' is given, then the given 'adapter' 
        is ignored as for reading the given data.

        Parameters
        ----------
            dname : str
                Data name.
            adapter : AdapterInterface, optional
                Adapter to be ignored, by default None

        Raises
        ------
            TypeError
                Raised if the given adapter is not AdapterInterface.
            ValueError
                Raised if the given adapter is not included in the adapter group.
            ValueError
                Raised if the given name is not included of the data names of 
                internal adapters.
            
        Notes
        -----
            'Readability' means whether a kind of data of Adapter can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular adapters.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        if not isinstance(adapter, AdapterInterface):
            raise TypeError(
                "'adapter' must be AdapterInterface."
            )
        
        adapters = self._DtoA.get(dname)
        if adapters is None:
            raise ValueError("The 'adapter' is not included in the adapter group.")

        if adapter is None:
            for a in adapters:
                self._AtoD[a].remove(dname)
            self._DtoA.pop(dname)
        elif adapter in adapters:
            self._DtoA[dname].remove(adapter)
            self._AtoD[adapter].remove(dname)
        else:
            raise ValueError(
                "The AdapterGroup doesn't have the adapter which has the dname."
            )
            
        self._configure_closures()

    def remove(self, adapter: AdapterInterface):
        """Remove given adapter from readabilities of all data.
        
        The method changes readability settings of all data as 'adapter' is ignored 
        when 'supply' method is called. This means the given object is to be completely 
        removed and the method of 'adapter' is never called after executing this method. 
        If you want to recover the 'adapter', you can call the 'reset' method.

        Parameters
        ----------
            adapter : AdapterInterface
                Adapter to be removed.

        Raises
        ------
            ValueError
                Raised if the given adapter is not included in the adapter group.
            
        Notes
        -----
            'Readability' means whether a kind of data of Adapter can be read, 
            in other words, whether a kind of data has possibility to be 
            retrieved with the 'supply' method of some particular adapters.
            The readability setting can be changed by calling 'concentrate' or 
            'ignore' or 'remove' methods, and it can be reset by 'reset' method.
        """
        for dname in adapter.dnames:
            adapter_list = self._DtoA.get(dname)
            if adapter_list is None:
                raise ValueError("The AdapterGroup doesn't have the adapter.")
            else:
                adapter_list.remove(adapter)
                
        self._AtoD.pop(adapter)
        self._configure_closures()
        
    def delete(self, adapter: AdapterInterface):
        """Remove given adapter completely.
        
        This method removes the given adapter from internal adapters set.
        Thus, users cannot reset the readability of the adapter after 
        calling this method.

        Parameters
        ----------
            adapter : AdapterInterface
                Adapter to be removed.
            
        See Also
        --------
            AdapterGroup.remove : This method is used inside.
        """
        self.remove(adapter)
        self._adapters.discard(adapter)

    def get_adapter(self, dname: str) -> List[AdapterInterface]:
        """Retrive adapters from given data name.

        Parameters
        ----------
            dname : str
                Data name to be searched.

        Returns
        -------
            List[AdapterInterface]
                Result of searching.
        """
        collected = self._DtoA.get(dname)
        if collected is None:
            return []
        
        return collected

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #   AdapterInterface implementions                                           #
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   #

    @property
    def dnames(self) -> Tuple[str]:
        return tuple(self._DtoA.keys())
    
    @property
    def requires(self) -> Dict[str, Tuple[str]]:
        reqs = {}
        for a in self._AtoD.keys():
            reqs.update(a.requires)
        return reqs

    def supply(self, data: Dict[str, Logable], *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Calculate from given data in the current readability setting.

        Parameters
        ----------
            data : dict
                Data included nessesary data

            *dname: Tuple[str, ...]
                Data names to be returned. If no given, all data
                available is to be returned.
                
        Returns
        -------
            Dict[str, Logable]
                Data calculated.

        Notes
        -----
            If data is not sufficient for calculation, then an adapter 
            given deficient data outputs all data's values are None.
        """
        result = {}
        if len(dnames) == 0:
            for closure in self._closures:
                result.update(closure(data))
        else:
            for dname in dnames:
                for adapter in self.get_adapter(dname=dname):
                    result.update(adapter.supply(data, dname))

        return result


class AdapterBase(AdapterInterface):
    """An element of the adapter set. 
    
    Diversity of the adapter system is one of the classes of AdapterBase. 
    In the pisat system (or the adapter system) an adapter means 
    an object of the AdapterBase. The AdapterBase should be inheritanced 
    in most cases. An adapter represents a calculator which recieve some 
    required values and output the result calculated from the input values. 
    In almost all cases, adapters are abstracted by logging classes, 
    especially SensorController. The logging classes combine sensors and 
    adapters inside, and the output data from the sensors are given to 
    the adapters, finally users can get the result of adapters' output and 
    sensors'. 
    
    This class is an abstract class of adapters. Subclasses of this class 
    must override some attributes and methods, at least, DATA_NAMES, 
    DATA_REQUIRES and calc. More information, see the references of 
    attributes and methods.
    
    Attributes
    ----------
        DATA_NAMES : Tuple[str]
            Data names the adapter outputs.
        DATA_REQUIRES : Dict[str, Tuple[str]]
            Data required for calculation.
            
    Notes
    -----
        DATA_NAMES must be same as keys of output of the 'calc' method. 
        
        The DATA_REQUIRES is a dictionary, whose keys are elements of the 
        DATA_NAMES and values are tuples required to calculate the keys. 
    """

    DATA_NAMES: Tuple[str] = ()
    DATA_REQUIRES: Dict[str, Tuple[str]] = {}

    def __str__(self):
        return self.__class__.__name__

    def __add__(self, adapter):
        return AdapterGroup(self, adapter)

    def __iadd__(self, adapter):
        return self.__add__(adapter)

    @property
    def dnames(self) -> Tuple[str]:
        return self.DATA_NAMES

    @property
    def requires(self) -> Dict[str, Tuple[str]]:
        return self.DATA_REQUIRES
    
    def calc(self, data: Dict[str, Logable], *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Calculate from given data in the current readability setting.
        
        This method is an abstract method. 

        Parameters
        ----------
            data : dict
                Data included nessesary data

            *dname: Tuple[str, ...]
                Data names to be returned. If no given, all data
                available is to be returned.

        Returns
        -------
            Dict[str, Logable]
                Data calculated.
        """
        pass

    def supply(self, data: Dict[str, Logable], *dnames: Tuple[str, ...]) -> Dict[str, Logable]:
        """Calculate from given data in the current readability setting.

        Parameters
        ----------
            data : dict
                Data included nessesary data

            *dname: Tuple[str, ...]
                Data names to be returned. If no given, all data
                available is to be returned.

        Returns
        -------
            Dict[str, Logable]
                Data calculated.
        """
        try:
            return self.calc(data, *dnames)
        except:
            return {}