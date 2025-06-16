from PIL import Image
import os
from pathlib import Path
import argparse

def compress_image(input_path, output_path, target_size=(24, 24), quality=85, optimize=True):
    """
    压缩单张图片为24x24像素并保留关键特征

    参数:
    input_path: 输入图片路径
    output_path: 输出图片路径
    target_size: 目标尺寸 (宽, 高)，固定为24x24
    quality: JPEG压缩质量 (1-100)
    optimize: 是否启用JPEG优化

    返回:
    压缩后的图片对象和文件大小信息
    """
    try:
        # 创建输出目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 打开原始图像
        img = Image.open(input_path)

        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 高质量下采样到24x24
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # 保存压缩后图像
        img.save(output_path,
                 format='JPEG',
                 quality=quality,
                 optimize=optimize,
                 subsampling=0)  # 保持4:4:4色度采样

        # 返回压缩信息
        original_size = os.path.getsize(input_path) / 1024
        compressed_size = os.path.getsize(output_path) / 1024
        compression_ratio = (1 - compressed_size/original_size) * 100

        print(f"压缩成功: {os.path.basename(input_path)} "
              f"| 尺寸: {img.size} "
              f"| 大小: {original_size:.1f}KB → {compressed_size:.1f}KB "
              f"| 压缩率: {compression_ratio:.1f}%")

        return img, compressed_size

    except Exception as e:
        print(f"处理失败 {input_path}: {e}")
        return None, 0

def compress_folder(input_dir, output_dir, target_size=(24, 24), quality=85, extensions=None):
    """
    压缩整个文件夹中的图片为24x24像素

    参数:
    input_dir: 输入文件夹路径
    output_dir: 输出文件夹路径
    target_size: 目标尺寸固定为24x24
    quality: 压缩质量 (1-100)
    extensions: 要处理的文件扩展名列表
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']

    # 支持的图片格式
    extensions = [ext.lower() for ext in extensions]

    total_original = 0
    total_compressed = 0
    processed_count = 0

    # 遍历输入目录
    for root, _, files in os.walk(input_dir):
        for file in files:
            # 检查文件扩展名
            if Path(file).suffix.lower() in extensions:
                input_path = os.path.join(root, file)

                # 保持相对路径结构
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)

                # 压缩图片为24x24
                _, compressed_size = compress_image(
                    input_path,
                    output_path,
                    target_size=target_size,
                    quality=quality
                )

                if compressed_size > 0:
                    total_original += os.path.getsize(input_path) / 1024
                    total_compressed += compressed_size
                    processed_count += 1

    # 打印汇总信息
    if processed_count > 0:
        print("\n===== 压缩汇总 =====")
        print(f"处理图片数量: {processed_count}")
        print(f"总大小: {total_original:.1f}KB → {total_compressed:.1f}KB")
        print(f"平均压缩率: {(1 - total_compressed/total_original)*100:.1f}%")
        print(f"节省空间: {total_original - total_compressed:.1f}KB")
    else:
        print("未找到可处理的图片文件")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='图片批量压缩工具 (24x24像素)')
    parser.add_argument('input',
                        nargs='?',
                        help='输入文件或文件夹路径 (默认: %(default)s)',
                        default=r'D:\python\end_of_term\ChatPhoto\photo\SVM_classification\fish')

    parser.add_argument('output',
                        nargs='?',
                        help='输出文件或文件夹路径 (默认: %(default)s)',
                        default=r'D:\python\end_of_term\ChatPhoto\photo\zip_photo\fish')

    # 移除尺寸参数，固定为24x24
    parser.add_argument('--quality', type=int, default=85,
                        help='JPEG质量 (1-100)，默认85')

    parser.add_argument('--ext', nargs='+', default=['.jpg', '.jpeg', '.png'],
                        help='处理的文件扩展名，默认 jpg jpeg png')

    args = parser.parse_args()

    # 确定是文件还是文件夹
    if os.path.isfile(args.input):
        # 单个文件处理
        compress_image(
            args.input,
            args.output,
            target_size=(24, 24),  # 固定为24x24
            quality=args.quality
        )
    elif os.path.isdir(args.input):
        # 文件夹批量处理
        compress_folder(
            args.input,
            args.output,
            target_size=(24, 24),  # 固定为24x24
            quality=args.quality,
            extensions=args.ext
        )
    else:
        print(f"错误: 路径不存在 {args.input}")

if __name__ == "__main__":
    main()