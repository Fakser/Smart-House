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
#### Open new terminal
$ source ./env/Scripts/activate<br/>
$ python3 ./env/Src/app.py --new-db<br/>

#### Open new terminal 
$ ngrok ./env/Src/ngrok/ngrok authtoken 1gkVLQwMgP5rHwSOkS9CTUU1Mug_FFTqUuqCfzsJL3L5b5X5 <br/>
$ ngrok ./env/Src/ngrok/ngrok http 5000<br/>

#### Open new terminal
$ streamlit run ./env/Src/dashboard.py<br/>

#### Open new terminal
$ ngrok ./env/Src/ngrok/ngrok http 8051<br/>

### Running existing server:<br/>
#### Open new terminal
$ source ./env/Scripts/activate<br/>
$ python3 ./env/Src/app.py<br/>

#### Open new terminal 
$ ngrok ./env/Src/ngrok/ngrok http 5000

#### Open new terminal
$ streamlit run ./env/Src/dashboard.py<br/>

#### Open new terminal
$ ngrok ./env/Src/ngrok/ngrok http 8051<br/>