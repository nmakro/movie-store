# A minimal restful application that simulates an online movie-store.

## Features
 - list movies using `GET`: endpoint api/v1/movies
 - search movies using `GET`: endpoint api/v1/movies/search and using the genre parameter to find movies in a specified category.
 - get the details of a movie by id using `GET`: endpoint api/v1/movies/\<int:movie_id>
 - update the details of a movie using `PATCH`: endpoint api/v1/movies/\<int:movie_id> use genre, title, year or director params to update the relative fields.
 - create a movie using `POST`: endpoint api/v1/movies use the above parameters and also title and director are mandatory.
 - delete a movie using `DELETE`: endpoint api/v1/movies/\<int:movie_id>
 
 - list categories using `GET`: endpoint api/v1/categories to view all available categories. If genre param is specified all movies under that category will be also listed. 
   If genre equals 'all', then all movies will be listed under their category.
 - create a new category using `POST`: endpoint api/v1/categories. You must specify the genre param for a successful creation.
 - delete a new category using `DELETE`: endpoint api/v1/categories. You must specify the genre or the id param for a successful deletion.
 
 - rent a movie using using `POST`: endpoint api/v1/rent. You must specify the id of the movie using the movie_id param.
 - list your orders using `GET`: endpoint api/v1/orders
 - pay a movie that was previously rent using `POST`: endpoint api/v1/pay. You must specify the order id and the amount to pay using the order_id and amount params.
   If the amount is less than the order's charge the payment will fail.
  
  - view all available info for the user using `GET`: endpoint api/v1/home/
 
 - login to gain access to the service by using the available users specified in the basic auth configuration.
 - all actions that create, modify or delete are using authorization rules.
 - data related to the user like orders, and info about a specific user require also authorization from the user or the admin.
 - only the admin user can modify movies, categories and orders.
 - click [here](https://github.com/nmakro/movie-store/blob/master/app/api/auth.py#L6) to see the current available users.
 - all list actions support pagination using the page/per_page params, defaulting to 1 and 4.
 - a database with some initial setup is provided [here](https://github.com/nmakro/movie-store/blob/master/app/app.db)
  
## Use
  example usage:
  search all movies by category:drama
  http://127.0.0.1:5000/api/v1/movies/search?genre=drama
  
  ```json
  {
  "_meta": {
    "next": "/api/v1/movies/?page=2&genre=drama", 
    "prev": null
  }, 
  "movies": [
    {
      "director": "Lumet", 
      "genre": [
        "drama"
      ], 
      "id": 4, 
      "title": "12 Angry Men", 
      "year": "1957"
    }, 
    {
      "director": "David Fincher", 
      "genre": [
        "drama"
      ], 
      "id": 6, 
      "title": "Fight Club", 
      "year": "1999"
    }, 
    {
      "director": "Robert Zemeckis", 
      "genre": [
        "drama"
      ], 
      "id": 7, 
      "title": "Forrest Gump", 
      "year": "1994"
    }, 
    {
      "director": "Martin Scorsese", 
      "genre": [
        "crime", 
        "drama"
      ], 
      "id": 10, 
      "title": "Goodfellas", 
      "year": "1990"
    }
  ]
}
```


## Install

### Get the app

 - $ `git clone https://github.com/nmakro/movie-store.git`


### Build the container

$ `docker build -t movie-store:latest .`

### Run the application
$ `docker-compose up`

