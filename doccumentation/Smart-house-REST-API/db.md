Module Smart-house-REST-API.db
==============================

Functions
---------

    
`create_table(name, columns, database_name='sensors_data.db')`
:   Function that table given by name, and columns.
    
    Args:
        name (string): name of the table that will be added to the database.
        columns (list): names of columns that will be added, must contain column "data". 
    Returns:
        (boolean, string): [description].

    
`drop_table(name, database_name='sensors_data.db')`
:   Function that drops the table given by 'name' 
    
    Args:
        name (string): name of the table
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.
    
    Returns:
        (tuple): first element of the tuple is a bool or a list of data, second is a message.

    
`get_column_names(name, database_name='sensors_data.db')`
:   

    
`get_list_of_table_names(database_name='sensors_data.db')`
:   Function returning list of table names.
    
    Args:
        database_name (str, optional): name of the databse file. Defaults to 'sensors_data.db'.
    
    Returns:
        tuple: (tuple): first element of the tuple is a bool or a list of names, second is a message.

    
`insert_record_into_table(name, data, database_name='sensors_data.db')`
:   Function inserting record into table given by name.
    
    Args:
        name (string): name of the table.
        data (list): data record.
        database_name (str, optional): name of the databse file. Defaults to 'sensors_data.db'.
    
    Returns:
        (tuple): first element of the tuple is a bool, second is a message.

    
`query_db(query, args=(), one=False, database_name='sensors_data.db')`
:   New function that soon will replace all of the other functions in db.py. Performs any SQL query that user want.
    
    Args:
        query (string): Sql query to be executed
        args (tuple, optional): Arguments of the query. Defaults to ().
        one (bool, optional): If True, only the first parameter will be returned, else whole query result. Defaults to False.
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.
    
    Returns:
        list: query result in the form of list

    
`select_all_from_table(name, database_name='sensors_data.db')`
:   Function returning all records from table given by name.
    
    Args:
        name (string): name of the table. 
    
    Returns:
        (tuple): first element of the tuple is either a bool (False), or a list.

    
`select_tail(name, n_rows=10, database_name='sensors_data.db')`
:   Function returning last 'n_rows' records from the table given by 'name' 
    
    Args:
        name (string): name of the table
        n_rows (int, optional): Size of the tail. Defaults to 10.
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.
    
    Returns:
        (tuple): first element of the tuple is a bool or a list of data, second is a message.