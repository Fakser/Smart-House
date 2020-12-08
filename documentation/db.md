# Db

> Auto-generated documentation for [db](..\db.py) module.

- [Smart-house-rest-api](README.md#description) / [Modules](MODULES.md#smart-house-rest-api-modules) / Db
    - [create_table](#create_table)
    - [drop_table](#drop_table)
    - [get_column_names](#get_column_names)
    - [get_list_of_table_names](#get_list_of_table_names)
    - [insert_record_into_table](#insert_record_into_table)
    - [query_db](#query_db)
    - [select_all_from_table](#select_all_from_table)
    - [select_tail](#select_tail)

## create_table

[[find in source code]](..\db.py#L3)

```python
def create_table(name, columns, database_name='sensors_data.db'):
```

Function that table given by name, and columns

#### Arguments

- `name` *string* - name of the table that will be added to the database
- `columns` *list* - names of columns that will be added, must contain column "data"

#### Returns

- `(boolean,` *string)* - [description]

## drop_table

[[find in source code]](..\db.py#L115)

```python
def drop_table(name, database_name='sensors_data.db'):
```

## get_column_names

[[find in source code]](..\db.py#L29)

```python
def get_column_names(name, database_name='sensors_data.db'):
```

## get_list_of_table_names

[[find in source code]](..\db.py#L85)

```python
def get_list_of_table_names(database_name='sensors_data.db'):
```

## insert_record_into_table

[[find in source code]](..\db.py#L67)

```python
def insert_record_into_table(name, data, database_name='sensors_data.db'):
```

## query_db

[[find in source code]](..\db.py#L131)

```python
def query_db(query, args=(), one=False, database_name='sensors_data.db'):
```

## select_all_from_table

[[find in source code]](..\db.py#L45)

```python
def select_all_from_table(name, database_name='sensors_data.db'):
```

Function returning all records from table given by name

#### Arguments

- `name` *string* - name of the table

#### Returns

- `(tuple)` - first element of the tuple is either a bool (False), or a list

## select_tail

[[find in source code]](..\db.py#L100)

```python
def select_tail(name, n_rows=10, database_name='sensors_data.db'):
```
