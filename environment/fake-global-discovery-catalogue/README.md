# Global Discovery Catalogue for training purposes

To add a WIS2 Global Discovery Catalogue (GDC) for WIS2 training, git clone the [wis2-gdc](https://github.com/wmo-im/wis2-gdc) as per the [Docker instructions](https://github.com/wmo-im/wis2-gdc?tab=readme-ov-file#docker) with the following additional steps:

- copy the [`wis2-gdc-training.env`](wis2-gdc-training.env) file in this directory to `wis2-gdc.env`
  - note to set `WIS2_GDC_GB` to the `GB_HOST` environment variable which is the host of the Fake Global Broker in the training network
- in `docker-compose.override.yml`, change the default GDC API port from `80:80` to `5002:80`
- in `wis2-gdc-api/docker/wis2-gdc-api.yml`, change the default port (`server.bind.port`) from `5000` to `5002`
- start the GDC using `make up`
