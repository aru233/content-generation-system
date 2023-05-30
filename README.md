# feedRenderer App
###### A REST API that returns the feed content for a user, built with Django and Redis
- The user can send a request to fetch their feed. 
- A central API gateway will receive requests from the clients and return a list of posts to be shown in their home feed.
- Redis is being as the backend server to store the feed (key-value store). 
It's chosen for the purpose of demonstration of how the app would react with a dao layer.
- In the current scope, the database has a pre-populated list of posts corresponding to each user. 
This can be extended to a larger scope- with recommendation algorithms working to generate recommendations for a user's feed and selecting the top recommendations to be shown to the user.


The flow of requests and data is across 3 components/layers
- views.py: it receieves the requests from the users and relays the request to the controller.py layer
- controller.py: it is the intermediary between the user facing layer and the DAO layer. It receives requests from views.py, does the required data processing (holds the business logic), and coordinates with the DAO layer to do CRUD operations on the database
- repo.py: the DAO layer. Its responsible for all operations related to the database


## Installation Instructions
Run the following commands inside the cloned repository 

We’re going to do all the setup etc inside a virtual environment.

### Create virtual environment
```
python3 -m venv <name_of_environment>
```

### Activate the virtual environment
```
source <name_of_environment>/bin/activate
```

### Install the required packages from requirements.txt
```
pip install -r requirements.txt
```
    Main installations needed:
    Install Django inside this virtual environment
    python3 -m pip install Django

    Install Redis inside the venv
    python3 -m pip install redis

    Start redis server
    redis-server

    Check if Redis is up and accepting connections:
    $ redis-cli ping
    PONG

    pip install django djangorestframework redis


### We need to have 2 processes running in 2 different terminals
(inside the virtual environment)

   Django app server
   
    python manage.py runserver
    
   Redis server
   
    redis-server

Open your web browser and go to http://localhost:8000 to view the app.

## Tech Stack
- Python/Django
    - Framework used to create the app
- Redis
    - The database

## API Endpoints

### Send request to view the feed
**Endpoint**: `feed/`

**URL**: `http://127.0.0.1:8000/feed/`

(assuming localserver for the purpose of this task)

**Method**: POST

**Query Params**:
Name | Description
--- | --- 
user-id | Id for the user 
timestamp | Most recent timestamp till which the user has viewed the feed 

**Response**:
A list of posts; each post is a dictionary, with following fields:
Name | Description
--- | --- 
id |  The post id
title | Title of the post
content | The description (or caption in case of an instagram post)
imageUri | The URI of the image associated with the post
created_at | Timestamp at which the post was created


### The home page of the app
**Endpoint**: ``

**URL**: `http://127.0.0.1:8000`

(assuming localserver for the purpose of this task)

**Method**: GET

**Response**:
A basic welcome message

When the user hits the home page, the database gets populated with a test list of pre-generated posts for a test user=1


<hr>


# contentGenerator App

###### A content generation REST API, built with Django, Redis and Celery
- The user can send a request to generate either text or image or an instagram post based on the entered text prompt. 
- A central API gateway will receive requests from clients and route them to the appropriate worker.
- We have identified two different types of workers- Text Workers and Image Workers.
- Message Queue and sqlite Database have been used. 
A message queue ensures that the requests are processed in order and to prevent overload of the AI models. 
The database is being used to store the generated content and metadata associated with it.
- Currently, there is no actual AI model involved in the text or image generation. In a real-world application, the AI models would be integrated into the text and image worker services to provide actual generated content

## Installation Instructions
Run the following commands inside the cloned repository 

We’re going to do all the setup etc inside a virtual environment.

### Create virtual environment
```
python3 -m venv <name_of_environment>
```

### Activate the virtual environment
```
source <name_of_environment>/bin/activate
```

### Database setup
```
python manage.py makemigrations
python manage.py migrate
```

### Install the required packages from requirements.txt
```
pip install -r requirements.txt
```
    Main installations needed:
    Install Django inside this virtual environment
    python3 -m pip install Django

    Install Redis inside the venv
    python3 -m pip install redis

    Start redis server
    redis-server

    Check if Redis is up and accepting connections:
    $ redis-cli ping
    PONG

    Celery setup
    pip install redis django-celery-beat django-celery-results python-decouple


