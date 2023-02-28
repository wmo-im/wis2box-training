# wis2box-training
Repository to contain training materials and data for training on the configuration and use of the WIS2box.

### bucket with wis2-training-materials

Files can be shared within the local network using the Minio-bucket 'wis2-training-materials' on local-repo-vm-222

For example to create/update the wis2box release archive:

```bash
zip -r wis2box-training-release.zip wis2box-training-release/
```

Upload into the 'wis2-training-materials'-bucket

```bash
python3 upload_training_materials.py wis2box-training-release.zip
```

After which the file can be downloaded by:

```bash
wget http://10.0.2.222/wis2-training-materials/wis2box-training-release.zip
```

### bucket with static html for topics

Exercise instructions can be shared on the local network using the Minio-bucket 'topics' on local-repo-vm-222.

To update the static html in the 'topics'-bucket after a git pull:

```
python3 update_topics_html.py
```