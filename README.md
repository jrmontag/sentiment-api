# Sentiment API, run three ways

A simple text sentiment API. 

Clone and enter the repo, then run it...

### ... locally with `uv` 

1. install `uv` [first](https://docs.astral.sh/uv/getting-started/installation/)

```shell
make local-dev
```

### ... locally with Docker

1. install Docker [first](https://docs.docker.com/get-started/get-docker/) 

```shell
make docker-run
```

### ... deployed to Fly.io

1. install `flyctl` [first](https://fly.io/docs/getting-started/)
2. create a Fly account
3. (Probably?) Change the `app` name in `fly.toml` to something unique

```shell
flyctl launch   # the first time
flyctl deploy   # subsequent app/config changes
```

(Note: I have no affilliation with Fly, just think it's a neat product) 

### Make requests

Use the OpenAPI request interface at `/docs`, or construct an artisan `curl` request:

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "this is a test bit of text for sentiment inference"
}'
```


## caveat emptor

- lacks tests 
- could use some automation (GH Actions)
    - run tests
    - build image
    - push to hub
    - redeploy
- no inference optimization
    - currently assumes cpu (and dependencies not optimized)
- Fly deployment works but has many opportunities for improvement
    - 1 machine deployment + auto-stop = everything is off after ~60 seconds of no usage
    - app takes ~5 minutes to be responsive to requests
    - use of volumes would avoid downloading weights on every restart (adds ~1 min) 
- docker image could be slimmed
    - choose dependencies more precisely, especially torch cpu/gpu
    - copy only what's really needed 
    - counterpoint: could add the model weights to the image to avoid download on startup
