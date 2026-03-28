# 将一个 CSV 文件从一种编码格式转换为另一种编码格式（默认从 GBK 转为 UTF-8）。
import csv


def convert_encoding(input_file, output_file, from_encoding='gbk', to_encoding='utf-8'):
    with open(input_file, 'r', encoding=from_encoding) as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    with open(output_file, 'w', encoding=to_encoding, newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


# 使用示例
input_file = 'relation.csv'  # 输入文件路径
output_file = 'output.csv'  # 输出文件路径
convert_encoding(input_file, output_file)

