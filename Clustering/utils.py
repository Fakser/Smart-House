from Clustering.controller import *

def is_iter(variable):
    """
    Function that can be used to find 
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
    """
    try:
        _  = (a for a in range(len(variable)))
    except:
        return False
    return True

def recursive_min(array, min_val = None):
    """
    Function that returns minimum value of an interable
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
    """
    if is_iter(array):
        for data in array:
            if is_iter(data):
                min_val = recursive_min(data, min_val)
            elif (min_val and min_val > data) or (min_val == None):
                min_val = data
    else:
        if (min_val and min_val > array) or (min_val == None):
            min_val = array
    return min_val



def recursive_max(array, max_val = None):
    """
    Function that returns maximum value of an interable
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

    """
    if is_iter(array):
        for data in array:
            if is_iter(data) == True:
                max_val = recursive_max(data, max_val)
            elif (max_val and max_val < data) or (max_val == None):
                max_val = data
    else:
        if (max_val and max_val < array) or (max_val == None):
            max_val = array
    return max_val
    
def recursive_list(array):
    """
    Function creating a list from iterable object of any shape

    Args:
        array (iterable): iterable object to be changed into list

    Returns:
        list: array of type list
    
    >>> from utils import recursive_list
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_list(tab)
    [[[1, 2], 3], [[-1, 5], 6], [[4, 2], -9]]
    """
    if is_iter(array):
        for data_index in range(len(array)):
            if is_iter(array[data_index]) == True:
                array[data_index] = recursive_list(array[data_index])
        return list(array)
    else:
        return array
            
def recursive_nparray(array):
    """
    Function creating a numpy array from iterable object of any shape

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
    """
    if is_iter(array):
        for data_index in range(len(array)):
            if is_iter(array[data_index]) == True:
                array[data_index] = recursive_nparray(array[data_index])
        return np.array(array)
    else:
        return array

def recursive_mean(array):
    """
    Function calculationg mean point from all objects in an iterable array.

    Args:
        array (iterable): array of objects of the same shape

    Returns:
        object: mean object of the array
    
    >>> from utils import recursive_mean
    >>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
    >>> recursive_mean(tab)
    [[1.3333333333333333, 3.0], 0.0]
    """
    if len(array) > 0:
        np_array = recursive_nparray(deepcopy(array))
        mean_of_np_array = np_array[0]
        for data in np_array[1:]:
            mean_of_np_array += data
        return recursive_list(mean_of_np_array/len(np_array))
    else:
        return array
