# Nearly free speech dynamic dns updater

## Docker

```
docker run -d \
    --name dns_updater \
    -e LOGIN=foo \
    -e API_KEY=bar \
    -e DOMAIN=cats.com \
    gregology/nearly-free-speech-dynamic-dns-updater:latest
```

### Cron job

Running every 5 mins

`*/5 * * * * docker start dns_updater`
