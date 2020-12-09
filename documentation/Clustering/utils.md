# Utils

> Auto-generated documentation for [Clustering.utils](..\..\Clustering\utils.py) module.

- [Smart-house-rest-api](..\README.md#table-of-contents) / [Modules](..\MODULES.md#smart-house-rest-api-modules) / [Multidimensional-Clustering](index.md#multidimensional-clustering) / Utils
    - [is_iter](#is_iter)
    - [recursive_list](#recursive_list)
    - [recursive_max](#recursive_max)
    - [recursive_mean](#recursive_mean)
    - [recursive_min](#recursive_min)
    - [recursive_nparray](#recursive_nparray)

## is_iter

[[find in source code]](..\..\Clustering\utils.py#L3)

```python
def is_iter(variable):
```

Function that can be used to find
wheter object is iterable

#### Arguments

- `variable` *object* - ariable to be checked

#### Returns

- `True` - variable is iterable
- `False` - variable is not iterable

```python
>>> from losses import is_iter
>>> is_iter([1,2])
True
>>> is_iter("hello")
>>> is_iter(6)
False

## recursive_list

[[find in source code]](..\..\Clustering\utils.py#L87)

```python
def recursive_list(array):
```

Function creating a list from iterable object of any shape

#### Arguments

- `array` *iterable* - iterable object to be changed into list

#### Returns

- `list` - array of type list

```python
>>> from utils import recursive_list
>>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
>>> recursive_list(tab)
[[[1, 2], 3], [[-1, 5], 6], [[4, 2], -9]]

## recursive_max

[[find in source code]](..\..\Clustering\utils.py#L58)

```python
def recursive_max(array, max_val=None):
```

Function that returns maximum value of an interable
object of any shape

#### Arguments

- `array` *iterable* - array/list/iterable object of any shape
- `max_val` *[type], optional* - in-function parameter. Defaults to None. Do not change.

#### Returns

- `float` - maximum found in the array

```python
>>> from utils import recursive_max
>>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
>>> recursive_max(tab)
6

## recursive_mean

[[find in source code]](..\..\Clustering\utils.py#L135)

```python
def recursive_mean(array):
```

Function calculationg mean point from all objects in an iterable array.

#### Arguments

- `array` *iterable* - array of objects of the same shape

#### Returns

- `object` - mean object of the array

```python
>>> from utils import recursive_mean
>>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
>>> recursive_mean(tab)
[[1.3333333333333333, 3.0], 0.0]

## recursive_min

[[find in source code]](..\..\Clustering\utils.py#L28)

```python
def recursive_min(array, min_val=None):
```

Function that returns minimum value of an interable
object of any shape

#### Arguments

- `array` *iterable* - array/list/iterable object of any shape
- `min_val` *[type], optional* - in-function parameter. Defaults to None. Do not change.

#### Returns

- `float` - minimum found in the array

```python
>>> from utils import recursive_max
>>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
>>> recursive_max(tab)
-9

## recursive_nparray

[[find in source code]](..\..\Clustering\utils.py#L110)

```python
def recursive_nparray(array):
```

Function creating a numpy array from iterable object of any shape

#### Arguments

- `array` *iterable* - iterable object to be changed into numpy array

#### Returns

- `array` - array of type numpy_array

```python
>>> from utils import recursive_nparray
>>> tab = [[[1, 2], 3] , [[-1, 5], 6], [[4, 2], -9]]
>>> recursive_nparray(tab)
array([[array([1, 2]), 3],
   [array([-1,  5]), 6],
   [array([4, 2]), -9]], dtype=object)
