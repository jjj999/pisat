
from typing import TypeVar

from pisat.config.datamodel import loggable, DataModelBase
from pisat.config.linked_datamodel import linked_loggable, LinkedDataModelBase, LinkNotSetError


DataModelGen = TypeVar("DataModelGen")
LinkedDataModelGen = TypeVar("LinkedDataModelGen")
