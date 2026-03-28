import json


# 定义一个函数来转换JSONL格式到目标JSON格式
def convert_jsonl_to_json(jsonl_data):
    result = []
    for item in jsonl_data:
        sentence = item["text"]
        entities = item["entities"]
        relations = item["relations"]

        for relation in relations:
            from_entity = next((e for e in entities if e["id"] == relation["from_id"]), None)
            to_entity = next((e for e in entities if e["id"] == relation["to_id"]), None)

            if from_entity and to_entity:
                head = sentence[from_entity["start_offset"]:from_entity["end_offset"]]
                tail = sentence[to_entity["start_offset"]:to_entity["end_offset"]]
                head_offset = from_entity["start_offset"]
                tail_offset = to_entity["start_offset"]
                relation_type = relation["type"]

                result.append({
                    "sentence": sentence,
                    "relation": relation_type,
                    "head": head,
                    "head_offset": head_offset,
                    "tail": tail,
                    "tail_offset": tail_offset
                })
    return result


# 读取JSONL文件
def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data


# 将结果写入JSON文件
def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 主函数
def main():
    input_file_path = '../admin.jsonl'  # 输入的JSONL文件路径
    output_file_path = '../output.json'  # 输出的JSON文件路径

    # 读取JSONL文件
    jsonl_data = read_jsonl_file(input_file_path)

    # 转换格式
    converted_data = convert_jsonl_to_json(jsonl_data)

    # 写入JSON文件
    write_json_file(output_file_path, converted_data)

    print(f"转换完成，结果已保存到 {output_file_path}")


if __name__ == "__main__":
    main()