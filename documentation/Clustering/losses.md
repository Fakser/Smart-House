# Losses

> Auto-generated documentation for [Clustering.losses](..\..\Clustering\losses.py) module.

- [Smart-house-rest-api](..\README.md#table-of-contents) / [Modules](..\MODULES.md#smart-house-rest-api-modules) / [Multidimensional-Clustering](index.md#multidimensional-clustering) / Losses
    - [geometric_distance](#geometric_distance)

## geometric_distance

[[find in source code]](..\..\Clustering\losses.py#L6)

```python
def geometric_distance(a, b, dist=0):
```

Loss function calculating geometric distance between 2 objects.
It can be explained by the example of distance between two points
on 2D plane.

^
|        .B(x2, y2)
|       /
|      /
|     .A(x1, y1)
|
+ --------------------- >

It is derived by:
sqrt((x1 - x2)^2 + (y1 - y2)^2)
This implementation of distance metric is multidimensional, which enables
calculation of geometric distance between

#### Arguments

- `a` *object* - first object
- `b` *object* - second object of same length as object a
- `dist` *int, optional* - [description]. Defaults to 0.

#### Returns

- `float` - value of geometric distance
