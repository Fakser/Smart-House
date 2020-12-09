import pandas as pd
from copy import deepcopy
import numpy as np
import itertools
class DataPreprocessor(object):

    @staticmethod
    def standarize(X, standarization_rule = 'sensor'):
        """
        static method used for data standarization

        Args:
            X (pandas.DataFare): whole data in the form of DataFrame.
            standarization_rule (str, optional): Columns which will be standarized. Defaults to 'sensor'.

        Returns:
            pandas.DataFrame: standarized DataFrame.
        """
        data = deepcopy(X.replace(['nan'], 0))
        standarization_matrix = pd.DataFrame(np.zeros((2, len(data.columns))), index = ['std', 'mean'], columns=data.columns)
        for column_name in data.columns:
            if standarization_rule in column_name and data[column_name].std() != 0:
                standarization_matrix.loc['std', column_name] = data[column_name].std()
                standarization_matrix.loc['mean', column_name] = data[column_name].mean()
                data[column_name] = (data[column_name] - data[column_name].mean())/data[column_name].std()
            else:
                standarization_matrix.loc['std', column_name] = 1
                standarization_matrix.loc['mean', column_name] = 0
        return data, standarization_matrix

    def __init__(self, data, standarization_rule = 'sensor', tolerance=pd.Timedelta('5s'), nan_value = -1, numerical_date = True):
        """
        init function of class DataProcessor

        Args:
            data (dict): raw data taken from http request
            standarization_rule (str, optional): columns which will be standarized. Defaults to 'sensor'.
            tolerance (pd.Timedelta, optional): optional parameter for merging data from different devices, based on simmilarity in date of sending. Defaults to pd.Timedelta('5s').
            nan_value (int, optional): value which will replace NaN falues. Defaults to -1.
            numerical_date (bool, optional): if True, numerical represetation of date will be added to each row. Defaults to True.
        """
        data_dfs = [pd.DataFrame(data[key]) for key in list(data.keys())]
        for data_df_index in range(len(data_dfs)):
            data_dfs[data_df_index]['date'] = pd.to_datetime(data_dfs[data_df_index]['date'])
            data_dfs[data_df_index] = data_dfs[data_df_index].sort_values(by='date')

        for data_df_index in range(len(data_dfs[:-1])):
            data_dfs[data_df_index + 1] = pd.merge_asof(data_dfs[data_df_index], data_dfs[data_df_index + 1],
                                                                on = "date", tolerance=tolerance, direction='backward', 
                                                                suffixes = ['_' + key for key in list(data.keys())[data_df_index:data_df_index+2]]).fillna(nan_value)

        self.data_df = data_dfs[-1]
        if numerical_date == True:
            self.data_df['month']  = self.data_df['date'].dt.month
            self.data_df['day']  = self.data_df['date'].dt.day
            self.data_df['hour']  = self.data_df['date'].dt.hour
            self.data_df['minute']  = self.data_df['date'].dt.minute
            self.data_df['second']  = self.data_df['date'].dt.second
        
        data_df, standarization_matrix = self.standarize(self.data_df, standarization_rule=standarization_rule)
        self.data_df = data_df
        self.standarization_matrix = standarization_matrix

    def time_series(self, time_series_size = 3, forecast = 1, y_rule = 'device'):
        """
        Method of class DataProcessor that returns padded time series 

        Args:
            time_series_size (int, optional): parameter used for determining how many rows represent one data point. Defaults to 3.
            forecast (int, optional): value representing how many rows in the future should Y be. Defaults to 3.
            y_rule (str, optional): name of columns which will be our target. Defaults to 'device'.

        Returns:
            tuple: tuple of two dataframes, first one representing X (model input), second one Y (target).
        """
        data_dfs  = [deepcopy(self.data_df.iloc[i:-time_series_size + i].drop('date', axis = 1).reset_index(drop = True)) for i in reversed(range(time_series_size))]
        for df_index in range(len(data_dfs)):
            data_dfs[df_index].columns = [column + '_' + str(df_index) for column in data_dfs[df_index].columns]
        if forecast:
            X = pd.concat(data_dfs, axis = 1).iloc[:-forecast]
            Y = self.data_df[[column for column in self.data_df.columns if y_rule in column]].iloc[time_series_size:-forecast]
            return X, Y
        else:
            X = pd.concat(data_dfs, axis = 1)
            return X, None



