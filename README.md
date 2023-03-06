# wis2box-training

Repository containing wis2box training material (exercises, data, configuration).

## Environment

This training is provided on a local network containing all data, images and configurations required
to deliver wis2box training in an isolated environment/network.

Workshop resources can be found at the following areas.

### Exercise materials

Files can be shared within the local network using the MinIO `exercise-materials` bucket on `local-repo-vm-222`:

```bash
wget http://10.0.2.222/exercise-materials/wis2box-training-release.zip
```

### Static HTML for topics

Exercise instructions can be shared on the local network using the MinIO `documentation` bucket on `local-repo-vm-222`.

To update the static HTML in the `documentation` bucket after a git pull/update:

```bash
python3 update_topics_html.py
```

## Building the workshop content locally

The workshop manual is powered by [MkDocs](https://www.mkdocs.org) which facilitates easy management
of training content and publishing. Workshop content is written in Markdown.

### Setting up the manual environment locally

```bash
# build a virtual Python environment in isolation
python3 -m venv .
. bin/activate
# fork or clone from GitHub
git clone https://github.com/wmo-im/wis2box-training.git
cd wis2box-training/content
# install required dependencies
pip install -r requirements.txt
# build the website
mkdocs build
# serve locally
mkdocs serve  # website is made available on http://localhost:8000
```

## Contributing updates

To make contributions back to the workshop, fork the repository from GitHub.  Contributions and Pull Requests are always welcome!

Changes to the GitHub repository result in an automated build and deploy of the content to [wmo-im.github.io/wis2box-training](https://wmo-im.github.io/wis2box-training).

## Deploying to live site

Website updates are automatically published via GitHub Actions. To publish manually:

```bash
# NOTE: you require access privileges to the GitHub repository
# to publish live updates
mkdocs gh-deploy -m 'add new page on topic x'
```
