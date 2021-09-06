# TUS

Stands for "Tiny URL Shortener" or "Tom's URL Shortener"

## What?

A dockerizable URL shortener written in Django.

## Why?

I couldn't find a good one fitting my needs. 

## How?

Published as [ghcr.io/tkw1536/tus](https://ghcr.io/tkw1536/tus) docker image.

```bash
docker run --name=tus -e 'DJANGO_ALLOWED_HOSTS=*' -e 'DJANGO_SECRET_KEY=supersecret' -v data:/data/ -p 8080:8080 ghcr.io/tkw1536/tus
docker exec -ti tus python manage.py createsuperuser
```

Afterwards visit `http://localhost:8080/admin` to login.
Everything should be self-explanatory.
