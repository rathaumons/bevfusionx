# Run ▶️

## Evaluation

Default command for evaluating a model: 

```bash
torchpack dist-run -np [number of GPU] python tools/test.py [config file path] pretrained/[checkpoint name].pth --eval [evaluation type]
```

For more details, see [test.py](https://github.com/rathaumons/bevfusionx/blob/main/tools/test.py).

- Evaluate with 1 GPU:

  <details><summary>Show more details</summary>

  - Evaluate the detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 1 python tools/test.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml pretrained/bevfusion-det.pth --eval bbox
    ```

  - Evaluate the detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 1 python tools/test.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml pretrained/bevfusion-det-radar.pth --eval bbox
    ```

  - Evaluate the segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/test.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml pretrained/bevfusion-seg.pth --eval map
    ```

  </details>

- Evaluate with 2 GPUs:

  <details><summary>Show more details</summary>

  - Evaluate the detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 2 python tools/test.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml pretrained/bevfusion-det.pth --eval bbox
    ```

  - Evaluate the detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 2 python tools/test.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml pretrained/bevfusion-det-radar.pth --eval bbox
    ```

  - Evaluate the segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/test.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml pretrained/bevfusion-seg.pth --eval map
    ```

  </details>

## Training

Default command for training a model: 

```bash
torchpack dist-run -np [number of GPU] python tools/train.py [config file path] [extra options]
```

For more details, see [train.py](https://github.com/rathaumons/bevfusionx/blob/main/tools/train.py).

- Train with 1 GPU:

  <details><summary>Show more details</summary>

  - Train the camera-only model:

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/det/centerhead/lssfpn/camera/256x704/swint/default.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```

  - Train the camera-only segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/seg/camera-bev256d2.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```

  - Train the LiDAR-only model:

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/det/transfusion/secfpn/lidar/voxelnet_0p075.yaml
    ```

  - Train the LiDAR-only segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/seg/lidar-centerpoint-bev128.yaml
    ```

  - Train the BEVFusion detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth --load_from pretrained/lidar-only-det.pth 
    ```

  - Train the BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```

  - Train the BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/train.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```

  </details>

- Train with 2 GPUs:

  <details><summary>Show more details</summary>

  - Train the camera-only model:

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/det/centerhead/lssfpn/camera/256x704/swint/default.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```
  
  - Train the camera-only segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/seg/camera-bev256d2.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```
  
  - Train the LiDAR-only model:

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/det/transfusion/secfpn/lidar/voxelnet_0p075.yaml
    ```
  
  - Train the LiDAR-only segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/seg/lidar-centerpoint-bev128.yaml
    ```
  
  - Train the BEVFusion detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth --load_from pretrained/lidar-only-det.pth 
    ```

  - Train the BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```
  
  - Train the BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/train.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --model.encoders.camera.backbone.init_cfg.checkpoint pretrained/swint-nuimages-pretrained.pth
    ```

  </details>
