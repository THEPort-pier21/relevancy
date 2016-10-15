# relevancy
relevancy api

To Run:

`pip install -r requirements.txt`

call:

`curl -H "Content-Type: application/json" -X POST -d '{"something":"asfd"}' http://127.0.0.1:5000/article`


expected response:

  ```
  {
  "article": {
    "something": "asfd"
  },
  "relevancy": false
}

```

on heroku

call:

`curl -H "Content-Type: application/json" -X POST -d '{"something":"asfd"}' http://pier21.herokuapp.com/article`
