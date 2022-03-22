# kilola-beta

Django app for the kilola platform

## Setup Instructions

To build this project, first make sure you have docker and compose installed and then
add the following two configuration files:

[/kilola/email_credentials.py](/kilola/email_credentials.py)

Example Content:

```py
port = 25
host = 'smtp.somedomain.com'
user = 'user@example.com'
password = 'some smtp user password'
```

[/kilola/server_credentials.py](/kilola/server_credentials.py)

Example content:

```py
hash_key = 'some complicated hach key'
```

and finally run
```
docker-compose up
```

## Links

| Link | Description |
|------|-------------|
|[https://kilola-beta.portacode.com/admin](https://kilola-beta.portacode.com/admin) | Django Admin |
|[https://kilola-beta.portacode.com/api/v1](https://kilola-beta.portacode.com/api/v1) | RESTFul API root URL |
|[https://kilola-beta.portacode.com/api/v1/swagger/](https://kilola-beta.portacode.com/api/v1/swagger/) | Auto generated swagger ui for the API |
|[https://kilola-beta.portacode.com/api/v1/redoc/](https://kilola-beta.portacode.com/api/v1/redoc/) | Auto generated redoc ui for the API |
|[kilola-ui.pages.dev](https://kilola-ui.pages.dev/terms) | That's where the ReactJS client side is deployed |
|[github.com/meena-erian/kilola-beta](https://github.com/meena-erian/kilola-beta) | The location of this replository |
|[github.com/meena-erian/kilola-ui](https://github.com/meena-erian/kilola-ui) | The location of the repository for the ReactJS Client app |