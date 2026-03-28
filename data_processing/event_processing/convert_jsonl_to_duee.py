# 把原始的 JSONL 数据转换成 DuEE 事件抽取格式的数据
import json

# 定义触发事件类型
event_trigger_labels = ["恶意软件投递", "开源工具武器化", "恶意文档利用", "钓鱼攻击", "社会工程学攻击"]

def tokenize(text):
    return list(text)  # 每个字符一个token，符合DuEE标准

def convert_to_duee_format_strict(sample):
    text = sample["text"]
    entities = sample["entities"]
    event_list = []

    for trigger_entity in entities:
        if trigger_entity["label"] in event_trigger_labels:
            trigger_type = trigger_entity["label"]
            trigger_text = text[trigger_entity["start_offset"]:trigger_entity["end_offset"]]
            trigger_start_index = trigger_entity["start_offset"]  # token index就是字符位置

            arguments = []
            for arg_entity in entities:
                if arg_entity["id"] != trigger_entity["id"]:
                    arg_text = text[arg_entity["start_offset"]:arg_entity["end_offset"]]
                    arg_start_index = arg_entity["start_offset"]
                    arguments.append({
                        "role": arg_entity["label"],
                        "argument": arg_text,
                        "argument_start_index": arg_start_index,
                        "alias": []
                    })

            event_list.append({
                "event_type": trigger_type,
                "trigger": trigger_text,
                "trigger_start_index": trigger_start_index,
                "arguments": arguments,
                "class": trigger_type
            })

    return {
        "id": str(sample["id"]),
        "text": text,
        "event_list": event_list
    }

def process_jsonl(input_file_path, output_file_path):
    # 打开输入和输出文件
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:

        # 逐行处理每一条数据
        for line in input_file:
            sample = json.loads(line.strip())  # 读取一行并解析为字典
            converted_sample = convert_to_duee_format_strict(sample)  # 转换为 DuEE 格式
            output_file.write(json.dumps(converted_sample, ensure_ascii=False) + '\n')  # 写入输出文件

# 替换为你的文件路径
input_file_path = 'admin.jsonl'  # 输入文件路径
output_file_path = 'admin2.jsonl'  # 输出文件路径

# 执行批量转换
process_jsonl(input_file_path, output_file_path)
