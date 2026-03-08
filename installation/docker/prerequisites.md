# Prerequisites

Install Docker on host (See [official guide here](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements)):

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
