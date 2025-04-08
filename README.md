# wis2box-training

Repository containing wis2box training material (exercises, data, configuration).

## Environment

The `environment` directory provides documentation and materials used to run the local setup.

The wis2box training is designed to be run on a local network containing all data, images and configurations.

A set of hardware (Wi-Fi router and 3 mini PCs) is brought along to local training sessions. The hardware setup will provide a dedicate student VM with Ubuntu and docker to each participant.

A local registry mirroring Docker Hub is setup on the local hardware to reduce the time needed to download large Docker images in a low bandwidth environment.

## Exercise materials

All the contents of the `exercise-materials` directory are added to the gh-pages during deployment in a single zipfile `exercise-materials.zip`.

The practical sessions will start by asking the student to download this archive on their local machine and extracting it.

## Building the workshop content locally

The workshop manual is powered by [MkDocs](https://www.mkdocs.org) which facilitates easy management
and publishing of documentation.  Workshop content is written in Markdown.

### Setting up the manual environment locally

```bash
# build a virtual Python environment in isolation
python3 -m venv .
. bin/activate
# fork or clone from GitHub
git clone https://github.com/World-Meteorological-Organization/wis2box-training.git
cd wis2box-training/documentation
# install required dependencies
pip3 install -r requirements.txt
# build the website, output is in site/
mkdocs build
# serve locally
mkdocs serve  # website is made available on http://localhost:8000
```

## Contributing updates

To make contributions back to the workshop, fork the repository from GitHub.  Contributions and Pull Requests are always welcome!

Changes to the GitHub repository result in an automated build and deploy of the content to [training.wis2box.wis.wmo.int](https://training.wis2box.wis.wmo.int).

## Deploying to live site

Website updates are automatically published via GitHub Actions. To publish manually:

```bash
# NOTE: you require access privileges to the GitHub repository
# to publish live updates
mkdocs gh-deploy -m 'add new page on topic x'
```
