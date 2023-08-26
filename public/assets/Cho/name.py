import os

def count_pngs_in_directory(dir_path):
    """统计指定目录内的png图片数量"""
    return len([f for f in os.listdir(dir_path) if f.endswith('.png')])

def main():
    # 获取当前目录下的所有文件和文件夹
    for root, dirs, files in os.walk("."):
        # 遍历子文件夹
        for dir_name in dirs:
            full_dir_path = os.path.join(root, dir_name)
            # 计算该文件夹内的png图片数量
            png_count = count_pngs_in_directory(full_dir_path)
            
            # 将数量保存到number.txt中
            with open(os.path.join(full_dir_path, "number.txt"), 'w') as file:
                file.write(str(png_count))

if __name__ == '__main__':
    main()
