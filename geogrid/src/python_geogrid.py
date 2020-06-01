# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _python_geogrid
else:
    import _python_geogrid

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)
try:
  import numpy as np
except:
  raise ImportError("import numpy library error.")
import os
import re

class geogrid:

  def __init__(self, open_model):
    self._open_model               = open_model
    self._index                    = {}
    self._index["projection"     ] = None
    self._index["type"           ] = None
    self._index["signed"         ] = None
    self._index["units"          ] = None
    self._index["description"    ] = None
    self._index["dx"             ] = None
    self._index["dy"             ] = None
    self._index["known_x"        ] = None
    self._index["known_y"        ] = None
    self._index["known_lat"      ] = None
    self._index["known_lon"      ] = None
    self._index["stdlon"         ] = None
    self._index["truelat1"       ] = None
    self._index["truelat2"       ] = None
    self._index["wordsize"       ] = None
    self._index["tile_x"         ] = None
    self._index["tile_y"         ] = None
    self._index["tile_z"         ] = None
    self._index["tile_z_start"   ] = None
    self._index["tile_z_end "    ] = None
    self._index["category_min"   ] = None
    self._index["category_max"   ] = None
    self._index["tile_bdr"       ] = None
    self._index["missing_value"  ] = None
    self._index["scale_factor"   ] = None
    self._index["row_order"      ] = None
    self._index["endian"         ] = None # big or little
    self._index["iswater"        ] = None
    self._index["islake"         ] = None
    self._index["isice"          ] = None
    self._index["isurban"        ] = None
    self._index["isoilwater"     ] = None
    self._index["mminlu"         ] = None
    self._index["filename_digits"] = None

  def __read_model_error(self):
    read_model = ["read", "r"]
    if self._open_model.lower() not in read_model: raise SyntaxError("This method not in read model.")

  def __write_model_error(self):
    write_model = ["write", "w"]
    if self._open_model.lower() not in write_model: raise SyntaxError("This method not in write model.")
  
  def __read_index(self, path):
    self.__read_model_error()
    if not os.path.exists(f"{path}/index"): raise RuntimeError("index file not in directory.")
    with open(f"{path}/index", "r") as f:
      content = f.readlines() 
    index_float = ["dx", "dy", "known_x", "known_y", "known_lat", "known_lon", "stdlon", "truelat1", "truelat2", "missing_value"]
    index_int   = ["wordsize", "tile_x", "tile_y", "tile_z", "tile_z_start", "tile_z_end", "category_min", "category_max",
                   "tile_bdr", "scale_factor", "iswater", "islake", "isice", "isurban", "isoilwater", "filename_digits"]
    for line in content:
      key   = line.split("=")[0].strip().lower()
      value = line.split("=")[1]
      if key in index_float:
        self._index[key] = float(value)
        continue
      if key in index_int:
        self._index[key] = int(value)
        continue
      self._index[key] = value

  def read_geogrid(self, data_root, dtype):

    self.__read_index(data_root)

    signed       = 1   if not self._index["signed"]        else self._index["signed"]
    endian       = 0   if not self._index["endian"]        else self._index["endian"]
    wordsize     = 1   if not self._index["wordsize"]      else self._index["wordsize"]
    scale_factor = 1.0 if not self._index["scale_factor"]  else self._index["scale_factor"]
    fill_value   = 255 if not self._index["missing_value"] else self._index["missing_value"]

    dx        = self._index["dx"]
    dy        = self._index["dy"]
    known_x   = self._index["known_x"]
    known_y   = self._index["known_y"]
    known_lat = self._index["known_lat"]-(known_y-1)*dy
    known_lon = self._index["known_lon"]-(known_x-1)*dx
    nz        = self._index["tile_z"]
    ny        = self._index["tile_y"]
    nx        = self._index["tile_x"]

    filenames = os.listdir(data_root)

    tiles_infos = {}
    for filename in filenames:
      match = re.match(r'(\d{5})-(\d{5}).(\d{5})-(\d{5})', filename)
      if not match: continue
      tiles_infos[filename] = {}
      tiles_infos[filename]["xstart"] = int(match.group(1))
      tiles_infos[filename]["xend"]   = int(match.group(2))
      tiles_infos[filename]["ystart"] = int(match.group(3))
      tiles_infos[filename]["yend"]   = int(match.group(4))

    count = 0
    for key, value in tiles_infos.items():
      count += 1
      if count == 1:
        xstart = value["xstart"]
        xend   = value["xend"]
        ystart = value["ystart"]
        yend   = value["yend"]
      else:
        xstart = min(xstart, value["xstart"])
        xend   = max(xend  , value["xend"])
        ystart = min(xstart, value["ystart"])
        yend   = max(yend  , value["yend"])

    geotransform = (known_lon+(xstart-1)*dx, dx, 0.0, known_lat+(xend-1)*dy, 0.0, -dy)

    array = np.full(shape=(nz, yend-ystart+1, xend-xstart+1), dtype=dtype, fill_value=fill_value)
    rarray = np.zeros(shape=(nz, ny, nx), dtype=np.float32)

    for key, value in tiles_infos.items():
      filename = key
      xstart = value["xstart"]
      xend   = value["xend"]
      ystart = value["ystart"]
      yend   = value["yend"]
      status = _python_geogrid.read_geogrid(filename, len(filename), rarray, signed, endian, scale_factor, wordsize)
      array[:, ystart-1:yend, xstart-1:xend] = rarray[:, ::-1, :]
      print(rarray)

    return array, geotransform

  def __write_index(self, index_root):
    self.__write_model_error()
    index_float1 = ["dx", "dy", "known_lat", "known_lon", "stdlon", "truelat1", "truelat2"]
    index_float2 = ["known_x", "known_y"]
    with open(f"{index_root}/index", "w") as f:
      for key, value in self._index.items():
        if not value: continue
        if key in index_float1: 
          f.write(f"{key}={value:.11f}\n")
          continue
        if key in index_float2:
          f.write(f"{key}={value:.1f}\n")
          continue
        f.write(f"{key}={value}\n")

  def get_index(self, **kw):
    self.__read_model_error()
    if not kw: return self._index
    if "key" in kw:
      return self._index[kw["key"].strip().lower()]

  def set_index(self, **kw):
    self.__write_model_error()
    if "key" in kw and "index" in kw: raise SyntaxError("can not input key and index in same time.")
    if "key" in kw:
      if not "value" in kw: raise SyntaxError("key value is empty.")
      if kw["key".strip().lower()] not in self._index: raise KeyError("This keyword not in geogrid index file.")
      self._index[kw["key"].strip().lower()] = kw["value"]
    if "index" in kw:
      for key, value in kw["index"].items():
        self._index[key.strip().lower()] = value

  def write_geogrid(self, array, index_root):

    self.__write_model_error()

    signed       = 1   if not self._index["signed"]       else self._index["signed"]
    endian       = 0   if not self._index["endian"]       else self._index["endian"]
    wordsize     = 1   if not self._index["wordsize"]     else self._index["wordsize"]
    scale_factor = 1.0 if not self._index["scale_factor"] else self._index["scale_factor"]

    ndim = array.ndim
    shape = array.shape
    
    if ndim == 3:
      nz = shape[0]
      ny = shape[1]
      nx = shape[2]
    else:
      nz = 1
      ny = shape[0]
      nx = shape[1]


    rarray = np.zeros(shape=(nz, ny, nx), dtype=np.float32)

    if ndim == 3: rarray[:, :, :] = array[:,::-1, :]
    if ndim == 2: rarray[0, :, :] = array[::-1, :]

    self.__write_index(index_root)

    status = _python_geogrid.write_geogrid(rarray, signed, endian, scale_factor, wordsize)
