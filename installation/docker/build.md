# Docker 🐳 · Dockerfile.cuxxx

Here, you can build and run BEVFusionx using the provided Dockerfiles and Docker Compose files for easy building and management:

- Data center GPUs: [`Dockerfile.cu130d`](Dockerfile.cu130d) · [`docker-compose-cu130d.yml`](docker-compose-cu130d.yml) 🆕
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu130`](Dockerfile.cu130) · [`docker-compose-cu130.yml`](docker-compose-cu130.yml) 🆕
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu128`](Dockerfile.cu128) · [`docker-compose-cu128.yml`](docker-compose-cu128.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu126`](Dockerfile.cu126) · [`docker-compose-cu126.yml`](docker-compose-cu126.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu121`](Dockerfile.cu121) · [`docker-compose-cu121.yml`](docker-compose-cu121.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu113`](Dockerfile.cu113) · [`docker-compose-cu113.yml`](docker-compose-cu113.yml)

The default build configurations target a broad range of GPUs, which can result in long build times (sometimes several hours). To speed up the process, you can modify the Dockerfile to compile only for the CUDA architectures you actually need. For example, you can generate a list of CUDA compute capabilities suited to your specific GPUs by adjusting the arguments `gpu_type='cons+jets', min_sm=60` in section:

```dockerfile
# Generate the CUDA arch list and store in /root/cuda_arch_list.txt
RUN source /root/miniconda3/bin/activate bevfusion && \
    python -c "import nvidia_arch; print(nvidia_arch.get_arches(gpu_type='cons+jets', min_sm=60, return_mode='cc_string', add_ptx=True))" > /root/cuda_arch_list.txt
```

For more details, see [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch).

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

Clone and build `bevfusion` inside the running container:

```bash
cd /workspace
git clone -b v1.3.0-bevfusionx https://github.com/rathaumons/bevfusionx.git
cd bevfusionx
python setup.py develop
```

From version 1.2.0, you can fully control CUDA architecture selection from the terminal when building extensions:

- Full control: Use the `BEVX_CUDA_ARCH_LIST` environment variable to specify custom architectures (e.g., "8.9;12.0"; see [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch) docs for syntax). For example, for normal consumer GPUs from **NVIDIA RTX 4000/5000** series and **NVIDIA DGX Spark**:

  ```bash
  BEVX_CUDA_ARCH_LIST="8.9;12.0;12.1+PTX" python setup.py develop
  ```

- Filtered auto-detection: Use `BEVX_GPU_TYPE` to specify the GPU type (`gpu_type`) and `BEVX_MIN_SM` to set the minimum SM number (`min_sm`) for auto-filtering via the [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch) package. For example, for Data Center GPUs from **NVIDIA T4, A100, H100, ...** to **NVIDIA RTX PRO 6000 Blackwell Server Edition**:

  ```bash
  BEVX_GPU_TYPE=dcen BEVX_MIN_SM=75 python setup.py develop
  ```

Check the main [README.md](https://github.com/rathaumons/bevfusionx#readme) for information on preparing datasets, running evaluations, training models, and visualizing results.
