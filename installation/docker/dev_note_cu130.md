# DEV NOTE 20260321 (CUDA 13.0)

This file contains the original, fully-tested manual steps used to build the BEVFusion training environment interactively inside a container.

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

- Pull the [official NVIDIA CUDA 13.0.2](https://hub.docker.com/layers/nvidia/cuda/13.0.2-cudnn-devel-ubuntu24.04) on host:

  ```bash
  docker pull nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04
  ```

- Create and run `bevfusionx-cu130` container with a mounted workspace `home/$USER/docker/bevfusionx-cu130:/workspace`:

  ```bash
  docker run --gpus all -it \
      --name bevfusionx-cu130 \
      --shm-size=32g \
      -v /home/$USER/docker/bevfusionx-cu130:/workspace \
      nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04 \
      bash
  ```

- Install all necessary packages and miniconda inside the running container `bevfusionx-cu130`:

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
    apt-get install -y gcc-9 g++-9 wget git libgl1 libglib2.0-0
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

  - Create a Python 3.11 environment call `bevfusion`:

    ```bash
    conda deactivate
    conda create -n bevfusion python=3.11 -y
    ```

  - Set GCC/G++ 9 as default:

    ```bash
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 100
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 100
    update-alternatives --set gcc /usr/bin/gcc-9
    update-alternatives --set g++ /usr/bin/g++-9
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

- Enter the container `bevfusionx-cu130` from host:

  ```bash
  docker restart bevfusionx-cu130
  docker exec -it bevfusionx-cu130 bash
  ```

- Install `opencv-python` and `numpy`:

  ```
  pip install -U pip wheel "setuptools<82"
  pip install numpy==1.26.4 "opencv-python<4.12"
  ```

- Install [PyTorch](https://pytorch.org/) 2.11.0 + CUDA 13.0 (Max support: `compute_120`, `sm_120`):

  ```bash
  pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cu130
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
    export TORCH_CUDA_ARCH_LIST="8.6;8.9;12.0"  # Use nvidia-arch for better control -> https://github.com/rathaROG/nvidia-arch
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
      nvidia-arch>=6.0.0 \
      yapf==0.40.1 \
      mpi4py \
      future \
      tensorboard \
      numpy==1.26.4 \
      "opencv-python<4.12"
  ```

- Install the prebuilt wheels of custom [`cumm`](https://github.com/rathaROG/cumm-gpu) and [`spconv`](https://github.com/rathaROG/spconv-gpu) with CUDA 13.0 (Or build from sources with [`nvidia-arch`](https://github.com/rathaROG/nvidia-arch) for robust SM/CC architecture control):

  ```bash
  pip install cumm-cu130 spconv-cu130 --extra-index-url https://ratharog.github.io/cumm-spconv/
  ```

- Install `flash-attn==1.0.9` and `setuptools==59.5.0`:

  ```bash
  pip install --no-build-isolation flash-attn==1.0.9
  pip install setuptools==59.5.0
  ```

## Export docker image

- Enter the container `bevfusionx-cu130` from host:

  ```bash
  docker restart bevfusionx-cu130
  docker exec -it bevfusionx-cu130 bash
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

- Export to `bevfusionx_cu130.tar` from host:

  ```bash
  docker commit bevfusionx-cu130 bevfusionx:cu130
  docker save -o bevfusionx_cu130.tar bevfusionx:cu130
  sha256sum bevfusionx_cu130.tar > bevfusionx_cu130.tar.sha256
  ```

## Import docker image

- Install Docker on host -> See [[Prepare prerequisites](#prepare-prerequisites)]

- Import from `bevfusionx_cu130.tar` in host:

  ```bash
  sha256sum -c bevfusionx_cu130.tar.sha256
  docker load -i bevfusionx_cu130.tar
  ```

- Start the container with a mounted workspace `home/$USER/docker/bevfusionx-cu130:/workspace`:

  ```bash
  docker run --gpus all -it \
      --name bevfusionx-cu130 \
      --shm-size=32g \
      -v /home/$USER/docker/bevfusionx-cu130:/workspace \
      bevfusionx:cu130 \
      bash
  ```

## BEVFusion: Build and run

- Enter the container from host:

  ```bash
  docker restart bevfusionx-cu130
  docker exec -it bevfusionx-cu130 bash
  ```

- Clone and build `bevfusion` inside the running container:

  ```bash
  cd /workspace
  git clone -b v1.1.0-bevfusionx https://github.com/rathaumons/bevfusionx.git
  cd bevfusionx
  python setup.py develop
  pip list
  ```

- Check the main [README.md](https://github.com/rathaumons/bevfusionx#readme) for information on preparing datasets, running evaluations, training models, and visualizing results.
