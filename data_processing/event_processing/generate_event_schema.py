# 从训练数据中提取所有“事件类型 + 角色”，生成一个标准的 event_schema.jsonl 文件。
import json
import hashlib
import os

def generate_event_schema(train_file_path, output_file_path):
    event_schemas = {}
    if not os.path.exists(train_file_path):
        print(f"错误：训练文件 {train_file_path} 不存在。")
        # 创建一个空的 train.json 以便后续步骤不报错，但提示用户
        with open(train_file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"已创建空的 {train_file_path}。请确保您提供正确的 train.json 文件路径并填充内容。")
        # 即使train.json为空，也尝试生成一个空的schema文件结构，避免后续脚本出错
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            pass #写入空文件
        return

    try:
        with open(train_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if 'event_list' in data:
                        for event in data['event_list']:
                            event_type = event.get('event_type')
                            if not event_type:
                                continue

                            if event_type not in event_schemas:
                                event_schemas[event_type] = {'roles': set(), 'class': event_type.split('-')[0] if '-' in event_type else event_type}
                            
                            for argument in event.get('arguments', []):
                                role = argument.get('role')
                                if role:
                                    event_schemas[event_type]['roles'].add(role)
                except json.JSONDecodeError as e:
                    print(f"解析行时发生JSON解码错误: {line.strip()}, 错误: {e}")
                    continue # 跳过无法解析的行
    except FileNotFoundError:
        print(f"错误：训练文件 {train_file_path} 未找到。")
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            pass #写入空文件
        return
    except Exception as e:
        print(f"处理训练文件时发生错误: {e}")
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            pass #写入空文件
        return

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', encoding='utf-8') as f_out:
        # 为了与原始文件顺序一致，最好对event_types进行排序，如果原始文件有特定顺序的话
        # DuEE的event_schema.json似乎是按某种类别排序，然后是类型。这里简单按event_type字符串排序
        sorted_event_types = sorted(event_schemas.keys())

        for event_type in sorted_event_types:
            schema_info = event_schemas[event_type]
            role_list = sorted(list(schema_info['roles'])) # 角色也排序以保持一致性
            output_dict = {
                "event_type": event_type,
                "role_list": [{"role": r} for r in role_list],
                "id": hashlib.md5(event_type.encode('utf-8')).hexdigest(),
                "class": schema_info['class']
            }
            f_out.write(json.dumps(output_dict, ensure_ascii=False) + '\n')
    print(f"event_schema.json 已生成在: {output_file_path}")

if __name__ == '__main__':
    # 假设 train.json 与脚本在同一目录或指定路径
    # 在实际的 Manus 环境中, 路径会是绝对路径
    # train_json_path = '/home/ubuntu/duee_data/raw/duee_train.json' # 使用解压后的路径
    # output_schema_path = '/home/ubuntu/duee_generation_scripts/event_schema.json'
    
    # 从环境变量或参数获取路径是更稳健的做法，这里为了简单直接指定
    # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 默认train.json在上一级的 duee_data/raw/ 目录下
    # 默认输出在当前脚本目录
    default_train_json_path = os.path.join(script_dir, '../..', 'duee_data', 'raw', 'duee_train.json')
    default_output_schema_path = os.path.join(script_dir, 'event_schema.json')

    # 优先使用环境变量指定的路径（如果设置了）
    train_json_path = os.environ.get('TRAIN_JSON_PATH', default_train_json_path)
    output_schema_path = os.environ.get('OUTPUT_SCHEMA_PATH', default_output_schema_path)
    
    # 确保 Manus 环境中的路径是绝对的
    # 这里硬编码为 Manus 环境的路径
    train_json_path = 'admin.jsonl'
    output_schema_path = 'event_schema.jsonl'

    generate_event_schema(train_json_path, output_schema_path)

