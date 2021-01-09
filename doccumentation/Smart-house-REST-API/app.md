Module Smart-house-REST-API.app
===============================

Functions
---------

    
`delete_table(name, token)`
:   Flask app DELETE request that delets whole database table given by name
    Endpoint data/
    
    Args:
        name (string): name of the database table that will be dropped
        token (string): API token
    
    Returns:
        string: message

    
`get_data(token)`
:   Flask app GET request that returns all data stored in the database
    Endpoint data/    
    
    Args:
        token (string): API token
    
    Returns:
        string: jsonified database content in the form of string

    
`get_model(name, token)`
:   Flask app GET request that returns parameters of a ml model given by its name
    Endpoint rules/
    Args:
        name (string): name of a ml model
        token (string): API token
    
    Returns:
        string: jsonified ml model in the form of string

    
`get_models_names(token)`
:   Flask app GET request that returns all ml model names
    Endpoint rules/
    Args:
        token (string): API token
    
    Returns:
        string: jsonified names of ml models in the form of string

    
`get_tails(size, token)`
:   Flask app GET request that returns last data stored in the database.
    Number of records is specified by parameter size
    Endpoint data/
    
    Args:
        size (string): size of returned data/numer of last records
        token (string): API token
    
    Returns:
        string: jsonified database content in the form of string

    
`train_all_models()`
:   Scheduled function that trains ml models for all available devices.

    
`train_clustering()`
:   Scheduled function that fits clustering algorithm

    
`use_all_models()`
:   Scheduled function that uses all available ml models on the previous records from database