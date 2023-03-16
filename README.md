# USER BACKEND SERIVE FOR A1 (TEST)
This projects contains 2 features:
* backend API for CRUID operations with users
* fetching user's info from external resourse

## INSTALLATION
The only thing that required is docker and docker-compose.

For building all dependencies in docker just run `./initialize.bash`

## EXECUTION
To start backend API run `./run_api.bash`

To start fetch script run `./fetch_users.bash`

To reset database state re-run `./initialize.bash`


## BACKEND API
After you hit `./run_api.bash` all endpoints will be available at [http://127.0.0.1](http://127.0.0.1), like [http://127.0.0.1/users](http://127.0.0.1/users)

### ENDPOINTS
List of available backend endpoints:
* GET `/users` - get list all users in database
* GET `/users/{user_id}` - get specific user from database
* PATCH `/users/{user_id}` - update user's info. It's allowed to provide not all fields for update
* POST `/users/create` - create new user
* DELETE `/users/{user_id}` - delete specific user

### DOCS
Docs can be found at [http://127.0.0.1/docs](http://127.0.0.1/docs) or [http://127.0.0.1/redoc](http://127.0.0.1/redoc)

### PGADMIN
PgAdmin is attached at [http://127.0.0.1:5050](http://127.0.0.1:5050), credentials are:
* username/email: `pgadmin4@pgadmin.org`
* password: `admin`

You should register new database with such info:
* host name: `db`
* maintance database: `a1-users`
* username: `postgres`
* password: `postgres`


## FETCHING USERS FROM EXTERNAL RESOURCE
Users are fetched from [https://randomuser.me/api](https://randomuser.me/api)

Default users fetch count are 100, count of async workers are 5. This could be customized via args:

`docker-compose run a1-users-app python3 -m app.scripts.fetch_users 10 1` - this will fetch 10 users via 1 worker
