# Table of contents

> Auto-generated documentation index.

 - [Description](#description)
   * [Data Warehouse](#data-warehouse)
   * [Server](#server)
   * [Unsupervised Machine Learning](#unsupervised-machine-learning)
   * [AutoML and Rule Induction](#automl-and-rule-induction)
   
 - [Requierments and Basic Usage](#requierments)

Full Smart-house-rest-api project documentation can be found in [Modules](MODULES.md#smart-house-rest-api-modules)

- [Table of contents](#table-of-contents)
    - [Server](#server)
    - [Unsupervised Machine Learning](#unsupervised-machine-learning)
    - [AutoML and rule induction](#automl-and-rule-induction)
    - [Linux/RasberryPi](#linuxrasberrypi)
  - [Smart-house-rest-api Modules](MODULES.md#smart-house-rest-api-modules)

# Description
![smart-house](./to_readme/smart-house.jpg)<br>
This project is my so-called bachelors. It is about creating system 
for the analysis of behavioural patterns of household members.
It means that it should be a system that can easly store IOT data from certain devices, and analyse it. For this to work i needed to create certain independent projects:
<br>

 - Dynamic data warehouse for storage of iot devices, that automaticly detects new device in the house.
 - Server in the form of rest api that handles both mqtt and http protocols.  
 - Unsupervised machine learning algorithm for analysis of behaviours of household members.
 - Auto Machine Learning pipeline and Supervised ML algorithm for the so called 'rule induction' models.
 - dashboard for visualization of IOT house data, and all ML algorithms.

You can see how it 'works' on the block diagram.<br>
![block_diagram](./to_readme/block_diagram.png)<br>
<br>

#### *NOTE: That was a joined research project. My research was based only on thestuffd listed above, that is why I DID NOT MAKE ANY IOT DEVICES, if you are interested in sensors and electronics I would recommend to contact my partner, [Jan Wróbel](https://github.com/janwrob120) with who i made the project.*
<br>

## Data Warehouse
![warehouse](./to_readme/data-warehouse-.png)<br>

Data storage appeared to be a problem from the very beginning of the project. 
Normally when you are working on a project containing a Rest API you should define your database and use it's models. For this in you can use ex. sql-alchemy. Unfortunately, my project is about iot smart house. Devices you 
use in it changes dynamicaly, that is why I needed a system that can automaticly create new table, delete them, change relations between them etc. It may sound simple, but it is something you do not implement often in web applications.<br>

### Because of that i had to implement whole database by myself in native python and sql. Yare Yare daze.<br>
![yareyare](./to_readme/yare_yare_daze.gif)<br>
I've tried my best to implement it and it works as follows. As database engine I have used sqlite as it is the simplest one to connect with python. Whenever new device is found in the house, new table in the database is created with appropriate columns. Device can contain several sensors and "usabe parts". After that each time this device will try to send anything to the world, database will add new record to the table. When device is no longer needed - table can be deleted. Also there is an option to run any SQL command from pythom with function db.query_db. Database should be somewhat save, and ressitable to simple hacking methods like SQL injection. But who knows, it still should be used only on local server.
<br>

## Server

So cool, I have a database and stuff but i need to connect to it somehow. That is why i created my RestAPI server in Flask. It uses some fancy Python stuff like:
 - Background app scheduler for scheduling tasks.
 - Previously mentioned database/data warehouse.
 - MQTT.
 - HTPP.
 - Pickle. 
 - ...and some private libraries I had to write for this projects that will be mentioned later.

Server is initialized in the form of Flask app. It connects to the mqtt broker and opens http://localhost port 5000 for connections. It operates on 3 mqtt topics: create/ data/ model/.
Each topic can have subtopics dependent on the usage. 
For now i have created 4 http requests on data/.<br>
![requests](./to_readme/requests_data.png)<br>
Thanks to that we can finnaly access the database and see how our IOT data looks like.<br>
![datarequests](./to_readme/room_jan_data.png)<br>
Nice.<br>
Also We can see that our server can connect to IOT devices with mqtt.<br>
![blinds](./to_readme/blinds.gif)<br>
On this example you can see that server connected to the blinds in the house, and closed them. Also you can spot my project partner Jan, recording the video.<br>

## Unsupervised Machine Learning

So finally i can write about the thing I am specialized in - Machine Learning.
First 'ML' part of my project was the analysis of the household members behaviours. My idea was such.<br>
### *Lets assume we have a house and at least 2 people are living in it. They have a set of "behaviours" like sleeping, eating, working, etc. We need to find an algorithm that, based on the data, can put current state of the house to the proper container, or so-called "behaviour".* <br>

This was a cool idea but we have a problem already. Not every human has the same set of behaviurs. That is why we need an algorithm that can firstly create this set of behaviours, and then be able to properly classify each moment in time with it. Fortunately there is a solution perfect for us. The K-Means algorithm.<br>
![blinds](./to_readme/kmeans1.png)<br>
yeah cool, it just works. And i have implemented it by myself in python using only native libraries like math and numpy for no normal reason.

But does it?
### It turns out that clustering is based on some CRAZY MATHEMATICS like simple mean<br>
![picsimplemean](./to_readme/simplestats.png)<br>
### and geometric distance between two points<br>
![picdistance](./to_readme/distance.png)<br>
### Algorithm first chooses some random points witch are called "centroids", which are centers of now empty clusters. Then for each point distance to all centroids is calculated, and the one closest to this point is choosen. After clustering each point to currently random cluster, new centroind is choosen from all points in the cluster by usage of simple mean on all of them.<br>

####  You still here?<br>
![epicmeme](./to_readme/epicmeme.jpg)<br>

### I performed simple experiment to check if my K-Means works.
### Here, data<br>
![pic1](./to_readme/Adnotacja-2020-09-07-201438.png)<br>

### And now clustered<br>
![pic2](./to_readme/Adnotacja-2020-09-07-201500.png)<br>

So yeah it works, nothing to add here.
<br>

## AutoML and rule induction

Another thing that i needed to create for my project was a rule induction algorithm. It is used to create certain AI for devices in the house, so that human no longer needs to use them, house will do everything automaticly. First i needed to choose my ML algorithm that will be trained for each device. And i have choosen Decision Trees.
<br>
Decision Trees are probably easiest to understand with real example. Let's say you want to loose weight.
![pic2](./to_readme/dig10.PNG)<br>
We start from the top of the "tree". Im under 30 so we go with the first choice "Yes". Also I am not eating pizza so second choice is "No". Oh nice i am fit, I don't have to loose weigth anymore.<br>
Unfortunately Decision trees are Supervised ML algorithm. And such algorithms have *HYPER PARAMETERS*. Of course I could use some predefined parameters and call it a day. But i was bored and I have written my own Auto ML framework, that can chooce 'perfect' hyper parameters for our supervised ml model.<br>
It works as such:
 - randomly chooses a set of hyper parametrs from all possible parametrs
 - chooses best random candidate
 - performs grid search around our random candidate

I also had an idea for genetic algorithm which chooses best parameters, but such algorithms in the case of automl tends to converge slower than random->grid search approach. <br>
Creating my own auto ml framework may sound like an overkill, but it gave me some knowledge it the field, which (what can I say) is pretty profitable, and currently there are not so many solutions for that industrially.
![pic2](./to_readme/google_automl.jpg)<br>

<br>

# Requierments
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
