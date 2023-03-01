# wis2box-training
Repository to contain training materials and data for training on the configuration and use of the WIS2box.

### bucket with exercise-materials

Files can be shared within the local network using the Minio-bucket 'exercise-materials' on local-repo-vm-222

```bash
wget http://10.0.2.222/exercise-materials/wis2box-training-release.zip
```

### bucket with static html for topics

Exercise instructions can be shared on the local network using the Minio-bucket 'documentation' on local-repo-vm-222.

To update the static html in the 'documentation'-bucket after a git pull:

```
python3 update_topics_html.py
```