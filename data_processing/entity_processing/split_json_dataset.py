# 将一个 JSON 文件数据按照 8:1:1 的比例划分为训练集、验证集和测试集。

import json


def split_json_file(input_file_path, output_file_paths, ratios):
    """
    将一个JSON文件的数据按照指定比例分成多个文件，不打乱数据顺序。

    :param input_file_path: 输入的JSON文件路径
    :param output_file_paths: 输出文件路径列表
    :param ratios: 分割比例列表，例如 [8, 1, 1]
    """
    # 读取原始JSON文件
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 确保数据是列表形式
    if not isinstance(data, list):
        raise ValueError("JSON文件中的数据必须是列表形式")

    # 计算每个文件的数据量
    total_count = len(data)
    ratios_sum = sum(ratios)
    splits = [int(total_count * ratio / ratios_sum) for ratio in ratios]

    # 调整最后一个文件的数量，以确保总数不变
    splits[-1] = total_count - sum(splits[:-1])

    # 分割数据
    split_data = []
    start = 0
    for split in splits:
        end = start + split
        split_data.append(data[start:end])
        start = end

    # 将分割后的数据写入新的JSON文件
    for output_path, data_part in zip(output_file_paths, split_data):
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data_part, file, ensure_ascii=False, indent=4)
        print(f"已将数据写入 {output_path}")


# 主函数
def main():
    input_file_path = '../output.json'  # 输入的JSON文件路径
    output_file_paths = ['train.json', 'valid.json', 'test.json']  # 输出的三个文件路径
    ratios = [8, 1, 1]  # 分割比例

    split_json_file(input_file_path, output_file_paths, ratios)


if __name__ == "__main__":
    main()