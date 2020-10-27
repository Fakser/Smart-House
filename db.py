import sqlite3

def create_table(name, columns, database_name = 'sensors_data.db'):
    """Function that table given by name, and columns

    Args:
        name (string): name of the table that will be added to the database
        columns (list): names of columns that will be added, must contain column "data" 
    Returns:
        (boolean, string): [description]
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
    """Function returning all records from table given by name

    Args:
        name (string): name of the table 

    Returns:
        (tuple): first element of the tuple is either a bool (False), or a list 
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
    db = sqlite3.connect(database_name)
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv