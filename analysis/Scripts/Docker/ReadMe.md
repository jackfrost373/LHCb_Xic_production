# Docker environment

A Docker environment contains the compressed environment of this analysis.
This Environment can be pulled directly from [Docker.hub](https://hub.docker.com/) or created by executing the Dockerfile.
## Installation

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## Usage

Either pull image directly from docker:
```bash
docker pull fritter3110/xic.lc_production_ratio_analysis:latest
```

Or create image and run container from local dockerfile:

(These commands have to be run in the "Docker" Folder under the Path: "LHCb_Xic_production/analysis/Scripts")

```bash
docker build -t [UserName]/[ImageName]:1.0 .

docker run [ImageName]
```

## Adding packages

To add additional packages to the environment, add the respective package with its required version to the "requirements.txt" file in this folder.
E.g. "rootpy=1.0.1"

If additional packages have been added the the Docker Images MUST be created locally with the dockerfile and "docker build" command


## Contributing
Pull requests are not welcome. For major ideas for change, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

