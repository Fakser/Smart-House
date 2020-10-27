import os

from Clustering.controller import *

from Clustering.losses import geometric_distance
from Clustering.utils import *

class Model(object):
    def __init__(self, X_train, n_clusters = 3, loss = 'distance'):
        """
        Init function of obcject K_Means.Model

        Args:
            X_train (iterable): Iterable object that represents data to be clustered
            n_clusters (int, optional): [description]. Defaults to 3.
            loss (str, optional): [description]. Defaults to 'distance'.
        """
        self.n_clusters = n_clusters
        self.data = deepcopy(X_train)
        if loss == 'distance':
            self.loss = geometric_distance
        self.clusters = [[] for _ in range(self.n_clusters)]
        self.centroids = []
        self.history = []

        self.centroids = [self._create_random_centroid(data = self.data[0], min_value = recursive_min(self.data), max_value=recursive_max(self.data)) for _ in range(self.n_clusters)]
        self.history.append(deepcopy(self.centroids))
        self.__centroids__()

    def __centroids__(self, epoch = 0, verbose = 1):
        """
        Method printing current centroids
        Args:
            epoch (int, optional): [description]. Defaults to 0.
            verbose (int, optional): [description]. Defaults to 1.
        """
        print("\nepoch {}:\n".format(epoch))
        for cluster_index, cluster in enumerate(self.clusters):
            print("\rcluster {} of size {} with centroid: {}".format(cluster_index + 1, len(cluster), self.centroids[cluster_index]))


    def _create_random_centroid(self, data, min_value, max_value):
        """
        Method creating random centroid based on provided data

        Args:
            data (iterable): one data ponit/reading from whole dataset 
            min_value ([type]): minimal value of the dataset
            max_value ([type]): maximal value of the dataset

        Returns:
            list: random centroid
        """
        centroid = []
        for x in data:
            if is_iter(x):
                centroid.append(self._create_random_centroid(x, min_value, max_value))
            else:
                centroid.append(np.random.normal(min_value, max_value))
        return centroid

    def predict(self, X):
        """
        Method that predicts to witch cluster belong each element of provided X

        Args:
            X (iterable): data to be classified into clusters

        Returns:
            iterable: array of predicted clusters
        """
        best_centroids = []
        for current_index, x in enumerate(X):
            best_distance = None
            best_centroid_index = None
            for centroid_index, centroid in enumerate(self.centroids):
                dist = self.loss(x, centroid)
                try:
                    if best_distance > dist:
                        best_distance = dist
                        best_centroid_index = centroid_index
                except:
                    best_distance = dist
                    best_centroid_index = centroid_index
            best_centroids.append(self.centroids[best_centroid_index])
        return best_centroids

    def fit(self, epochs = 50, verbose = 2):
        """
        Method for fitting K-Mean algorithm to the dataset

        Args:
            epochs (int, optional): Max number of epochs. Defaults to 50.
            verbose (int, optional): Level of printing --> higher level means more information. Defaults to 2.
        """
        X = self.data
        for epoch in range(epochs):
            self.clusters = [[] for _ in range(self.n_clusters)]
            for current_index, x in enumerate(X):
                best_distance = None
                best_centroid_index = None
                for centroid_index, centroid in enumerate(self.centroids):
                    try:
                        dist = self.loss(x, centroid)
                    except Exception as e:
                        print(x, centroid, e) 
                    try:
                        if best_distance > dist:
                            best_distance = dist
                            best_centroid_index = centroid_index
                    except:
                        best_distance = dist
                        best_centroid_index = centroid_index

                self.clusters[best_centroid_index].append(current_index)

            for cluster_index, cluster in enumerate(self.clusters):
                self.centroids[cluster_index] = recursive_mean([X[x] for x in cluster])
                if len(cluster) == 0:
                    self.centroids[cluster_index] = self._create_random_centroid(data = self.data[0], min_value = recursive_min(self.data), max_value=recursive_max(self.data))

            self.history.append(deepcopy(self.centroids))
            if verbose >= 1:
                self.__centroids__(epoch = epoch+1, verbose=verbose)

            #TODO recursive early stopping
            # early_stopping = True
            # for index in range(self.n_clusters):
            #     if self.history[-1][index] - self.history[-2][index]:
            #         early_stopping = False
            #         break
            # if early_stopping:
            #     print('eary stopping on epoch: {}'.format(epoch+1))
            #     break
