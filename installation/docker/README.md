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
  git clone -b v1.3.0-bevfusionx https://github.com/rathaumons/bevfusionx.git
  cd bevfusionx
  python setup.py develop
  ```

  <details><summary>Show more details</summary><br>

  From version 1.2.0, you can fully control CUDA architecture selection from the terminal when building extensions:

  - Full control: Use the `BEVX_CUDA_ARCH_LIST` environment variable to specify custom architectures (e.g., "8.9;12.0"; see [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch) docs for syntax). For example, for normal consumer GPUs from **NVIDIA RTX 4000/5000** series and **NVIDIA DGX Spark**:

    ```bash
    BEVX_CUDA_ARCH_LIST="8.9;12.0;12.1+PTX" python setup.py develop
    ```

  - Filtered auto-detection: Use `BEVX_GPU_TYPE` to specify the GPU type (`gpu_type`) and `BEVX_MIN_SM` to set the minimum SM number (`min_sm`) for auto-filtering via the [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch) package. For example, for Data Center GPUs from **NVIDIA T4, A100, H100, ...** to **NVIDIA RTX PRO 6000 Blackwell Server Edition**:

    ```bash
    BEVX_GPU_TYPE=dcen BEVX_MIN_SM=75 python setup.py develop
    ```

  </details>

- **Step 3**: Check the main [README.md](https://github.com/rathaumons/bevfusionx#readme) for information on preparing datasets, running evaluations, training models, and visualizing results.

Or, if you want to build and run BEVFusionx yourself, use the provided Dockerfiles and Docker Compose files for easy building and management (See details [build.md](build.md)):

- Data center GPUs: [`Dockerfile.cu130d`](Dockerfile.cu130d) · [`docker-compose-cu130d.yml`](docker-compose-cu130d.yml) 🆕
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu130`](Dockerfile.cu130) · [`docker-compose-cu130.yml`](docker-compose-cu130.yml) 🆕
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu128`](Dockerfile.cu128) · [`docker-compose-cu128.yml`](docker-compose-cu128.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu126`](Dockerfile.cu126) · [`docker-compose-cu126.yml`](docker-compose-cu126.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu121`](Dockerfile.cu121) · [`docker-compose-cu121.yml`](docker-compose-cu121.yml)
- Consumer/Workstation/Jetson GPUs: [`Dockerfile.cu113`](Dockerfile.cu113) · [`docker-compose-cu113.yml`](docker-compose-cu113.yml)

Or, if you want fully manual, step-by-step dev notes for different CUDA versions, see:

- [`dev_note_cu130.md`](dev_note_cu130.md) 🆕
- [`dev_note_cu128.md`](dev_note_cu128.md)
- [`dev_note_cu126.md`](dev_note_cu126.md)
- [`dev_note_cu121.md`](dev_note_cu121.md)
