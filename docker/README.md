# Docker 🐳

This guide describes how to build and run the BEVFusion training environment using:

- [`Dockerfile`](Dockerfile) (reproducible image build)
- [`docker-compose.yml`](docker-compose.yml) (convenient run/start/stop)

For the original fully manual, step-by-step dev notes, see: [`dev_note.md`](dev_note.md).

## Prerequisites

- Install Docker on host, see: [`dev_note.md`](dev_note.md#prepare-prerequisites).

- Must set `nvidia` to [`default-runtime`](https://github.com/open-mmlab/mmcv/issues/1154#issuecomment-880515012) in `/etc/docker/daemon.json`:

  ```json
  {
      "runtimes": {
          "nvidia": {
              "args": [],
              "path": "nvidia-container-runtime"
          }
      },
      "default-runtime": "nvidia"
  }
  ```

## Build image ([`Dockerfile`](Dockerfile))

- From the [current directory](.) containing [`Dockerfile`](Dockerfile):

  ```bash
  # export DOCKER_BUILDKIT=0 # Use legacy builder
  docker build -t bev-train:latest .
  ```

## Export image

- From host:

  ```bash
  docker save bev-train:latest -o bev_train_2026.tar
  sha256sum bev_train_2026.tar > bev_train_2026.tar.sha256
  ```

## Run container (CLI)

- Create and run the container with GPU enabled and a mounted workspace:

  ```bash
  docker run --gpus all -it \
      --name bev-train \
      --shm-size=32g \
      -v /home/$USER/docker/bev_train:/workspace \
      bev-train:latest \
      bash
  ```

- Re-enter later:

  ```bash
  docker restart bev-train
  docker exec -it bev-train bash
  ```

## Run container (Compose [`docker-compose.yml`](docker-compose.yml))

- Build + start (background):

  ```bash
  docker compose up -d --build
  ```

- Enter the running container:

  ```bash
  docker exec -it bev-train bash
  ```

- Stop and remove:

  ```bash
  docker compose down
  ```

> Note: `docker-compose.yml` uses `/home/${USER}/...`. `${USER}` is expanded from your host environment.
> If `${USER}` is not set, replace it with your actual username/path.

## BEVFusion: Build and run

- Enter the container from host:

  ```bash
  docker restart bev-train
  docker exec -it bev-train bash
  ```

- If you didn't follow [Prerequisites](#prerequisites) or due to some unknown reasons, MMCV might need a rebuild to get a proper CUDA support:

  <details><summary>Show more details</summary>

  ```bash
  cd /root/mmcv-1.4.0

  # Check if MMCV has CUDA support
  python -W ignore -c "import mmcv"
  python -W ignore .dev_scripts/check_installation.py

  # Rebuild if MMCV has no CUDA support
  MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 pip install -e . -v
  ```

  </details>

- Clone and build `bevfusion` inside the running container:

  ```bash
  cd /workspace
  git clone https://github.com/rathaumons/bevfusionx.git
  cd bevfusionx
  python setup.py develop
  ```

- Check the main [README.md](../README.md) for prepare dataset, run evaluations, and train models.
