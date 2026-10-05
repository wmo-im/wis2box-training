# Global Discovery Catalogue for training purposes

To add a WIS2 Global Discovery Catalogue (GDC) for WIS2 training, git clone the [wmo-resource-catalogue](https://github.com/wmo-im/wmo-resource-catalogue) as per the [Docker instructions](https://github.com/wmo-im/wmo-resource-catalogue?tab=readme-ov-file#docker) with the following additional steps:

- copy the [`wmo-resource-catalogue-training.env`](wmo-resource-catalogue-training.env) file in this directory to `wmo-resource-catalogue.env`
  - note to set `WMO_RESOURCE_CATALOGUE_GB` to the `GB_HOST` environment variable which is the host of the Fake Global Broker in the training network
- in `docker-compose.override.yml`, change the default GDC API port from `80:8080` to `5002:8080`
- in `wmo-resource-catalogue-api/docker/wmo-resource-catalogue-api.yml`, change the default port (`server.bind.port`) from `5000` to `5002`
- start the GDC using `make up`