### We need to have 3 processes running in 3 different terminals
(inside the virtual environment)

   Django app server
   
    python manage.py runserver
    
   Redis server
   
    redis-server
    
   Celery worker
   
    python -m celery -A contentGen worker
    
   [celery is the CLI command,
   -A references the django configuration folder,
   contentGen where celery.py lives (the Django project folder)
   worker means our task offloader is running]

Open your web browser and go to http://localhost:8000 to view the app.

## Tech Stack
- Python/Django
    - Framework used to create the app
- Celery
    - Celery is a task queue/worker framework. It allows you to offload CPU-intensive or time-consuming tasks from your main application to a separate process or machine. This can improve the performance of your application by freeing up resources for other tasks.
    Celery is often used in conjunction with a message broker, such as RabbitMQ or Redis. The message broker is responsible for delivering tasks to workers and collecting their results.
- Redis
    - The message broker

## API Endpoints

### Send request for content generation
**Endpoint**: `content/`

**Method**: POST

**Query Params**:
Name | Description
--- | --- 
prompt | The text string given as input by the user 
tag | String; it can be "text", "image" or "instagram" depending on whether the user wants to generate text or image or both text and image.

**Response**:
Name | Description
--- | --- 
message |  "Hello! Your content is being generated. Use the request id to know status"
RequestId | The unique id of the request made by the user; this id will be used to view the generated content once available 

### View the response of the generated content
**Endpoint**: `content/view/`

**Method**: POST

**Query Params**:
Name | Description
--- | --- 
request-id | The unique id of the request

**Response**:
Name | Description
--- | --- 
status | Indicating whether response is available or not. If it's not available, the user can try again;
text | The generated text (if tag="text" or tag="instagram") 
imageUri | The URI of the generated image (if tag="image" or tag="instagram")
error | Error message in case of Bad Request


### Endpoints for internal use
**Endpoint**: `worker/text`
**Endpoint**: `worker/image`

These are used internally by the Redis queue worker, to call the text generation worker and image generation worker respectively, while processing the request from the queue.

## Design Decisions
- The API has been designed to be asynchronous. The API server puts the requests in the queue that get handled by workers asynchronously. This allows the API server to be available to serve other incoming requests, without the user having to wait.
The image and text workers will need to run in background outside of the request processing scope (based on assumption that it’ll be a long processing time). In this case, we have to pull the relevant data together and render a compiled response, which can be a time-consuming process, often better performed asynchronously.
- The workers have been simulated in the form of API endpoints; this has been done to represent the idea that they can be independently scaled- we can increase or decrease the number of workers depending on the user load, geographical spread of request, time taken by the AI model to generate content etc.
A load balancer can be used to distribute the requests between the text worker and image worker services based on their availability.
- Redis + Celery have been used as task queue. Celery, along with message broker like Redis,  allows to offload CPU-intensive or time-consuming tasks from your main application to a separate process or machine. It's is a powerful tool that can be used to improve the performance and scalability of the application. 
The use of a task queue also allows the communications between two servers in real-time application, depending on our scalability and availability requirements.
- In the interest of time, the response of the contentGeneration API is available at the `content/view/` endpoint. The user will hit this endpoint to check if response is available and view the response if it is. Else, they can try after sometime. There are different mechanisms to handle this workflow, like Polling, Webhooks, Websockets etc where the response can asynchronously be made available to the user. 
This endpoint could work with frontend to show a loading sign to the user while the response is not available and return the response as soon as it is available.
- Celery comes with task workers that process requests from queue. The logic for calling workers, receiving response from them, persisting the response in the database sits with the queue task workers. 
The system can easily be scaled and be made more robust; like the text and image generation requests can be distributed and processed in parallel by the text worker and image worker services.

# contentGenerator App

###### A content generation REST API, built with Django, Redis and Celery
- The user can send a request to generate either text or image or an instagram post based on the entered text prompt. 
- A central API gateway will receive requests from clients and route them to the appropriate worker.
- We have identified two different types of workers- Text Workers and Image Workers.
- Message Queue and sqlite Database have been used. 
A message queue ensures that the requests are processed in order and to prevent overload of the AI models. 
The database is being used to store the generated content and metadata associated with it.
- Currently, there is no actual AI model involved in the text or image generation. In a real-world application, the AI models would be integrated into the text and image worker services to provide actual generated content

## Installation Instructions
Run following commands inside the cloned repository 

We’re going to do all the setup etc inside the virtual environment.

