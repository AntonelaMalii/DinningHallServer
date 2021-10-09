# Network Programming - Laboratory N1 - Dinning Hall

# Network Programming 
Laboratory N1. Restaurant Simulator. Dinning Hall

## Table of contents

* [Description](#description)
* [Current Implementation](#current-implementation) 
* [Docker](#docker)
* [Technologies](#technologies)

## Description

The purpose of this laboratory work is to write a somewhat realistic simulation of how a restaurant works like.

## Current Implementation

* Initialising 2 web-servers.
* Establish http communication between them
* Initial logic of generating random orders and sending that orders to kitchen and logic of receiving the orders that should be served from kitchen.
* Initial logic of preparing foods at kitchen should be implemented. Just logic of having multiple threads picking up orders, preparing them all and returning them.
* Configuration of docker containers communication

## Docker

1.Create docker image with name (<name1>) for dinning hall server
~~~
docker build --tag <name1> 
~~~
2.Create docker communication network (<name2>) for dinning hall server and kitchen server to communicate on
~~~
docker network create <name2>
~~~
3.Create docker container for dinning hall server and run on created network
~~~
docker run -d --net name2 --name name1 name1
~~~

## Technologies

* IDE : PyCharm
* Programming language : Python 3.9
* Additional software used in project: Docker