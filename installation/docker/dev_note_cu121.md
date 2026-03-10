# DEV NOTE 20260306 (CUDA 12.1)

This file contains the original, fully-tested manual steps used to build the BEVFusion training environment interactively inside a container.

> Recommended usage now:
> - Use [`Dockerfile`](Dockerfile) + [`docker-compose.yml`](docker-compose.yml) for reproducible builds (see [`README.md`](README.md))
> - Keep this file as a reference / troubleshooting log

## Prepare prerequisites

- Install Docker on host [[Official guide](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements)]:

  <details><summary>Show more details</summary>

  - Enable [KVM](https://docs.docker.com/desktop/setup/install/linux/#kvm-virtualization-support):

    ```bash
    # install cpu-checker
    sudo apt-get install -y cpu-checker

    # activate kvm
    modprobe kvm
    modprobe kvm_intel
    kvm-ok

    # check kvm
    lsmod | grep kvm
    ls -al /dev/kvm

    # check groups
    groups $USER

    # add user to group kvm and reboot
    sudo usermod -aG kvm $USER
    sudo reboot
    ```

  - Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

    ```bash
    # install requirements
    sudo apt-get update && sudo apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg2

    # add key & repo
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # install
    sudo apt-get update
    sudo apt-get install nvidia-container-toolkit

    # config the docker to use nvidia
    sudo nvidia-ctk runtime configure --runtime=docker
    ```

  - Install [Docker CE](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository):

    ```bash
    # add GPG key
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # add repo
    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
    Types: deb
    URIs: https://download.docker.com/linux/ubuntu
    Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
    Components: stable
    Signed-By: /etc/apt/keyrings/docker.asc
    EOF

    # install
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo systemctl start docker

    # test
    docker ps
    ```

  - If docker fails to run, check [this](https://docs.docker.com/engine/install/linux-postinstall) or:

    ```bash
    sudo usermod -aG docker $USER
    sudo reboot
    ```

  </details>

## Create a container for BEVFusion

- Pull the [official NVIDIA CUDA 12.1.0](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/unsupported-tags.md#cuda-1210-1) on host:

  ```bash
  docker pull nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04
  ```

- Create and run `bev-train-cu121` container with a mounted workspace `home/$USER/docker/bev_train_cu121:/workspace`:

  ```bash
  docker run --gpus all -it \
      --name bev-train-cu121 \
      --shm-size=32g \
      -v /home/$USER/docker/bev_train_cu121:/workspace \
      nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04 \
      bash
  ```

- Install all necessary packages and miniconda inside the running container `bev-train-cu121`:

  <details><summary>Show more details</summary>

  - Check the packages:

    ```bash
    apt list --installed
    nvcc --version
    gcc --version
    g++ --version
    ```

  - Install necessary packages:

    ```bash
    apt-get update
    apt-get install -y wget git libgl1 libglib2.0-0
    ```

  - Install [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2):

    ```bash
    cd ~
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh
    source ~/miniconda3/bin/activate
    conda init --all
    conda update --all
    ```

  - Create a Python 3.9 environment call `bevfusion`:

    ```bash
    conda deactivate
    conda create -n bevfusion python=3.11 -y
    ```

  - Add to `.bashrc` using [VS Code](https://code.visualstudio.com/download) from host:

    ```bash
    if [ -f "/root/miniconda3/bin/activate" ]; then
        source /root/miniconda3/bin/activate
        conda deactivate
        conda activate bevfusion
        cd /workspace
        clear
        history -c && history -w
    fi
    ```

  </details>

## Install requirements

- Enter the container `bev-train-cu121` from host:

  ```bash
  docker restart bev-train-cu121
  docker exec -it bev-train-cu121 bash
  ```

- Install `opencv-python` and `numpy`:

  ```
  pip install -U pip wheel "setuptools<82"
  pip install numpy==1.26.4 "opencv-python<4.12"
  ```

- Install [PyTorch](https://pytorch.org/) 2.2.2 + CUDA 12.1 (Max support: `compute_90`, `sm_90`):

  ```bash
  pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cu121
  ```

- Install [OpenMPI v4.0.7](https://www.open-mpi.org/software/ompi/v4.0/) with CUDA:

  <details><summary>Show more details</summary>

  - Clone source:

    ```bash
    cd ~
    wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.7.tar.gz
    tar -xvf openmpi-4.0.7.tar.gz
    ```

  - Config cmake with CUDA:

    ```bash
    cd openmpi-4.0.7
    ./configure --prefix="$HOME/.openmpi" --with-cuda=/usr/local/cuda
    ```

  - Build and install:

    ```bash
    make -j$(nproc)
    make install
    ```

  - Add environment variables in `.bashrc`:

    ```bash
    export OPENMPI_HOME="$HOME/.openmpi"
    if [ -d "$OPENMPI_HOME" ]; then
        export PATH="$OPENMPI_HOME/bin:$PATH"
        export LD_LIBRARY_PATH="$OPENMPI_HOME/lib:$LD_LIBRARY_PATH"
        export OMPI_MCA_plm=isolated
        export OMPI_MCA_plm_rsh_agent=sh
    fi
    ```

  - Quick test:

    ```bash
    ompi_info
    ```

  </details>

- Install [MMCV v1.7.3](https://github.com/rathaROG/mmcv/releases/tag/v1.7.3-bevfusionx) with CUDA:

  <details><summary>Show more details</summary>

  - Clone source:

    ```bash
    cd ~
    wget -O mmcv.tar.gz https://github.com/rathaROG/mmcv/archive/refs/tags/v1.7.3-bevfusionx.tar.gz
    mkdir -p mmcv && tar -xzf mmcv.tar.gz --strip-components=1 -C mmcv
    ```

  - Config cmake, build, and install:

    ```bash
    cd mmcv
    export TORCH_CUDA_ARCH_LIST="8.6;8.9"
    MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 FORCE_CUDA=1 pip install -e . --no-build-isolation -v
    ```

  - Quick test:

    ```bash
    python -W ignore -c "import mmcv"
    python -W ignore .dev_scripts/check_installation.py
    ```

  </details>

- Install other required Python packages:

  ```bash
  pip install \
      psutil \
      "Pillow<10" \
      tqdm \
      git+https://github.com/rathaumons/torchpack.git \
      "mmdet<3" \
      nuscenes-devkit==1.1.11 \
      numba \
      yapf==0.40.1 \
      mpi4py \
      future \
      tensorboard \
      numpy==1.26.4 \
      "opencv-python<4.12"
  ```

- Install custom [`cumm`](https://github.com/FindDefinition/cumm.git) and [`spconv`](https://github.com/traveller59/spconv.git) with CUDA 12.8:

  ```bash
  export CUMM_CUDA_VERSION="12.1"
  export CUMM_CUDA_ARCH_LIST="7.5;8.6;8.9"
  export CUMM_DISABLE_JIT="1"
  export SPCONV_DISABLE_JIT="1"
  export CUMM_NVRTC_STD="c++14"
  pip install git+https://github.com/rathaROG/cumm-gpu.git@v0.7.13
  pip install git+https://github.com/rathaROG/spconv-gpu.git
  ```

- Install `flash-attn==1.0.9` and `setuptools==59.5.0`:

  ```bash
  pip install --no-build-isolation flash-attn==1.0.9
  pip install setuptools==59.5.0
  ```

## Export docker image

- Enter the container `bev-train-cu121` from host:

  ```bash
  docker restart bev-train-cu121
  docker exec -it bev-train-cu121 bash
  ```

- Clean inside the running container:

  ```bash
  cd ~
  pip cache purge && \
  conda clean -a -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /tmp/* /var/tmp/* && \
  rm -rf ~/.cache/*
  ```

- Export to `bev_train_cu121_2026.tar` from host:

  ```bash
  docker commit bev-train-cu121 bev-train:cu121
  docker save -o bev_train_cu121_2026.tar bev-train:cu121
  sha256sum bev_train_cu121_2026.tar > bev_train_cu121_2026.tar.sha256
  ```

## Import docker image

- Install Docker on host -> See [[Prepare prerequisites](#prepare-prerequisites)]

- Import from `bev_train_cu121_2026.tar` in host:

  ```bash
  sha256sum -c bev_train_cu121_2026.tar.sha256
  docker load -i bev_train_cu121_2026.tar
  ```

- Start the container with a mounted workspace `home/$USER/docker/bev_train_cu121:/workspace`:

  ```bash
  docker run --gpus all -it \
      --name bev-train-cu121 \
      --shm-size=32g \
      -v /home/$USER/docker/bev_train_cu121:/workspace \
      bev-train:cu121 \
      bash
  ```

## BEVFusion: Build and run

- Enter the container from host:

  ```bash
  docker restart bev-train-cu121
  docker exec -it bev-train-cu121 bash
  ```

- Clone and build `bevfusion` inside the running container:

  ```bash
  cd /workspace
  git clone https://github.com/rathaumons/bevfusionx.git
  cd bevfusion
  python setup.py develop
  pip list
  ```

- Check the main [README.md](../README.md) for prepare dataset, run evaluations, and train models.
