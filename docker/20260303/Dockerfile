FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-lc"]

# ------------------------------------------------------------
# System packages
# ------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y wget git dos2unix libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Miniconda
# ------------------------------------------------------------
RUN mkdir -p /root/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh && \
    bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3 && \
    rm /root/miniconda3/miniconda.sh

# Add conda ENV
ENV PATH="/root/miniconda3/bin:${PATH}"

# Do conda init + ToS + update + create env
RUN source /root/miniconda3/bin/activate && \
    conda init --all && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda update --all -y && \
    conda deactivate || true && \
    conda create -n bevfusion python=3.9 -y

# Auto-activate conda env in interactive shells
RUN cat <<'EOF' >> /root/.bashrc
if [ -f "/root/miniconda3/bin/activate" ]; then
    source /root/miniconda3/bin/activate
    conda deactivate
    conda activate bevfusion
    export PYTHONWARNINGS="ignore"
    cd /workspace
    clear
    history -c && history -w
fi
EOF

# Fix Unix-style line endings
RUN dos2unix /root/.bashrc

# ------------------------------------------------------------
# Base Python requirements
# ------------------------------------------------------------
RUN source /root/miniconda3/bin/activate bevfusion && \
    pip install -U wheel setuptools==59.5.0 "pip<23" && \
    pip install numpy==1.23.5 opencv-python==4.5.5.64

RUN source /root/miniconda3/bin/activate bevfusion && \
    pip install torch==1.10.2 torchvision==0.11.3 --index-url https://download.pytorch.org/whl/cu113

# ------------------------------------------------------------
# Global ENV
# ------------------------------------------------------------

# CUDA
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# OpenMPI
ENV OPENMPI_HOME=/root/.openmpi
ENV PATH=${OPENMPI_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${OPENMPI_HOME}/lib:${LD_LIBRARY_PATH}
ENV OMPI_MCA_plm=isolated
ENV OMPI_MCA_plm_rsh_agent=sh

# ------------------------------------------------------------
# OpenMPI 4.0.4 with CUDA
# ------------------------------------------------------------

# Intall
RUN source /root/miniconda3/bin/activate bevfusion && \
    cd /root && \
    wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.4.tar.gz && \
    tar -xvf openmpi-4.0.4.tar.gz && \
    cd openmpi-4.0.4 && \
    ./configure --prefix="$HOME/.openmpi" --with-cuda=/usr/local/cuda && \
    make -j"$(nproc)" && \
    make install

# ------------------------------------------------------------
# MMCV 1.4.0 with CUDA
# ------------------------------------------------------------

# Force CUDA
# For compute capability, see: 
# https://developer.nvidia.com/cuda/gpus
ARG TORCH_CUDA_ARCH_LIST="7.5;8.6"
ENV FORCE_CUDA="1"
ENV TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST}"

# Install
RUN source /root/miniconda3/bin/activate bevfusion && \
    cd /root && \
    wget -O mmcv-1.4.0.tar.gz https://github.com/open-mmlab/mmcv/archive/refs/tags/v1.4.0.tar.gz && \
    tar -xvf mmcv-1.4.0.tar.gz && \
    cd mmcv-1.4.0 && \
    MAKEFLAGS="-j$(nproc)" MMCV_WITH_OPS=1 pip install -e . -v

# ------------------------------------------------------------
# Other Python requirements
# ------------------------------------------------------------
RUN source /root/miniconda3/bin/activate bevfusion && \
    pip install \
        Pillow==8.4.0 \
        tqdm==4.67.3 \
        git+https://github.com/rathaumons/torchpack.git \
        mmdet==2.20.0 \
        nuscenes-devkit==1.1.11 \
        numba==0.60.0 \
        flash-attn==1.0.9 \
        yapf==0.40.1 \
        mpi4py==3.0.3 \
        future==1.0.0 \
        tensorboard==2.20.0 \
        cumm-cu113==0.4.11 \
        spconv-cu113==2.3.6 \
        numpy==1.23.5 \
        opencv-python==4.5.5.64

# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------
RUN source /root/miniconda3/bin/activate bevfusion && \
    pip cache purge && \
    conda clean -a -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /root/.cache/* && \
    rm -rf /root/openmpi-4.0.4.tar.gz && \
    rm -rf /root/mmcv-1.4.0.tar.gz

WORKDIR /workspace
CMD ["bash"]
