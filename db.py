import sqlite3

def create_table(name, columns, database_name = 'sensors_data.db'):
    """Function that table given by name, and columns.

    Args:
        name (string): name of the table that will be added to the database.
        columns (list): names of columns that will be added, must contain column "data". 
    Returns:
        (boolean, string): [description].
    """
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    query = 'CREATE TABLE ' + name + '( date STRING PRIMARY KEY'
    for column in columns[1:]:
        query += ', ' + column + ' STRING'
    query += ')' 
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        return False, e
    return True, "Table added successfully"

def get_column_names(name, database_name = 'sensors_data.db'):
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        print(e)
    cursor = connection.cursor()
    try:
        cursor.execute("pragma table_info('" + name + "')")
        names = cursor.fetchall()
    except Exception as e:
        return False, e    
    connection.close()
    return [name[1] for name in names], 'Success'



def select_all_from_table(name, database_name = 'sensors_data.db'):
    """Function returning all records from table given by name.

    Args:
        name (string): name of the table. 

    Returns:
        (tuple): first element of the tuple is either a bool (False), or a list. 
    """
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    try:
        data = cursor.execute("select * from " + name)
        data = cursor.fetchall()
        connection.close()
    except Exception as e:
        return False, e
    return data, "Success"

def insert_record_into_table(name , data, database_name = 'sensors_data.db'):
    """Function inserting record into table given by name.

    Args:
        name (string): name of the table.
        data (list): data record.
        database_name (str, optional): name of the databse file. Defaults to 'sensors_data.db'.

    Returns:
        (tuple): first element of the tuple is a bool, second is a message.
    """
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    query = "INSERT INTO " + name + " VALUES ("
    for record in data:
        query += "'" + str(record) + "'" + ', '
    query = query[:-2] + ')' 
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        return False, e
    return True, "Success"

def get_list_of_table_names(database_name = 'sensors_data.db'):
    """Function returning list of table names.

    Args:
        database_name (str, optional): name of the databse file. Defaults to 'sensors_data.db'.

    Returns:
        tuple: (tuple): first element of the tuple is a bool or a list of names, second is a message.
    """
    query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
    except Exception as e:
        return False, e
    return data, "Success"

def select_tail(name, n_rows = 10, database_name = 'sensors_data.db'):
    """Function returning last 'n_rows' records from the table given by 'name' 

    Args:
        name (string): name of the table
        n_rows (int, optional): Size of the tail. Defaults to 10.
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.

    Returns:
        (tuple): first element of the tuple is a bool or a list of data, second is a message.
    """
    query = "SELECT * FROM ( SELECT * FROM " + name + " ORDER BY date DESC LIMIT " + str(n_rows) +") ORDER BY date ASC"
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
    except Exception as e:
        return False, e
    return data, "Success"

def drop_table(name, database_name = 'sensors_data.db'):
    """Function that drops the table given by 'name' 

    Args:
        name (string): name of the table
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.

    Returns:
        (tuple): first element of the tuple is a bool or a list of data, second is a message.
    """
    query = 'DROP TABLE ' + name
    try:
        connection = sqlite3.connect(database_name)
    except Exception as e:
        return False, e
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        return False, e
    return True, "Success"


def query_db(query, args=(), one=False, database_name = 'sensors_data.db'):
    """New function that soon will replace all of the other functions in db.py. Performs any SQL query that user want.

    Args:
        query (string): Sql query to be executed
        args (tuple, optional): Arguments of the query. Defaults to ().
        one (bool, optional): If True, only the first parameter will be returned, else whole query result. Defaults to False.
        database_name (str, optional): Name of the database file. Defaults to 'sensors_data.db'.

    Returns:
        list: query result in the form of list
    """
    db = sqlite3.connect(database_name)
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv