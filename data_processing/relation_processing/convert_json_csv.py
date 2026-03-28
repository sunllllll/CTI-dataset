import json
import csv


def json2csv(fp_json, fp_csv):
    """
    将 JSON 文件转换为 CSV 文件。

    参数:
        fp_json (str): JSON 文件的路径。
        fp_csv (str): 要生成的 CSV 文件的路径。
    """
    try:
        # 打开 JSON 文件并加载数据
        with open(fp_json, encoding='utf-8') as f1:
            data = json.load(f1)

        # 检查 JSON 数据是否是一个列表
        if not isinstance(data, list):
            raise ValueError("JSON 数据必须是一个列表，每个元素是一个字典。")

        # 检查列表是否为空
        if len(data) == 0:
            raise ValueError("JSON 数据为空，无法转换为 CSV。")

        # 获取字段名（假设所有字典的字段名一致）
        fieldnames = data[0].keys()

        # 打开 CSV 文件并写入数据
        with open(fp_csv, 'w', encoding='utf-8', newline='') as f2:
            writer = csv.DictWriter(f2, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"转换完成，CSV 文件已保存到 {fp_csv}")

    except FileNotFoundError:
        print(f"错误：文件 {fp_json} 未找到，请检查文件路径是否正确。")
    except json.JSONDecodeError:
        print(f"错误：文件 {fp_json} 的 JSON 格式无效。")
    except ValueError as ve:
        print(f"错误：{ve}")
    except Exception as e:
        print(f"发生未知错误：{e}")


# 示例用法
if __name__ == "__main__":
    json_file_path = "test.json"  # 替换为你的 JSON 文件路径
    csv_file_path = "test.csv"  # 替换为你想要保存的 CSV 文件路径
    json2csv(json_file_path, csv_file_path)