# Visualization 👁️

Default command for visualization:

```bash
torchpack dist-run -np [number of GPU] python tools/visualize.py [config file] [extra options]
```

For more details, see [visualize.py](https://github.com/rathaumons/bevfusionx/blob/cu113/tools/visualize.py).

## Ground-truth Visualization:

Default command:

```bash
torchpack dist-run -np [number of GPU] python tools/visualize.py [config file] --out-dir [output dir]
```

- Visualize with 1 GPU:

  <details><summary>Show more details</summary>

  - BEVFusion detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --out-dir viz/gt_det
    ```

  - BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --out-dir viz/gt_det_radar
    ```

  - BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --out-dir viz/gt_seg
    ```

  </details>

- Visualize with 2 GPU:

  <details><summary>Show more details</summary>

  - BEVFusion detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --out-dir viz/gt_det
    ```

  - BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --out-dir viz/gt_det_radar
    ```

  - BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --out-dir viz/gt_seg
    ```

  </details

## Model Visualization:

Default command:

```bash
torchpack dist-run -np [number of GPU] python tools/visualize.py [config file] --checkpoint [checkpoint file] --out-dir [output dir] --mode pred --bbox-score [float]
```

- Visualize with 1 GPU:

  <details><summary>Show more details</summary>

  - BEVFusion detection model (Camera + LiDAR):
  
    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --checkpoint=pretrained/bevfusion-det.pth --out-dir viz/bev_det --mode pred --bbox-score 0.1
    ```

  - BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --checkpoint=pretrained/bevfusion-det-radar.pth --out-dir viz/bev_det_radar --mode pred --bbox-score 0.1
    ```

  - BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 1 python tools/visualize.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --checkpoint=pretrained/bevfusion-seg.pth --out-dir viz/bev_seg --mode pred --bbox-score 0.1
    ```

  </details>

- Visualize with 2 GPU:

  <details><summary>Show more details</summary>

  - BEVFusion detection model (Camera + LiDAR):

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --checkpoint=pretrained/bevfusion-det.pth --out-dir viz/bev_det --mode pred --bbox-score 0.1
    ```

  - BEVFusion detection model (Camera + RADAR):

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/det/centerhead/lssfpn/camera+radar/resnet50/dlss.yaml --checkpoint=pretrained/bevfusion-det-radar.pth --out-dir viz/bev_det_radar --mode pred --bbox-score 0.1
    ```

  - BEVFusion segmentation model:

    ```bash
    torchpack dist-run -np 2 python tools/visualize.py configs/nuscenes/seg/fusion-bev256d2-lss.yaml --checkpoint=pretrained/bevfusion-seg.pth --out-dir viz/bev_seg --mode pred --bbox-score 0.1
    ```
