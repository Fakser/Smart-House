Module Smart-house-REST-API.Clustering.utils
============================================

Functions
---------

    
`is_iter(variable)`
:   Function that can be used to find 
    wheter object is iterable
    
    Args:
        variable (object): ariable to be checked
    
    Returns:
        True: variable is iterable
        False: variable is not iterable
    
    >>> from losses import is_iter
    >>> is_iter([1,2])
    True
    >>> is_iter("hello")
    >>> is_iter(6)
    False

    
`recursive_list(array)`
:   Function creating a list from iterable object of any shape
    
    Args:
        array (iterable): iterable object to be changed into list
    
    Returns:
        list: array of type list
    
    >>> from utils import recursive_list
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_list(tab)
    [[[1, 2], 3], [[-1, 5], 6], [[4, 2], -9]]

    
`recursive_max(array, max_val=None)`
:   Function that returns maximum value of an interable
    object of any shape 
    
    Args:
        array (iterable): array/list/iterable object of any shape
        max_val ([type], optional): in-function parameter. Defaults to None. Do not change.
    
    Returns:
        float: maximum found in the array
    
    >>> from utils import recursive_max
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_max(tab)
    6

    
`recursive_mean(array)`
:   Function calculationg mean point from all objects in an iterable array.
    
    Args:
        array (iterable): array of objects of the same shape
    
    Returns:
        object: mean object of the array
    
    >>> from utils import recursive_mean
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_mean(tab)
    [[1.3333333333333333, 3.0], 0.0]

    
`recursive_min(array, min_val=None)`
:   Function that returns minimum value of an interable
    object of any shape 
    
    Args:
        array (iterable): array/list/iterable object of any shape
        min_val ([type], optional): in-function parameter. Defaults to None. Do not change.
    
    Returns:
        float: minimum found in the array
    
    >>> from utils import recursive_max
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_max(tab)
    -9

    
`recursive_nparray(array)`
:   Function creating a numpy array from iterable object of any shape
    
    Args:
        array (iterable): iterable object to be changed into numpy array
    
    Returns:
        array: array of type numpy_array
    
    >>> from utils import recursive_nparray
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_nparray(tab)
    array([[array([1, 2]), 3],
       [array([-1,  5]), 6],
       [array([4, 2]), -9]], dtype=object)