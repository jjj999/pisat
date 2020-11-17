

from pisat.util.deco import cached_property
import time
from typing import Optional, Tuple

import numpy as np

from pisat.model.datamodel import DataModelBase, loggable, cached_loggable


def get_tag_name(publisher: str, tag: str, coo: Tuple[str]):
    return [f"{publisher}-{tag}_{x}" for x in coo]


# NOTE pisat 内での機体座標系を固定する

class AccModel(DataModelBase):
    
    TAG_ACC = "acc"
    TAG_DIFF_ACC = "diff_acc"
    TAG_VEL = "vel"
    
    COO = ("X", "Y", "Z")
    
    def __init__(self, publisher: str) -> None:
        super().__init__(publisher)
        
        self._time = 0
        self._acc = np.zeros(3)
        self._last_time = 0
        self._last_acc = np.zeros(3)
    
    def setup(self, acc: np.ndarray):
        super().setup()
        
        # NOTE only at first time, initialize two times as same.
        if not self._time:
            self._time = time.time()
            self._last_time = self._time
        
        self._last_time = self._time
        self._last_acc = self._acc
        self._time = time.time()
        self._acc = acc
        
    @loggable
    def acc(self):
        return self._acc
    
    @acc.formatter
    def acc(self):
        names = get_tag_name(self.publisher, self.TAG, self.COO)
        return {name: val for name, val in zip(names, self._acc)}
    
    @property
    def delta_time(self):
        return self._time - self._last_time
    
    
class AccPlusModel(AccModel):
    
    TAG_ACC_LIN = "acc_lin"
    TAG_ACC_GRA = "acc_gra"
    
    def __init__(self, publisher: str) -> None:
        super().__init__(publisher)
        
        self._acc_lin = np.zeros(3)
        self._acc_gra = np.zeros(3)
        self._last_acc_lin = np.zeros(3)
        self._last_acc_gra = np.zeros(3)
        
    def setup(self, acc: np.ndarray, acc_lin: np.ndarray, acc_gra: np.ndarray):
        super().setup(acc)
        
        self._last_acc_lin = self._acc_lin
        self._last_acc_gra = self._acc_gra
        self._acc_lin = acc_lin
        self._acc_gra = acc_gra
        
    @loggable
    def acc_lin(self):
        return self._acc_lin
    
    @acc_lin.formatter
    def acc_lin(self):
        names = get_tag_name(self.publisher, self.TAG_ACC_LIN, self.COO)
        return {name: val for name, val in zip(names, self._acc_lin)}
    
    @loggable
    def acc_gra(self):
        return self._acc_gra
    
    @acc_gra.formatter
    def acc_gra(self):
        names = get_tag_name(self.publisher, self.TAG_ACC_GRA, self.COO)
        return {name: val for name, val in zip(names, self._acc_gra)}
    
    @property
    def delta_acc(self):
        return self._acc_lin - self._last_acc_lin
    
    @cached_loggable
    def diff_acc(self):
        return self.delta_acc / self.delta_time
    
    @diff_acc.formatter
    def diff_acc(self):
        names = get_tag_name(self.publisher, self.TAG_DIFF_ACC, self.COO)
        return {name: val for name, val in zip(names, self.diff_acc)}
        
    @cached_loggable
    def velocity(self):
        return (self._last_acc_lin + self._acc_lin) * self.delta_time / 2
    
    @velocity.formatter
    def velocity(self):
        names = get_tag_name(self.publisher, self.TAG_VEL, self.COO)
        return {name: val for name, val in zip(names, self.velocity)}


# TODO
# 1. Enable it to work on any sensors
# 2. Consider about handling same data (like gyro, euler and quat) 

class IMU9Model(DataModelBase):
    """DataModel for IMU with 9 degrees of freedom.
    """
        
    def setup(self, acc: np.ndarray, mag: np.ndarray, gyro: np.ndarray,
              euler: np.ndarray, quat: np.ndarray, acc_lin: Optional[np.ndarray], acc_gra: np.ndarray):
                    
        self._delta_t = 0
        self._last_acc = np.zeros(3)
        self._last_mag = np.zeros(3)
        self._last_gyro = np.zeros(3)
        self._last_euler = np.zeros(3)
        self._last_quat = np.zeros(3)
        self._last_acc_lin = np.zeros(3)
        self._last_acc_gra = np.zeros(3)
        
        self._acc = acc
        self._mag = mag
        self._gyro = gyro
        self._euler = euler
        self._quat = quat
        self._acc_lin = acc_lin
        self._acc_gra = acc_gra
        
        def get_name(tag: str, coo: Tuple[str]):
            return [f"{self.publisher}-{tag}_{x}" for x in coo]
        
        self._name_acc = get_name("acc", ("X", "Y", "Z"))
        self._name_mag = get_name("mag", ("X", "Y", "Z"))
        self._name_gyro = get_name("gyro", ("X", "Y", "Z"))
        self._name_euler = get_name("euler", ("X", "Y", "Z"))
        self._name_quat = get_name("quat", ("X", "Y", "Z", "W"))
        self._name_acc_lin = get_name("acc_lin", ("X", "Y", "Z"))
        self._name_acc_gra = get_name("acc_gra", ("X", "Y", "Z"))
        
    def update(self, delta_t: float, acc: np.ndarray, mag: np.ndarray, gyro: np.ndarray,
               euler: np.ndarray, quat: np.ndarray, acc_lin: np.ndarray, acc_gra: np.ndarray):
        super().update()
        
        self._delta_t = delta_t
        self._last_acc = self._acc
        self._last_mag = self._mag
        self._last_gyro = self._gyro
        self._last_euler = self._euler
        self._last_quat = self._quat
        self._last_acc_lin = self._acc_lin
        self._last_acc_gra = self._acc_gra
        
        self._acc = acc
        self._mag = mag
        self._gyro = gyro
        self._euler = euler
        self._quat = quat
        self._acc_lin = acc_lin
        self._acc_gra = acc_gra
        
    @cached_loggable
    def velocity(self):
        return 
        
    @loggable
    def acc(self):
        return self._acc
    
    @acc.formatter
    def acc(self):
        return {name: val for name, val in zip(self._name_acc, self._acc)}
    
    @loggable
    def mag(self):
        return self._mag
    
    @mag.formatter
    def mag(self):
        return {name: val for name, val in zip(self._name_mag, self._mag)}
    
    @loggable
    def gyro(self):
        return self._gyro
    
    @gyro.formatter
    def gyro(self):
        return {name: val for name, val in zip(self._name_gyro, self._gyro)}
    
    @loggable
    def euler(self):
        return self._euler
    
    @euler.formatter
    def euler(self):
        return {name: val for name, val in zip(self._name_euler, self._euler)}
    
    @loggable
    def quat(self):
        return self._quat
    
    @quat.formatter
    def quat(self):
        return {name: val for name, val in zip(self._name_quat, self._quat)}
    
    @loggable
    def acc_lin(self):
        return self._acc_lin
    
    @acc_lin.formatter
    def acc_lin(self):
        return {name: val for name, val in zip(self._name_acc_lin, self._acc_lin)}
    
    @loggable
    def acc_gra(self):
        return self._acc_gra
    
    @acc_gra.formatter
    def acc_gra(self):
        return {name: val for name, val in zip(self._name_acc_gra, self._acc_gra)}
