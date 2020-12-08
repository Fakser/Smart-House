# App

> Auto-generated documentation for [app](..\app.py) module.

- [Smart-house-rest-api](README.md#description) / [Modules](MODULES.md#smart-house-rest-api-modules) / App
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

[[find in source code]](..\app.py#L177)

```python
@app.route('/data/<name>/<token>', methods=['DELETE'])
def delete_table(name, token):
```

## get_data

[[find in source code]](..\app.py#L151)

```python
@app.route('/data/<token>', methods=['GET'])
def get_data(token):
```

## get_model

[[find in source code]](..\app.py#L197)

```python
@app.route('/rules/<name>/<token>', methods=['GET'])
def get_model(name, token):
```

## get_models_names

[[find in source code]](..\app.py#L188)

```python
@app.route('/rules/<token>', methods=['GET'])
def get_models_names(token):
```

## get_tails

[[find in source code]](..\app.py#L164)

```python
@app.route('/data/<size>/<token>', methods=['GET'])
def get_tails(size, token):
```

## handle_mqtt_message

[[find in source code]](..\app.py#L226)

```python
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
```

## train_all_models

[[find in source code]](..\app.py#L111)

```python
def train_all_models():
```

## train_clustering

[[find in source code]](..\app.py#L134)

```python
def train_clustering():
```

## use_all_models

[[find in source code]](..\app.py#L83)

```python
def use_all_models():
```
