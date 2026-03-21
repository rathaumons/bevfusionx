# Docker 🐳

You can easily pull the [**official images from Docker Hub 🐳**](https://hub.docker.com/r/ratharog/bevfusionx) and build BEVFusionx as follows:

- **Step 1: On host**

  ```bash
  # Pull from Docker Hub (lastest=cu130)
  docker pull ratharog/bevfusionx:latest
  
  # Start a Docker container with /workspace mounted @ /home/$USER/docker/bevfusionx-latest
  docker run --gpus all -it \
      --name bevfusionx-latest \
      --shm-size=32g \
      -v /home/$USER/docker/bevfusionx-latest:/workspace \
      ratharog/bevfusionx:latest \
      bash
  ```

- **Step 2: Inside the container**

  ```bash
  cd /workspace
  git clone -b v1.0.0-bevfusionx https://github.com/rathaumons/bevfusionx.git
  cd bevfusionx
  python setup.py develop
  ```

- **Step 3**: Check the main [README.md](https://github.com/rathaumons/bevfusionx#readme) for information on preparing datasets, running evaluations, training models, and visualizing results.

Or, if you want to build and run BEVFusionx yourself, use the provided Dockerfiles and Docker Compose files for easy building and management (See details [here](dockerfile.md)):

- [`Dockerfile.cu130`](Dockerfile.cu130) · [`docker-compose-cu130.yml`](docker-compose-cu130.yml) 🆕
- [`Dockerfile.cu128`](Dockerfile.cu128) · [`docker-compose-cu128.yml`](docker-compose-cu128.yml)
- [`Dockerfile.cu126`](Dockerfile.cu126) · [`docker-compose-cu126.yml`](docker-compose-cu126.yml)
- [`Dockerfile.cu121`](Dockerfile.cu121) · [`docker-compose-cu121.yml`](docker-compose-cu121.yml)
- [`Dockerfile.cu113`](Dockerfile.cu113) · [`docker-compose-cu113.yml`](docker-compose-cu113.yml)

Or, if you want fully manual, step-by-step dev notes for different CUDA versions, see:

- [`dev_note_cu130.md`](dev_note_cu130.md) 🆕
- [`dev_note_cu128.md`](dev_note_cu128.md)
- [`dev_note_cu126.md`](dev_note_cu126.md)
- [`dev_note_cu121.md`](dev_note_cu121.md)
