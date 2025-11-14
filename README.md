Birding West Bengal Discord server bot
====================================

Upgrading dependencies
----------------------

```sh
cd birding_wb_bot/
pip-compile --upgrade
```

Running locally
---------------

```sh
# Assuming you're a member and have a config with this name. To read some required secrets & RBA exclude list.
gcloud config configurations activate birding-wb
python -m birding_wb_bot.main
```

Pushing a new image
-------------------

No pipeline for this yet:

```sh
docker build -t us.gcr.io/birding-wb/birding-wb-bot:latest . && docker push us.gcr.io/birding-wb/birding-wb-bot:latest
```

Deploying
---------

```sh
gcloud compute ssh --plain --zone "us-central1-a" --project "birding-wb" --command="sudo systemctl restart cloudservice.service" birding-wb-bot-compute
```

Rare Bird Alerts bot
--------------------

The `Birding WB eBird Rarities Bot` will attempt to post to a channel named `#ebird-alerts` in any guild/server it is added to.

The eBird `Recent notable observations` API returns a lot of results that we don't really consider worth posting (e.g. high counts), so anything that matches the [exclude list](./data/rare-bird-excludes.txt) is filtered out.

Text in parenthesis is trimmed from the name before matching (e.g. `(hybrid)`)
