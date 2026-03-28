# 把 Doccano 标注工具导出的 JSONL 数据转换为 BIO 格式（用于命名实体识别 NER 任务），并保存为文本文件。
import json


def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)


def doccano2BIO(file_name, output_file='out.txt'):
    def _get_pair():
        data = load_jsonl(file_name)
        for line in data:
            text = line['text']
            labels = ['O'] * len(text)
            for ent in line['entities']:
                label, start_offset, end_offset = ent['label'], ent['start_offset'], ent['end_offset']
                labels[start_offset] = 'B-' + label
                labels[start_offset + 1: end_offset] = ['I-' + label] * (end_offset - start_offset - 1)
            yield text, labels

    # 显式指定写入文件的编码为 UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        for text, labels in _get_pair():
            item = zip(list(text), labels)
            for char, label in item:
                f.write(f"{char} {label}\n")
            f.write("\n")  # 在每个句子之间添加空行分隔


if __name__ == '__main__':
    doccano2BIO('valid.jsonl', 'valid.txt')
