"""
SunPy Map objects are constructed using the special `Map()` function. ::

>>> map = sunpy.Map('file.fits')

The result of a call to `Map` will be either a generic 
:class:`sunpy.data.BaseMap` object, or a sublcass of :class:`sunpy.data.BaseMap` 
which deals with a specific type of data, e.g. :class:`AIAMap` or 
:class:`LASCOMap`.
"""
__author__ = "Keith Hughitt"
__email__ = "keith.hughitt@nasa.gov"

import sys
import pyfits
from sunpy.data.sources import *
from sunpy.data.BaseMap import BaseMap
from sunpy.data.BaseMap import UnrecognizedDataSouceError

def Map(input_):
    """Map class factory
    
    Attempts to determine the type of data associated with input and returns
    an instance of either the generic BaseMap class or a subclass of BaseMap
    such as AIAMap, EUVIMap, etc.
    
    Parameters
    ----------
    input_ : filepath, data array
        The data source used to create the map object. This can be either a
        filepath to an image, a 2d list, or an ndarray.
        
    Returns
    -------
    out : BaseMap
        Returns a BaseMap or BaseMap subclass instance
    
    References
    ----------
    http://stackoverflow.com/questions/456672/class-factory-in-python
    """
    if isinstance(input_, str):
        try:
            fits = pyfits.open(input_)
            data = fits[0].data
            header = fits[0].header
        except IOError:
            sys.exit("Unable to read the file %s" % input_)

        for cls in BaseMap.__subclasses__():
            if cls.is_datasource_for(header):
                return cls(data, header)
        raise UnrecognizedDataSouceError

    else:
        return BaseMap(input_)
