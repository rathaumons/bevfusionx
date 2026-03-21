# Docker 🐳 · Dockerfile.cuxxx

Here, you can build and run BEVFusionx using the provided Dockerfiles and Docker Compose files for easy building and management:

- [`Dockerfile.cu130`](Dockerfile.cu130) · [`docker-compose-cu130.yml`](docker-compose-cu130.yml) 🆕
- [`Dockerfile.cu128`](Dockerfile.cu128) · [`docker-compose-cu128.yml`](docker-compose-cu128.yml)
- [`Dockerfile.cu126`](Dockerfile.cu126) · [`docker-compose-cu126.yml`](docker-compose-cu126.yml)
- [`Dockerfile.cu121`](Dockerfile.cu121) · [`docker-compose-cu121.yml`](docker-compose-cu121.yml)
- [`Dockerfile.cu113`](Dockerfile.cu113) · [`docker-compose-cu113.yml`](docker-compose-cu113.yml)

## Prerequisites

Make sure Docker is correctly installed and configured on host, see: [`prerequisites.md`](prerequisites.md).

## Build image using Dockerfile

From the [current directory](.) containing `Dockerfile.cuxxx` files on host:

```bash
# Use legacy builder (Not recommend)
# export DOCKER_BUILDKIT=0

# For CUDA 13.0
docker build -f Dockerfile.cu130 -t bevfusionx:cu130 .
```

(Optional) Export docker image:

<details><summary>Show more details</summary>

```bash
# For CUDA 13.0
docker save bevfusionx:cu130 -o bevfusionx_cu130.tar
sha256sum bevfusionx_cu130.tar > bevfusionx_cu130.tar.sha256
```

</details>

## Run container

There are 2 option to manage container:

- Option 1: [CLI mode](https://docs.docker.com/reference/cli/docker/); for example, container with CUDA 13.0:

  - Run container with all GPUs and a mount `-v host:container`:

    ```bash
    docker run --gpus all -it \
        --name bevfusionx-cu130 \
        --shm-size=32g \
        -v /home/$USER/docker/bevfusionx-cu130:/workspace \
        bevfusionx:cu130 \
        bash
    ```

  - Re-enter the running container:

    ```bash
    docker exec -it bevfusionx-cu130 bash
    ```

  - Stop the running container:

    ```bash
    docker stop bevfusionx-cu130
    ```

  - Restart/start the container:

    ```bash
    docker restart bevfusionx-cu130
    ```


- Option 2: [Compose mode](https://docs.docker.com/reference/cli/docker/compose/) using `docker-compose-cuxx.yml` files:

  - Build + start (background):

    ```bash
    docker compose -f docker-compose-cu130.yml up -d --build
    ```

  - Stop the running container:

    ```bash
    docker compose -f docker-compose-cu130.yml stop
    ```

  - Stop and remove the container:

    ```bash
    docker compose -f docker-compose-cu130.yml down
    ```

### Note: 

- File `docker-compose-cuxxx.yml` uses `/home/${USER}/...` where `${USER}` is expanded from your host environment.
- If `${USER}` is not set, replace it with your actual username or preferred path.

## BEVFusion: Build and install

Enter the container from host:

```bash
docker restart bevfusionx-cu130
docker exec -it bevfusionx-cu130 bash
```

If you didn't follow [Prerequisites](#prerequisites) or due to some unknown reasons, MMCV might need a rebuild to get a proper CUDA support:

<details><summary>Show more details</summary>

```bash
cd /root/mmcv

# Check if MMCV has CUDA support
python -W ignore -c "import mmcv"
python -W ignore .dev_scripts/check_installation.py

# Rebuild if MMCV has no CUDA support
pip install -U "setuptools<82"
MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 FORCE_CUDA=1 pip install -e . --no-build-isolation -v
pip install setuptools==59.5.0
```

</details>

Clone and build `bevfusion` inside the running container:

```bash
cd /workspace
git clone -b v1.0.0-bevfusionx https://github.com/rathaumons/bevfusionx.git -b v1.0.0-bevfusionx
cd bevfusionx
python setup.py develop
```

Check the main [README.md](https://github.com/rathaumons/bevfusionx#readme) for information on preparing datasets, running evaluations, training models, and visualizing results.
