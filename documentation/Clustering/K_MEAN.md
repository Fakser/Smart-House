# K Mean

> Auto-generated documentation for [Clustering.K_MEAN](..\..\Clustering\K_MEAN.py) module.

- [Smart-house-rest-api](..\README.md#description) / [Modules](..\MODULES.md#smart-house-rest-api-modules) / [Multidimensional-Clustering](index.md#multidimensional-clustering) / K Mean
    - [Model](#model)
        - [Model().\_\_centroids\_\_](#model__centroids__)
        - [Model().fit](#modelfit)
        - [Model().predict](#modelpredict)

## Model

[[find in source code]](..\..\Clustering\K_MEAN.py#L8)

```python
class Model(object):
    def __init__(X_train, n_clusters=3, loss='distance'):
```

### Model().\_\_centroids\_\_

[[find in source code]](..\..\Clustering\K_MEAN.py#L30)

```python
def __centroids__(epoch=0, verbose=1):
```

Method printing current centroids

#### Arguments

- `epoch` *int, optional* - [description]. Defaults to 0.
- `verbose` *int, optional* - [description]. Defaults to 1.

### Model().fit

[[find in source code]](..\..\Clustering\K_MEAN.py#L88)

```python
def fit(epochs=50, verbose=2):
```

Method for fitting K-Mean algorithm to the dataset

#### Arguments

- `epochs` *int, optional* - Max number of epochs. Defaults to 50.
- `verbose` *int, optional* - Level of printing --> higher level means more information. Defaults to 2.

### Model().predict

[[find in source code]](..\..\Clustering\K_MEAN.py#L62)

```python
def predict(X):
```

Method that predicts to witch cluster belong each element of provided X

#### Arguments

- `X` *iterable* - data to be classified into clusters

#### Returns

- `iterable` - array of predicted clusters
