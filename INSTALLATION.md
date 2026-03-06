# Installation 🚀

This guide walks you through installing the project directly on your machine. If you have newer‑generation hardware or prefer an isolated, reproducible environment, you can instead use Docker.

✅ **For [CUDA 11.3](https://github.com/rathaumons/bevfusionx/blob/cu113/INSTALLATION.md) | [Docker 🐳](https://github.com/rathaumons/bevfusionx/tree/cu113/docker)**

👉 For [CUDA 12.1](https://github.com/rathaumons/bevfusionx/blob/cu121/INSTALLATION.md) | [Docker 🐳](https://github.com/rathaumons/bevfusionx/tree/cu121/docker)

👉 For [CUDA 12.6](https://github.com/rathaumons/bevfusionx/blob/cu126/INSTALLATION.md) | [Docker 🐳](https://github.com/rathaumons/bevfusionx/tree/cu126/docker)

## Prepare prerequisites

- Only Linux
- Only gcc/g++ 9; otherwise, errors will occur later in some builds.
- Only [CUDA 11.3](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) & [cuDNN 8.9](https://docs.nvidia.com/deeplearning/cudnn/latest/installation/linux.html)
- Only Python 3.8/3.9 -> `conda create --name bevfusion python=3.9`

## Install requirements and build

- From here, you must switch to gcc/g++ 9, and activate your conda environment:

  ```bash
  conda activate bevfusion
  ```

- Install `opencv-python` and `numpy`:

  ```bash
  pip install -U wheel setuptools==59.5.0 "pip<23"  # MUST DO !!!
  pip install numpy==1.23.5 "opencv-python<4.6"
  ```

- Install [PyTorch](https://pytorch.org/) 1.10.2 + CUDA 11.3 (Max support: `compute_86`, `sm_86`):

  <details><summary>Show more details</summary>

  - pip (recommended):

    ```bash
    pip install torch==1.10.2 torchvision==0.11.3 --index-url https://download.pytorch.org/whl/cu113
    ```

  </details>

- Install [OpenMPI v4.0.4](https://www.open-mpi.org/software/ompi/v4.0/) (CUDA):

  <details><summary>Show more details</summary>

  - Clone source:

    ```bash
    cd ~
    wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.4.tar.gz
    tar -xvf openmpi-4.0.4.tar.gz
    ```

  - Config cmake with CUDA:

    ```bash
    cd openmpi-4.0.4
    ./configure --prefix="/home/$USER/.openmpi" --with-cuda=/usr/local/cuda
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
    fi
    ```

  - Quick test:

    ```bash
    ompi_info
    ```

  </details>

- Install [MMCV v1.4.0](https://github.com/rathaROG/mmcv/releases/tag/v1.4.0) (CUDA):

  <details><summary>Show more details</summary>

  - Clone source:

    ```bash
    cd ~
    wget -O mmcv.tar.gz https://github.com/rathaROG/mmcv/archive/refs/tags/v1.4.0.tar.gz
    mkdir -p mmcv && tar -xzf mmcv.tar.gz --strip-components=1 -C mmcv
    ```

  - Config cmake, build, and install:

    ```bash
    cd mmcv
    # export TORCH_CUDA_ARCH_LIST="7.5;8.6"  # optional for direct install
    MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 FORCE_CUDA="1" pip install -e . --no-build-isolation -v
    ```

  - Quick test:

    ```bash
    python -W ignore -c "import mmcv"
    python -W ignore .dev_scripts/check_installation.py
    ```

  </details>

- Clone the repo and install Python packages:

  ```bash
  cd ~  # or choose your preferred location
  git clone https://github.com/rathaumons/bevfusionx.git
  git checkout cu113  # IMPORTANT !!!
  cd bevfusion
  pip install -r requirements.txt
  ```

- If `mpi4py` is failed to install, try:

  <details><summary>Show more details</summary>

  ```bash
  # Find and set paths
  env_path=$(dirname "$(dirname "$(which python)")")
  ld_file="$env_path/compiler_compat/ld"
  tmp_ld_file="$env_path/compiler_compat/ld_tmp"
  
  # Temporarily renamed ld to ld_tmp
  mv "$ld_file" "$tmp_ld_file"
  
  # Install mpi4py
  pip install mpi4py==3.0.3

  # Reverted ld_tmp to ld
  mv "$tmp_ld_file" "$ld_file"
  ```

  </details>

- Build `bevfusion`:

  ```bash
  python setup.py develop
  ```

- Check the main [README.md](README.md) for prepare dataset, run evaluations, and train models.
