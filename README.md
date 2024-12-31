# Sentiment API, run three ways

A simple text sentiment API. 

Clone and enter the repo, then run it...

## ... locally with `uv` ([installation](https://docs.astral.sh/uv/getting-started/installation/))

```shell
make local-dev
```

## ... locally with Docker

```shell
make docker-run
```

## ... deployed to Fly.io (no affiliation)

1. [Install and set up an account](https://fly.io/docs/getting-started/)
2. (Probably?) Change the `app` name in `fly.toml` to something unique

```shell
flyctl launch   # the first time
flyctl deploy   # subsequent app/config changes
```

## caveat emptor

- could use some automation (GH Actions)
    - run tests
    - build image
    - push to hub
    - redeploy
- lacks tests 
- no inference optimization
    - currently assumes cpu
- app is slow to load after Fly deployment
    - takes ~5 minutes before first successful response 
    - use of volumes would avoid downloading weights on every restart (~1 min) 
- docker image could be slimmed
    - choose cpu/gpu dependencies more precisely
    - copy only what's really needed
    - counterpoint: could save the weights in the image for faster app startup
