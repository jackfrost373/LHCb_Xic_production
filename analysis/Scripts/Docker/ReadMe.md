# Docker environment

A Docker environment contains the compressed environment of this analysis.
This Environment can be pulled directly from [Docker.hub](https://hub.docker.com/) or created by executing the Dockerfile.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install docker.

```bash
pip install docker
```

## Usage

Either pull image directly from docker:
```bash
docker pull XXX
```

Or create image and run container from local dockerfile:
(These commands have to be run in the "Docker" Folder under the Path: "LHCb_Xic_production/analysis/Scripts")

```bash
docker build [ImageName] .

docker start [ImageName]
```

## Adding packages

To add additional packages to the environment, add the respective package with its required version to the "requirements.txt" file in this folder.
E.g. "rootpy=1.0.1"

If additional packages have been added the the Docker Images MUST be created locally with the dockerfile and "docker build" command


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