class AutoTuningHyperparameters(object):
    @staticmethod
    def generate_all_possible_params(params):
        """
        Static method generationg all possible combinations of parameters.

        Args:
            params (dict): dictionary representing each parameter in the form: {'parameter name': [min value, max value, step]}.

        Returns:
            dict: all possible params.
        """
        params_unpacked = {key: list(np.arange(params[key][0], params[key][1] + params[key][2], params[key][2])) for key in                     params.keys()}
        keys, values = zip(*params_unpacked.items())
        possible_params = [dict(zip(keys, v)) for v in itertools.product(*values)]
        return possible_params

    def __init__(self, model, data, params, cost, time_series_size = 3, forecast = 3, standarization_rule = 'sensor', y_rule = 'device_blinds'):
        """
        Initialization of AutoTuningHyperparameters object. 

        Args:
            model (object): Model that will be optimized. EX. xgboost classifier.
            data (object): Whole dataset in the form of pandas dataframe. It will be splitted into train and test dataset.
            params (dict): Search space for the ml algorithm.
            cost (function): Cost function for the model, higher value means metter model (maximization).
            time_series_size (int, optional): Size of the time series. Defaults to 3.
            forecast (int, optional): How many records into the future should model look. Defaults to 3.
            standarization_rule (str, optional): Column name (partial) in the dataset that will be standatized. Defaults to 'sensor'.
            y_rule (str, optional): Column name that wil be predicted. Defaults to 'device_blinds'.
        """
        self.model = model 
        self.data_preprocessor = DataPreprocessor(data, standarization_rule=standarization_rule)
        X, y = self.data_preprocessor.time_series(time_series_size=time_series_size, forecast=forecast, y_rule = y_rule)
        self.X_train = X[:int(0.7*len(X))]
        self.X_test = X[int(0.7*len(X)):]
        self.y_train = y[:int(0.7*len(y))]
        self.y_test = y[int(0.7*len(y)):]
        self.params = params
        self.cost = cost
        self.best_model = None
    
    def fit_model(self, params):
        """
        Methods that fits provided ml model on given hyperparameters from the search space, and returns it withm its score.

        Args:
            params (dicr): hyperparameters of the model.

        Returns:
            tuple: object and its score on the test dataset.
        """
        model = self.model(**params)
        try:
            model.fit(self.X_train.to_numpy(), self.y_train.to_numpy())
            predictions = model.predict(self.X_test)
            return model, self.cost(self.y_test, predictions)
        except Exception as e:
            print(e)
            return None, 0
    
    def grid_search(self, params = None, verbose = 1):
        """
        Grid search algorithm on the provided search space.

        Args:
            params (dict, optional): Search space for the algorithm. Defaults to None.
            verbose (int, optional): Parameter defining if anything should be printed to the console. verbose>=1 -> yes, verobose < 1 - no. Defaults to 1.

        Returns:
            tuple: best found parameters and score of the model trained on them
        """
        if params:
            params = self.generate_all_possible_params(params)
        else:
            params = self.generate_all_possible_params(self.params)
        models = []
        for index, parameters in enumerate(params):
            model, ratio = self.fit_model(parameters)
            models.append([parameters, ratio])

            if verbose >= 1:
                print('{:.4f}'.format((index+1)/len(params)), end = '\r')

        sorted_models = [[x[0], x[1]] for x in sorted(models, key = lambda x: x[1])]
        self.best_model = sorted_models[-1]
        return self.best_model[0], self.best_model[1]

    def random_search(self, verbose = 1, group_size = 5, iterations = 20, params = None):
        """
        Random search algorithm on the provided search space.

        Args:
            verbose (int, optional): Parameter defining if anything should be printed to the console. verbose>=1 -> yes, verobose < 1 - no. Defaults to 1.
            group_size (int, optional): Number of random samples taken by the random searcj to compare. Defaults to 5.
            iterations (int, optional): Number of algorithm iterations. Defaults to 20.
            params ([type], optional): Search space for the algorithm. Defaults to None.

        Returns:
            tuple: best found parameters and score of the model trained on them
        """
        if params:
            params = self.generate_all_possible_params(params)
        else:
            params = self.generate_all_possible_params(self.params)

        models = []
        for iteration in range(iterations):
            random_group = np.random.choice(params, group_size)
            for random_params in random_group:
                model, ratio = self.fit_model(random_params)
                models.append([random_params, ratio])

            if verbose >= 1:
                print('{:.4f}'.format((iteration+1)/iterations), end = '\r')

        sorted_models = [[x[0], x[1]] for x in sorted(models, key = lambda x: x[1])]
        self.best_model = sorted_models[-1]
        return self.best_model[0], self.best_model[1]

    def auto_tune_pipeline(self, pipeline = ['random', 'grid'], narrow_to = 0.2, params = None):
        """
        Pipleline of algorithms given by the 'pipeline' parameter. After each search, search space is narrowed by the parameter 'narrow_to' around current best model.

        Args:
            pipeline (list, optional): List of searches that will be performed. Defaults to ['random', 'grid'].
            narrow_to (float, optional): How much the search space should be narrowed by after each iteration. Defaults to 0.2.
            params ([type], optional): Search space. Defaults to None.

        Returns:
            object: best model found after all searches
        """
        if params:
            params = params
        else:
            params = self.params
        
        possible_params_lengths = {key: len([param for param in np.arange(params[key][0], params[key][1], params[key][2])]) for key in list(params.keys())}

        for search in pipeline:
            if search == 'random':
                best_params, score = self.random_search(params = params, group_size = 5, iterations = 50)
            elif search == 'grid':
                best_params, score = self.random_search(params = params)


            for key in best_params.keys():
                key_type = type(params[key][2])
                params_length = possible_params_lengths[key]
                new_min = key_type(best_params[key] - key_type(narrow_to * params_length) * params[key][2])
                new_max = key_type(best_params[key] + key_type(narrow_to * params_length) * params[key][2])
                if new_min > params[key][0]:
                    params[key][0] = new_min
                if new_max < params[key][1]:
                    params[key][1] = new_max
            print('new search ranges for parameters: {}'.format(params))

            print('performed {} serach with max score of {} and best parameters {}'.format(search, score, best_params))
            
        return self.fit_model(best_params)  #model, score


    