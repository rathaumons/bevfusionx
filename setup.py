# Modified by UMONS-Numediart, Ratha SIV in 2026.

import os
import runpy
import torch

from pathlib import Path
from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension


PROJECT_ROOT = Path(__file__).parent
meta = runpy.run_path(PROJECT_ROOT / "mmdet3d" / "__init__.py")
PROJECT_META = {
    "version": meta["__version__"],
    "author": meta["__author__"],
    "description": meta["__description__"],
    "license": meta["__license__"],
    "repository": meta["__repository__"],
    "homepage": meta["__homepage__"],
}

def make_cuda_ext(
    name, module, sources, sources_cuda=[], extra_args=[], extra_include_path=[]
):

    define_macros = []
    extra_compile_args = {"cxx": [] + extra_args}

    if (torch.cuda.is_available() and torch.version.cuda is not None) or os.getenv("FORCE_CUDA", "0") == "1":
        define_macros += [("WITH_CUDA", None)]
        extension = CUDAExtension
        cuda_version = float(torch.version.cuda)
        if cuda_version >= 12.8:
            print(f"PyTorch deteted CUDA {cuda_version}, enabling compute capabilities sm_86, sm_89, and sm_120.")
            # See more details here: https://github.com/rathaROG/NVIDIA-CUDA-COMPUTE-CAPABILITY
            extra_compile_args["nvcc"] = extra_args + [
                "-D__CUDA_NO_HALF_OPERATORS__",
                "-D__CUDA_NO_HALF_CONVERSIONS__",
                "-D__CUDA_NO_HALF2_OPERATORS__",
                # "-gencode=arch=compute_75,code=sm_75",
                # "-gencode=arch=compute_80,code=sm_80",    # Data Center GPUs (A30, A100)
                "-gencode=arch=compute_86,code=sm_86",
                "-gencode=arch=compute_89,code=sm_89",
                # "-gencode=arch=compute_90,code=sm_90",    # Data Center GPUs (H100, H200, GH200)
                # "-gencode=arch=compute_100,code=sm_100",  # Data Center GPUs (B200, GB200)
                # "-gencode=arch=compute_103,code=sm_103",  # Data Center GPUs (B300, GB300)
                "-gencode=arch=compute_120,code=sm_120",
            ]
        elif cuda_version < 12.8 and cuda_version >= 11.8:
            print(f"PyTorch deteted CUDA {cuda_version}, enabling compute capabilities sm_75, sm_86, and sm_89.")
            # See more details here: https://github.com/rathaROG/NVIDIA-CUDA-COMPUTE-CAPABILITY
            extra_compile_args["nvcc"] = extra_args + [
                "-D__CUDA_NO_HALF_OPERATORS__",
                "-D__CUDA_NO_HALF_CONVERSIONS__",
                "-D__CUDA_NO_HALF2_OPERATORS__",
                "-gencode=arch=compute_75,code=sm_75",
                # "-gencode=arch=compute_80,code=sm_80",    # Data Center GPUs (A30, A100)
                "-gencode=arch=compute_86,code=sm_86",
                "-gencode=arch=compute_89,code=sm_89",
                # "-gencode=arch=compute_90,code=sm_90",    # Data Center GPUs (H100, H200, GH200)
            ]
        elif cuda_version < 11.8 and cuda_version >= 11.1:
            print(f"PyTorch deteted CUDA {cuda_version}, enabling compute capabilities sm_75 and sm_86.")
            # See more details here: https://github.com/rathaROG/NVIDIA-CUDA-COMPUTE-CAPABILITY
            extra_compile_args["nvcc"] = extra_args + [
                "-D__CUDA_NO_HALF_OPERATORS__",
                "-D__CUDA_NO_HALF_CONVERSIONS__",
                "-D__CUDA_NO_HALF2_OPERATORS__",
                "-gencode=arch=compute_75,code=sm_75",
                # "-gencode=arch=compute_80,code=sm_80",    # Data Center GPUs (A30, A100)
                "-gencode=arch=compute_86,code=sm_86",
            ]
        else:
            print(f"PyTorch deteted CUDA {cuda_version} which is not supported.")
            # See more details here: https://github.com/rathaROG/NVIDIA-CUDA-COMPUTE-CAPABILITY
            exit(1)
        sources += sources_cuda
    elif (torch.cuda.is_available() and torch.version.hip is not None) or os.getenv("FORCE_ROCM", "0") == "1":
        define_macros += [("WITH_ROCM", None)]
        extension = CUDAExtension
        extra_compile_args["hipcc"] = extra_args + [
            "-D__HIP_NO_HALF_OPERATORS__",
            "-D__HIP_NO_HALF_CONVERSIONS__",
            "-D__HIP_NO_HALF2_OPERATORS__",
        ]
        sources += sources_cuda
    else:
        print("Compiling {} without CUDA".format(name))
        extension = CppExtension

    return extension(
        name="{}.{}".format(module, name),
        sources=[os.path.join(*module.split("."), p) for p in sources],
        include_dirs=extra_include_path,
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
    )