# Create virtual environment
```
python3 -m venv <name_of_environment>
```

# Activate the virtual environment
```
source <name_of_environment>/bin/activate
```

# Database setup
```
python manage.py makemigrations
python manage.py migrate
```

# Install the required packages from requirements.txt
```
pip install -r requirements.txt
```
    Main installations needed:
    Install Django inside this virtual environment
    python3 -m pip install Django

    Install Redis inside the venv
    python3 -m pip install redis

    Start redis server
    redis-server

    Check if Redis is up and accepting connections:
    $ redis-cli ping
    PONG

    Celery setup
    pip install redis django-celery-beat django-celery-results python-decouple


### We need to have 3 processes running in 3 different terminals
(inside the virtual environment)

   Django app server
   
    python manage.py runserver
    
   Redis server
   
    redis-server
    
   Celery worker
   
    python -m celery -A contentGen worker
    
   [celery is the CLI command,
   -A references the django configuration folder,
   contentGen where celery.py lives (the Django project folder)
   worker means our task offloader is running]

Open your web browser and go to http://localhost:8000 to view the app.

## Tech Stack
- Python/Django
    - Framework used to create the app
- Celery
    - Celery is a task queue/worker framework. It allows you to offload CPU-intensive or time-consuming tasks from your main application to a separate process or machine. This can improve the performance of your application by freeing up resources for other tasks.
    Celery is often used in conjunction with a message broker, such as RabbitMQ or Redis. The message broker is responsible for delivering tasks to workers and collecting their results.
- Redis
    - The message broker

## API Endpoints

### Send request for content generation
**Endpoint**: `content/`

**Method**: POST

**Query Params**:
Name | Description
--- | --- 
prompt | The text string given as input by the user 
tag | String; it can be "text", "image" or "instagram" depending on whether the user wants to generate text or image or both text and image.

**Response**:
Name | Description
--- | --- 
message |  "Hello! Your content is being generated. Use the request id to know status"
RequestId | The unique id of the request made by the user; this id will be used to view the generated content once available 

### View the response of the generated content
**Endpoint**: `content/view/`

**Method**: POST

**Query Params**:
Name | Description
--- | --- 
request-id | The unique id of the request

**Response**:
Name | Description
--- | --- 
status | Indicating whether response is available or not. If it's not available, the user can try again;
text | The generated text (if tag="text" or tag="instagram") 
imageUri | The URI of the generated image (if tag="image" or tag="instagram")
error | Error message in case of Bad Request


### Endpoints for internal use
**Endpoint**: `worker/text`
**Endpoint**: `worker/image`

These are used internally by the Redis queue worker, to call the text generation worker and image generation worker respectively, while processing the request from the queue.

## Design Decisions
- The API has been designed to be asynchronous. The API server puts the requests in the queue that get handled by workers asynchronously. This allows the API server to be available to serve other incoming requests, without the user having to wait.
The image and text workers will need to run in background outside of the request processing scope (based on assumption that it’ll be a long processing time). In this case, we have to pull the relevant data together and render a compiled response, which can be a time-consuming process, often better performed asynchronously.
- The workers have been simulated in the form of API endpoints; this has been done to represent the idea that they can be independently scaled- we can increase or decrease the number of workers depending on the user load, geographical spread of request, time taken by the AI model to generate content etc.
A load balancer can be used to distribute the requests between the text worker and image worker services based on their availability.
- Redis + Celery have been used as task queue. Celery, along with message broker like Redis,  allows to offload CPU-intensive or time-consuming tasks from your main application to a separate process or machine. It's is a powerful tool that can be used to improve the performance and scalability of the application. 
The use of a task queue also allows the communications between two servers in real-time application, depending on our scalability and availability requirements.
- In the interest of time, the response of the contentGeneration API is available at the `content/view/` endpoint. The user will hit this endpoint to check if response is available and view the response if it is. Else, they can try after sometime. There are different mechanisms to handle this workflow, like Polling, Webhooks, Websockets etc where the response can asynchronously be made available to the user. 
This endpoint could work with frontend to show a loading sign to the user while the response is not available and return the response as soon as it is available.
- Celery comes with task workers that process requests from queue. The logic for calling workers, receiving response from them, persisting the response in the database sits with the queue task workers. 
The system can easily be scaled and be made more robust; like the text and image generation requests can be distributed and processed in parallel by the text worker and image worker services.

