# App

> Auto-generated documentation for [app](..\app.py) module.

- [Smart-house-rest-api](README.md#table-of-contents) / [Modules](MODULES.md#smart-house-rest-api-modules) / App
    - [delete_table](#delete_table)
    - [get_data](#get_data)
    - [get_model](#get_model)
    - [get_models_names](#get_models_names)
    - [get_tails](#get_tails)
    - [handle_mqtt_message](#handle_mqtt_message)
    - [train_all_models](#train_all_models)
    - [train_clustering](#train_clustering)
    - [use_all_models](#use_all_models)

#### Attributes

- `app` - app and scheduler: `Flask(__name__)`

## delete_table

[[find in source code]](..\app.py#L208)

```python
@app.route('/data/<name>/<token>', methods=['DELETE'])
def delete_table(name, token):
```

Flask app DELETE request that delets whole database table given by name
Endpoint data/

#### Arguments

- `name` *string* - name of the database table that will be dropped
- `token` *string* - API token

#### Returns

- `string` - message

## get_data

[[find in source code]](..\app.py#L160)

```python
@app.route('/data/<token>', methods=['GET'])
def get_data(token):
```

Flask app GET request that returns all data stored in the database
Endpoint data/

#### Arguments

- `token` *string* - API token

#### Returns

- `string` - jsonified database content in the form of string

## get_model

[[find in source code]](..\app.py#L248)

```python
@app.route('/rules/<name>/<token>', methods=['GET'])
def get_model(name, token):
```

Flask app GET request that returns parameters of a ml model given by its name
Endpoint rules/

#### Arguments

- `name` *string* - name of a ml model
- `token` *string* - API token

#### Returns

- `string` - jsonified ml model in the form of string

## get_models_names

[[find in source code]](..\app.py#L230)

```python
@app.route('/rules/<token>', methods=['GET'])
def get_models_names(token):
```

Flask app GET request that returns all ml model names
Endpoint rules/

#### Arguments

- `token` *string* - API token

#### Returns

- `string` - jsonified names of ml models in the form of string

## get_tails

[[find in source code]](..\app.py#L183)

```python
@app.route('/data/<size>/<token>', methods=['GET'])
def get_tails(size, token):
```

Flask app GET request that returns last data stored in the database.
Number of records is specified by parameter size
Endpoint data/

#### Arguments

- `size` *string* - size of returned data/numer of last records
- `token` *string* - API token

#### Returns

- `string` - jsonified database content in the form of string

## handle_mqtt_message

[[find in source code]](..\app.py#L287)

```python
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
```

MQTT message handler. depending on the topic, performs different operations:
 - control/ - pass
 - data/ - adds new record to the database table given by the name in the topic 'data/<name>', if table was not found creates it.
           Record data is provided in message payload
 - model/ - changes parameters of a ml model given by the name in the topic 'models/<name>', changable parametrs: trainable ["false", "true"], use ["false", "true"]

#### Arguments

- `client` *string* - client of the mqtt
- `userdata` *string* - data on the user
- `message` *object* - whole message that can be unpacked into message.payload and message.topic

## train_all_models

[[find in source code]](..\app.py#L114)

```python
def train_all_models():
```

Scheduled function that trains ml models for all available devices.

## train_clustering

[[find in source code]](..\app.py#L140)

```python
def train_clustering():
```

Scheduled function that fits clustering algorithm

## use_all_models

[[find in source code]](..\app.py#L83)

```python
def use_all_models():
```

Scheduled function that uses all available ml models on the previous records from database
