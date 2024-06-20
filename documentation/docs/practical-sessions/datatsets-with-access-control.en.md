---
title: Setting up a recommended dataset with access control
---

# Setting up a recommended dataset with access control

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create a new dataset with data-policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset

## Introduction

Datasets that are not considered 'core' dataset in WMO

## create a new dataset with data-policy 'recommended'

Go to the 'dataset editor' page in the wis2box-webapp and create a new dataset. In the dataset editor, set the data-policy to 'recommended'.

## add an access token to the dataset

Login to the wis2box-management container and add an access token to the dataset.

```bash
docker exec -it wis2box-management bash
```

```bash
wis2box auth add-token --mdi urn:md:wmo:mydataset --token S3cr3tT0k3n
```

## publish some data to the dataset

Publish some data to the dataset.

Check the canonical-link in the WIS2 Notification Message and copy-paste the link to the browser.

You should see a 403 Forbidden error.

## add the access token to HTTP headers to access the dataset

Add the access token to the HTTP headers to access the dataset.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Did you manage the access the data?

## clean up

Delete the dataset using the dataset editor.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create a new dataset with data-policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset
