# Docker 🐳

This guide describes how to build and run the BEVFusion training environment using Dockerfile for reproducible image build and docker compose YML for convenient run/start/stop.

For the original fully manual, step-by-step dev notes for different CUDA versions, see: 

- [`dev_note_cu128.md`](dev_note_cu128.md)
- [`dev_note_cu126.md`](dev_note_cu126.md)
- [`dev_note_cu121.md`](dev_note_cu121.md)
- [`dev_note_cu113.md`](dev_note_cu113.md)

## Prerequisites

Make sure Docker is correctly installed and configured on host, see: [`prerequisites.md`](prerequisites.md).

## Build image using Dockerfile

From the [current directory](.) containing `Dockerfile.cuxxx` files on host:

```bash
# Use legacy builder (Not recommend)
# export DOCKER_BUILDKIT=0

# For CUDA 12.8
docker build -f Dockerfile.cu128 -t bev-train:cu128 .
```

(Optional) Export docker image:

<details><summary>Show more details</summary>

```bash
# For CUDA 12.8
docker save bev-train:cu128 -o bev_train_cu128_2026.tar
sha256sum bev_train_cu128_2026.tar > bev_train_cu128_2026.tar.sha256
```

</details>

## Run container

There are 2 option to manage container:

- Option 1: [CLI mode](https://docs.docker.com/reference/cli/docker/); for example, container with CUDA 12.8:

  - Run container with all GPUs and a mount `-v host:container`:

    ```bash
    docker run --gpus all -it \
        --name bev-train-cu128 \
        --shm-size=32g \
        -v /home/$USER/docker/bev_train_cu128:/workspace \
        bev-train:cu128 \
        bash
    ```

  - Re-enter the running container:

    ```bash
    docker exec -it bev-train-cu128 bash
    ```

  - Stop the running container:

    ```bash
    docker stop bev-train-cu128
    ```

  - Restart/start the container:

    ```bash
    docker restart bev-train-cu128
    ```


- Option 2: [Compose mode](https://docs.docker.com/reference/cli/docker/compose/) using `docker-compose-cuxx.yml` files:

  - Build + start (background):

    ```bash
    docker compose -f docker-compose-cu128.yml up -d --build
    ```

  - Stop the running container:

    ```bash
    docker compose -f docker-compose-cu128.yml stop
    ```

  - Stop and remove the container:

    ```bash
    docker compose -f docker-compose-cu128.yml down
    ```

### Note: 

- File `docker-compose-cuxxx.yml` uses `/home/${USER}/...` where `${USER}` is expanded from your host environment.
- If `${USER}` is not set, replace it with your actual username or preferred path.

## BEVFusion: Build and install

Enter the container from host:

```bash
docker restart bev-train-cu128
docker exec -it bev-train-cu128 bash
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
git clone https://github.com/rathaumons/bevfusionx.git
cd bevfusionx
python setup.py develop
```

Check the main [README.md](../../README.md) for prepare dataset, run evaluations, and train models.
