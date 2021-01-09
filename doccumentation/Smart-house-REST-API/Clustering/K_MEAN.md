Module Smart-house-REST-API.Clustering.K_MEAN
=============================================

Classes
-------

`Model(X_train, n_clusters=3, loss='distance')`
:   Init function of obcject K_Means.Model
    
    Args:
        X_train (iterable): Iterable object that represents data to be clustered
        n_clusters (int, optional): [description]. Defaults to 3.
        loss (str, optional): [description]. Defaults to 'distance'.

    ### Methods

    `fit(self, epochs=50, verbose=2)`
    :   Method for fitting K-Mean algorithm to the dataset
        
        Args:
            epochs (int, optional): Max number of epochs. Defaults to 50.
            verbose (int, optional): Level of printing --> higher level means more information. Defaults to 2.

    `predict(self, X)`
    :   Method that predicts to witch cluster belong each element of provided X
        
        Args:
            X (iterable): data to be classified into clusters
        
        Returns:
            iterable: array of predicted clusters