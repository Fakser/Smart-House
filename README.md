# Smart-house-REST-API

## Windows
### Setting up new server:<br/>
$ ./env/Scripts/activate<br/>
$ python ./env/Src/app.py --new-db<br/>

### Running existing server:<br/>
$ ./env/Scripts/activate<br/>
$ python ./env/Src/app.py<br/>

## Linux/RasberryPi

### Setting up new server:<br/>
$ source ./env/Scripts/activate<br/>
$ python3 ./env/Src/app.py --new-db<br/>

#### In new terminal 
$ ngrok ./env/Src/ngrok/ngrok authtoken 1gkVLQwMgP5rHwSOkS9CTUU1Mug_FFTqUuqCfzsJL3L5b5X5
$ ngrok ./env/Src/ngrok/ngrok http 5000


### Running existing server:<br/>
$ source ./env/Scripts/activate<br/>
$ python3 ./env/Src/app.py<br/>

#### In new terminal 
$ ngrok ./env/Src/ngrok/ngrok http 5000
