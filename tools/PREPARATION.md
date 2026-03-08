# Preparation 📚

## Prepare nuScenes dataset

For nuScenes dataset:

- Default path [`bevfusionx/data/nuscenes`](./data/nuscenes):

  ```
  bevfusion
  ├── assets
  ├── configs
  ├── data
  │   ├── nuscenes
  │   │   ├── maps
  │   │   ├── samples
  │   │   ├── sweeps
  │   │   ├── v1.0-xxx
  ```

- Full version:

  ```
  python tools/create_data.py nuscenes --root-path ./data/nuscenes --out-dir ./data/nuscenes --extra-tag nuscenes
  ```

- Mini version:

  ```
  python tools/create_data.py nuscenes --root-path ./data/nuscenes --out-dir ./data/nuscenes --extra-tag nuscenes --version v1.0-mini
  ```

- All [available versions here](https://github.com/rathaumons/bevfusionx/blob/main/tools/data_converter/nuscenes_converter.py#L62): `available_vers = ["v1.0-trainval", "v1.0-test", "v1.0-mini"]`

- More info: [mmdetection3d/docs/en/datasets/nuscenes_det.md](https://github.com/open-mmlab/mmdetection3d/blob/1.0/docs/en/datasets/nuscenes_det.md)

## Prepare pretrained models

For pretrain models, simply run [download_pretrained.sh](tools/download_pretrained.sh) or download manually and place them in [pretrained](pretrained):

- [bevfusion-det.pth](https://www.dropbox.com/scl/fi/ulaz9z4wdwtypjhx7xdi3/bevfusion-det.pth?rlkey=ovusfi2rchjub5oafogou255v)
- [bevfusion-seg.pth](https://www.dropbox.com/scl/fi/8lgd1hkod2a15mwry0fvd/bevfusion-seg.pth?rlkey=2tmgw7mcrlwy9qoqeui63tay9)
- [lidar-only-det.pth](https://www.dropbox.com/scl/fi/b1zvgrg9ucmv0wtx6pari/lidar-only-det.pth?rlkey=fw73bmdh57jxtudw6osloywah)
- [lidar-only-seg.pth](https://www.dropbox.com/scl/fi/mi3w6uxvytdre9i42r9k7/lidar-only-seg.pth?rlkey=rve7hx80u3en1gfoi7tjucl72)
- [camera-only-det.pth](https://www.dropbox.com/scl/fi/pxfaz1nc07qa2twlatzkz/camera-only-det.pth?rlkey=f5do81fawie0ssbg9uhrm6p30)
- [camera-only-seg.pth](https://www.dropbox.com/scl/fi/cwpcu80n0shmwraegi6z4/camera-only-seg.pth?rlkey=l60kdaz19fq3gwocsjk09e60z)
- [swint-nuimages-pretrained.pth](https://www.dropbox.com/scl/fi/f3e67wgn2omoftah4ceri/swint-nuimages-pretrained.pth?rlkey=k9kafympye80b3b1quutti4yq)
