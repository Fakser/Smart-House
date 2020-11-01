# Smart-house-REST-API

## Description
DODAM KIEDYŚ

## Requierments
sudo apt-get install libatlas-base-dev <br/>
Pandas <br/>
Scikit-learn <br/>
Flask <br/>
Flask-MQTT <br/>
Streamlit <br/>
plotly <br/>
apscheduler <br/>
pickle-mixin <br/>

## Windows
### Setting up new server:<br/>
$ python ./app.py --new-sensors-db --new-ml-db<br/>

### Running existing server:<br/>
$ python ./app.py<br/>

## Linux/RasberryPi

### Setting up new server:<br/>
#### Open new terminal
$ python3 ./app.py --new-sensors-db --new-ml-db<br/>

#### Open new terminal 
$ ngrok ./ngrok/ngrok authtoken 1gkVLQwMgP5rHwSOkS9CTUU1Mug_FFTqUuqCfzsJL3L5b5X5 <br/>
$ ngrok ./ngrok/ngrok http 5000<br/>

#### Open new terminal
$ streamlit run ./dashboard.py<br/>

#### Open new terminal
$ ngrok ./ngrok http 8051<br/>

### Running existing server:<br/>
#### Open new terminal
$ python3 ./app.py<br/>

#### Open new terminal 
$ ngrok ./ngrok/ngrok http 5000

#### Open new terminal
$ streamlit run ./dashboard.py<br/>

#### Open new terminal
$ ngrok ./ngrok/ngrok http 8051<br/>
