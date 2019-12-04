import os
import shutil

# 基础反转义函数
def iner_escape_reverse(stream=str):
    """
    反转义函数，将每一条记录数据反转义并返回
    :param stream: 输入十六进制字节字符串
    :return: 返回反转义后的
    """
    # 首先检测帧头帧尾
    if stream[:2] == '7E' and stream[(len(stream)-2):] =='7F':
        pass
    else:
        print('--->err stream: '+stream)
        return ''
    ori_bytes_str = stream[2:(len(stream)-2)]

    if '7E' in ori_bytes_str:
        idx1 = ori_bytes_str.index('7E')
        if idx1 % 2 == 0:
           print('fatal error!')
        else:
            pass
    # 转义内容
    for idx in range(0, len(ori_bytes_str), 2):
        tmp = ori_bytes_str[idx:idx+2]
        if '7D' == tmp:
            ori_bytes_str = ori_bytes_str[:idx+1] + ori_bytes_str[idx+3:]
        else:
            pass
    return '7E'+ori_bytes_str+'7F'


# 基础遍历文件函数
def get_file_list(fileList, rootPath, fileType=None):
    """
    根据输入的根路径，向下递归搜索文件名
    :param fileList: 输出的文件列表
    :param rootPath: 输入的查询父目录
    :param fileType: 查询文件的后缀名
    :return:
    """
    files = os.listdir(rootPath)
    for fileName in files:
        fullPath = os.path.join(rootPath, fileName)
        if os.path.isdir(fullPath):
            get_file_list(fileList, fullPath, fileType)
        else:
            if fileType:  # 如果指定文件后缀
                if fileType == fullPath[-len(fileType):]:    # 检查后缀名
                    fileList.append(fullPath)
                else:
                    print(fullPath)
            else:
                # 如果不指定则添加所有
                fileList.append(fullPath)
                print(fullPath)
    return fileList


# 基础遍历文件函数
def get_dir_list(dirList, rootPath):
    """
    根据输入的根路径，向下递归搜索文件名
    :param fileList: 输出的文件列表
    :param rootPath: 输入的查询父目录
    :return:
    """
    files = os.listdir(rootPath)
    for fileName in files:
        fullPath = os.path.join(rootPath, fileName)
        if os.path.isdir(fullPath):
            # 添加文件目录
            dirList.append(fullPath)
            # 继续向下搜索
            get_dir_list(dirList, fullPath)
    return dirList


# 重写copy函数，用于拷贝目录或拷贝文件
# 可以参考copy2和copy函数，复制所有文件和状态
def copy_func(src, dst, *, follow_symlinks=True):
    # 如果输入路径是目录，首先创建目标目录
    if os.path.isdir(src):
        dst_path = os.path.join(dst, os.path.basename(dst))     # 定义目的基础目录
        # 这里不复制文件和状态
        # 所以只复制了文件路径
    return dst


# 将输入路径整体复制到指定路径下
def copy_file_dir(src_path=str, dst_path=str, include_file=bool):
    """
    将指定的路径子目录复制到指定路径下（指定是否包含文件）
    :param src_path: 被复制源路径
    :param dst_path: 复制到目的路径
    :param include_file: 是否复制文件
    :return: 无
    """
    # 检查是否要拷贝
    shutil.copytree(src_path, dst_path, symlinks=False, ignore=None, copy_function=copy_func,
                    ignore_dangling_symlinks=True)
