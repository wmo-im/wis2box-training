# wis2box-training
Repository to contain training materials and data for training on the configuration and use of the WIS2box.

### bucket with wis2-training-materials

Files can be shared within the local network using the Minio-bucket on local-repo-vm-222

For example to create/update the wis2box release archive:

```bash
zip -r wis2box-training-release.zip wis2box-training-release/
```

Upload into the training-materials-bucket

```bash
python3 copy_file_to_minio.py wis2box-training-release.zip http://wmo_admin:XXX@10.0.2.222/wis2-training-materials/
```

After which the file can be downloaded by:

```bash
wget http://10.0.2.222/wis2-training-materials/wis2box-training-release.zip
