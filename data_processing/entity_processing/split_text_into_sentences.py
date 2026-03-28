# 按句号分句 + 每句单独成行
def split_sentences_to_new_file(input_file, output_file):
    try:
        # 读取输入文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 按句号分割句子
        sentences = content.split("。")

        # 过滤空字符串，并确保每个句子以句号结尾
        sentences = [sentence.strip() + "。" for sentence in sentences if sentence.strip()]

        # 将句子写入新的输出文件，每个句子占一行
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                f.write(sentence + "\n")

        print(f"处理完成！句子已分割并保存到文件：{output_file}")
    except FileNotFoundError:
        print(f"错误：文件 {input_file} 未找到，请检查文件路径是否正确。")
    except Exception as e:
        print(f"发生错误：{e}")


# 示例用法
input_file = "1-5正式标注.txt"  # 输入文件名
output_file = "1-5output_sentences.txt"  # 输出文件名
split_sentences_to_new_file(input_file, output_file)