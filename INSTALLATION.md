# Installation 🚀

This guide walks you through installing the project directly on your machine. Note that because the project has very limited and strict requirements (Locked to [CUDA 11.3](https://docs.nvidia.com/cuda/archive/11.3.1/)), this installation path may only work reliably on older or specific hardware.

If you have newer‑generation hardware or prefer an isolated, reproducible environment, you can instead use [Docker 🐳](docker).

## Prepare prerequisites

- Only Linux
- Only gcc/g++ 9; otherwise, errors will occur later in some builds.
- Only [CUDA 11.3](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) & [cuDNN 8.9.7](https://docs.nvidia.com/deeplearning/cudnn/latest/installation/linux.html)
- Only Python 3.8/3.9 -> `conda create --name bevfusion python=3.9`

## Install requirements and build

- From here, you must switch to gcc/g++ 9, and activate your conda environment:

  ```bash
  conda activate bevfusion
  ```

- Install `opencv-python` and `numpy`:

  ```
  pip install "pip<23" "setuptools==59.5.0" "wheel<0.40" # MUST DO !!!
  pip install "numpy==1.23.5" "opencv-python<4.6"
  ```

- Install [PyTorch](https://pytorch.org/) 1.10.2 + CUDA 11.3 (Max support: `compute_86`, `sm_86`):

  <details><summary>Show more details</summary>

  - pip (recommended):

    ```bash
    pip install torch==1.10.2 torchvision==0.11.3 --index-url https://download.pytorch.org/whl/cu113
    ```

  - or conda:

    ```bash
    conda install pytorch==1.10.2 torchvision==0.11.3 cudatoolkit=11.3 -c pytorch -c conda-forge
    ```

  </details>

- Install OpenMPI v4.0.4 (CUDA):

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

- Install MMCV v1.4.0 (CUDA):

  <details><summary>Show more details</summary>

  - Clone source:

    ```bash
    cd ~
    wget -O mmcv-1.4.0.tar.gz https://github.com/open-mmlab/mmcv/archive/refs/tags/v1.4.0.tar.gz
    tar -xvf mmcv-1.4.0.tar.gz
    ```

  - Config cmake, build, and install:

    ```bash
    cd mmcv-1.4.0
    MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 pip install -e . -v
    ```

  - Quick test:

    ```bash
    python -W ignore -c "import mmcv"
    python -W ignore .dev_scripts/check_installation.py
    ```

  </details>

- Clone the repo and install Python Packages:

  ```bash
  cd ~ # or choose your preferred location
  git clone https://github.com/rathaumons/bevfusionx.git
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