if __name__ == "__main__":
    setup(
        name="mmdet3d",
        version=PROJECT_META["version"],
        author=PROJECT_META["author"],
        description=PROJECT_META["description"],
        license=PROJECT_META["license"],
        project_urls={
            "Source": PROJECT_META["repository"],
            "Homepage": PROJECT_META["homepage"],
        },
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        include_package_data=True,
        package_data={"mmdet3d.ops": ["*/*.so"]},
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.11",
        ],
        ext_modules=[
            make_cuda_ext(
                name="sparse_conv_ext",
                module="mmdet3d.ops.spconv",
                extra_include_path=[
                    os.path.abspath(
                        os.path.join(*"mmdet3d.ops.spconv".split("."), "include/")
                    )
                ],
                sources=[
                    "src/all.cc",
                    "src/reordering_cpu.cc",
                    "src/reordering_cuda.cu",
                    "src/indice_cpu.cc",
                    "src/indice_cuda.cu",
                    "src/maxpool_cpu.cc",
                    "src/maxpool_cuda.cu",
                ],
                extra_args=["-w", "-std=c++17"],
            ),
            make_cuda_ext(
                name="bev_pool_ext",
                module="mmdet3d.ops.bev_pool",
                sources=[
                    "src/bev_pool_cpu.cpp",
                    "src/bev_pool_cuda.cu",
                ],
            ),
            make_cuda_ext(
                name="iou3d_cuda",
                module="mmdet3d.ops.iou3d",
                sources=[
                    "src/iou3d.cpp",
                    "src/iou3d_kernel.cu",
                ],
            ),
            make_cuda_ext(
                name="voxel_layer",
                module="mmdet3d.ops.voxel",
                sources=[
                    "src/voxelization.cpp",
                    "src/scatter_points_cpu.cpp",
                    "src/scatter_points_cuda.cu",
                    "src/voxelization_cpu.cpp",
                    "src/voxelization_cuda.cu",
                ],
            ),
            make_cuda_ext(
                name="roiaware_pool3d_ext",
                module="mmdet3d.ops.roiaware_pool3d",
                sources=[
                    "src/roiaware_pool3d.cpp",
                    "src/points_in_boxes_cpu.cpp",
                ],
                sources_cuda=[
                    "src/roiaware_pool3d_kernel.cu",
                    "src/points_in_boxes_cuda.cu",
                ],
            ),
            make_cuda_ext(
                name="ball_query_ext",
                module="mmdet3d.ops.ball_query",
                sources=["src/ball_query_cpu.cpp"],
                sources_cuda=["src/ball_query_cuda.cu"],
            ),
            make_cuda_ext(
                name="knn_ext",
                module="mmdet3d.ops.knn",
                sources=["src/knn_cpu.cpp"],
                sources_cuda=["src/knn_cuda.cu"],
            ),
            make_cuda_ext(
                name="assign_score_withk_ext",
                module="mmdet3d.ops.paconv",
                sources=["src/assign_score_withk.cpp"],
                sources_cuda=["src/assign_score_withk_cuda.cu"],
            ),
            make_cuda_ext(
                name="group_points_ext",
                module="mmdet3d.ops.group_points",
                sources=["src/group_points_cpu.cpp"],
                sources_cuda=["src/group_points_cuda.cu"],
            ),
            make_cuda_ext(
                name="interpolate_ext",
                module="mmdet3d.ops.interpolate",
                sources=["src/interpolate.cpp"],
                sources_cuda=["src/three_interpolate_cuda.cu", "src/three_nn_cuda.cu"],
            ),
            make_cuda_ext(
                name="furthest_point_sample_ext",
                module="mmdet3d.ops.furthest_point_sample",
                sources=["src/furthest_point_sample_cpu.cpp"],
                sources_cuda=["src/furthest_point_sample_cuda.cu"],
            ),
            make_cuda_ext(
                name="gather_points_ext",
                module="mmdet3d.ops.gather_points",
                sources=["src/gather_points_cpu.cpp"],
                sources_cuda=["src/gather_points_cuda.cu"],
            ),
            make_cuda_ext(
                name="feature_decorator_ext",
                module="mmdet3d.ops.feature_decorator",
                sources=["src/feature_decorator.cpp"],
                sources_cuda=["src/feature_decorator_cuda.cu"],
            ),
        ],
        cmdclass={"build_ext": BuildExtension},
        zip_safe=False,
    )
