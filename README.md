# graphql-python
A Hacketnews project developed for the [How to GraphQL tutorial](https://www.howtographql.com/graphql-python/0-introduction/) using Python, Django and Graphene. Tested on Python 3.6.

## Installation and Usage
Clone the project.

Create a virtual environment:
```bash
python3.6 -m venv venv
source venv/bin/activate
```

Install everything needed:
```bash
pip install -r requirements.txt
```

Create the database and run the server:
```
python hackernews/manage.py migrate
python hackernews/manage.py runserver
```

You should be able to access the server on [here](http://localhost:8000/graphql).

To get the most of the project, please read the [tutorial](https://www.howtographql.com/graphql-python/0-introduction/).
