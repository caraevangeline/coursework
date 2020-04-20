# Cloud Computing Mini-Project


Mini Project on REST services. The following functionalities are performed 

  - Spotify API is used to process various requests and OAuth 2.0 authentication is used to obtain the access_token of the user
  - The data obtained from spotify is displayed in a neatly formatted HTML webpage 
  - The Spotify API requests are served over HTTPS
  - Data is downloaded from Spotify API in json format and converted to csv format and the converted data is copied to cassandra database
  - GET, POST, PUT and DELETE requests are processed on the data stored in cassandra
  - Docker image is built for the above mentioned services
  - Kubertnetes is used for load-balancing.

### SPOTIFY API

  - GET the details of user's currently_playing track
  - GET the cover_image of user specified playlist
  - GET the recommendation of genres for the user
  - POST- Create playlist for the user
  - POST- Add tracks to the user's specified playlist
  - PUT- Save a particular album
  - DELETE - Unfollow an artist
  
 **Note: Every requests has a scope which the user must give permission to.

### Processing requests for Spotify API 
  - Using https://developer.spotify.com/documentation/web-api/reference-beta/ get the access_token for the above mentioned requests where you need to choose the scope required and get the access_token. The user(ie. in this case I am the user) will be redirected to a webpage where she needs to grant permission.
  - programs/app.py contains all the above mentioned requests.
  - Once the request is processed succesfully, you will be redirected to a webpage.
  - GET requests leads to HTML webpages -- programs/templates/.. contains the HTML files.
  - PUT, POST and DELETE requests are processed via GET requests explicitly and they show a success message.
  - app.run(host='0.0.0.0', ssl_context='adhoc') is used to run the Flask application where 'adhoc' certificates are used to run the app over HTTPS.


  Once you login into amazon EC2 t2.medium instance
  ```sh
  $ sudo apt update
  $ sudo apt install python3-pip
  $ pip3 install Flask
  $ pip3 install requests
  $ pip3 install pyopenssl
  $ cd coursework
  $ cd programs
  $ python3 app.py
  ```
 
 
  Go to https://ec2-54-172-5-180.compute-1.amazonaws.com/{..} to observe the outputs of the created app. Below are the urls of requests served.
 - currently_playing - To get the details of the currently_playing track
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig1.jpg)
 - cover_image/<play_id> - To get the cover image of a given playlist
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig2.png)
 - recommendations - To get the genre recommendations for the user
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig3.jpg)
 - create_playlist/<user_id> - Create a playlist for the user (user_id)
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig4.png)
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig13.jpg)
 - add_tracks/<playlist_id> - Add tracks to playlist_id
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig5.png)
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig14.jpg)
 - save_album/<album_id> - Save album with id = album_id to the user's account
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig6.png)
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig15.jpg)
 - unfollow_artist/<artist_id> - Unfollow the artist with id = artist_id
 ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig7.png)
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig16.jpg)
  
### Create database for cassandra
 
- programs/database.py contains the code to retrieve the songs, realease_date and spotify uri of 4 albums [sums upto 195 rows of record with 4 columns] and the output csv file is saved in spotify.csv
```sh
$ cd programs
$ python3 database.py
```
### Store data to Cassandra
- Pull the latest version of cassandra docker image
- Run a Cassandra instance with docker
- Create a keyspace
- Create the table and copy the database obtained from previous step.
```sh
$ cd programs
$ sudo apt install docker.io
$ sudo docker pull cassandra:latest
$ sudo docker run --name coursework -p 9042:9042 -d cassandra:latest
$ sudo docker cp spotify.csv coursework:/home/spotify.csv
$ sudo docker exec -it coursework cqlsh
cqlsh>CREATE KEYSPACE spotify WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
cqlsh>CREATE TABLE spotify.statistics (artist text,song text PRIMARY KEY, 
 .....date text,uri text);
cqlsh>COPY spotify.statistics(artist,song,date,uri)
 .....FROM '/home/spotify.csv'
 .....WITH DELIMITER=',' AND HEADER=FALSE;
 cqlsh>exit
```
commands.txt contains the required commands and queries .

### Process requests for Cassandra
- GET request to get the album to which a particular song belongs to.
- POST to insert a row with given attributes
- PUT to update artist name for a particular song
- DELETE to delete a record from the database

programs/cw1.py contains the combined code to process both cassandra database requests and Spotify API requests.
  ```sh
 $ sudo docker inspect coursework
  ```
  Use the above command to look for the ip-address and make the corresponding changes in cw1.py in line 4.
  programs/requirements.txt contains the packages that are supposed to be installed while building our image and programs/Dockerfile contains the necessary commands to assemble our image.
   ```sh
   $ sudo docker build . --tag=cassandrarest:v1
   $ sudo docker run -p 80:80 cassandrarest:v1
   ```
 
  The above commands are to build our image and to run the requests desired. 
  - To see the GET request open https://ec2-54-172-5-180.compute-1.amazonaws.com/spotify_display/<song_name>
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig8.png) 
  - To process POST, type the below command in another terminal
  ```sh
   $ curl -i -H "Content-Type: application/json" -X POST -d '{"song":"Ha_cara1","artist":"cara","date":"10-10-2020","uri":"spotify:album:cara"}' http://ec2-54-172-5-180.compute-1.amazonaws.com/spotify_create
   ```
   ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig9.jpg)
  - To process PUT, give the below command from another terminal
   ```sh
   $ curl -X "PUT" http://ec2-54-172-5-180.compute-1.amazonaws.com/spotify_update/Ha_cara
   ```
   ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig11.jpg)
   - For DELETE,
   ```sh
   $ curl -X "DELETE" http://ec2-54-172-5-180.compute-1.amazonaws.com/spotify_delete/Ha_cara
   ```
   ![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig10.jpg)
 ### Kubertnetes for load balancing


> Containers are a good way to bundle and run your applications. In a production environment, you need to manage the containers that run the applications and ensure that there is no downtime. For example, if a container goes down, another container needs to start. Wouldn’t it be easier if this behavior was handled by a system?
That’s how Kubernetes comes to the rescue! Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more. 

Below commands are to install microk8s to run kubernetes and to check status
```sh
$ sudo snap install microk8s --classic
$ sudo microk8s.status
$ sudo microk8s.kubectl get nodes
$ sudo snap alias microk8s.kubectl kubectl
$ sudo kubectl get nodes
$ sudo snap list
```
To create deployment.apps, pods and to do scaling and to expose app to external ip below are the commands 
```sh
$ sudo kubectl create deployment coursework --image=cassandrarest:v1
$ sudo kubectl run coursework --image=cassandrarest:v1 --port=80
$ sudo kubectl scale deployment coursework --replicas=3
$ sudo kubectl expose deployment coursework --type=LoadBalancer --name=coursework --port=80
$ sudo kubectl patch service coursework -p '{"spec": {"type": "LoadBalancer", "externalIPs":["54.172.5.180"]}}'
```
![Image](https://raw.githubusercontent.com/caraevangeline/coursework/master/images/Fig12.png)

To view or delete Deployment
```sh
$ sudo kubectl get all
$ sudo kubectl delete deployment.apps/coursework
$ sudo kubectl delete pod/coursework
$ sudo kubectl delete service/coursework
```







 









License
----

@caraevangeline


**Cloud Computing Mini-Project - Done!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
