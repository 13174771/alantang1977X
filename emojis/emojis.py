import os
import json
import random
import re

# 完整的 Unicode Emoji 列表（收录常用表情、人物、动物、物品、旗帜等，可根据需要继续扩充）
ALL_EMOJIS = [
    "😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "😘", "🥰",
    "😗", "😙", "😚", "🙂", "🤗", "🤩", "🤔", "🤨", "😐", "😑", "😶", "🙄", "😏", "😣", "😥",
    "😮", "🤐", "😯", "😪", "😫", "🥱", "😴", "😌", "😛", "😜", "😝", "🤤", "😒", "😓", "😔",
    "😕", "🙃", "🤑", "😲", "☹️", "🙁", "😖", "😞", "😟", "😤", "😢", "😭", "😦", "😧", "😨",
    "😩", "🤯", "😬", "😰", "😱", "🥵", "🥶", "😳", "🤪", "😵", "😡", "😠", "🤬", "😷", "🤒",
    "🤕", "🤢", "🤮", "🤧", "😇", "🥳", "🥺", "🥲", "🤠", "🥸", "🤓", "🧐", "🫠", "🤖", "👻",
    "💀", "☠️", "👽", "👾", "👹", "👺", "💩", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
    "😾", "🙈", "🙉", "🙊", "🐵", "🐒", "🦍", "🦧", "🐶", "🐕", "🦮", "🐕‍🦺", "🐩", "🐺", "🦊",
    "🦝", "🐱", "🐈", "🐈‍⬛", "🦁", "🐯", "🐅", "🐆", "🐴", "🦄", "🐮", "🐂", "🐃", "🐄", "🐷",
    "🐖", "🐗", "🐽", "🐏", "🐑", "🐐", "🐪", "🐫", "🦙", "🦒", "🐘", "🦣", "🦏", "🦛", "🐭",
    "🐁", "🐀", "🐹", "🐰", "🐇", "🐿️", "🦫", "🦔", "🦇", "🐻", "🐻‍❄️", "🐨", "🐼", "🦥", "🦦",
    "🦨", "🦘", "🦡", "🐾", "🦃", "🐔", "🐓", "🐣", "🐤", "🐥", "🐦", "🐧", "🕊️", "🦅", "🦆",
    "🦢", "🦉", "🦩", "🦚", "🦜", "🦤", "🦥", "🦦", "🦨", "🦩", "🦪", "🦑", "🦐", "🦞", "🦀",
    "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🧑‍💻",
    "👨‍💻", "👩‍💻", "👨‍🔬", "👩‍🔬", "👨‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "👨‍⚕️", "👩‍⚕️", "👨‍🍳",
    "👩‍🍳", "👨‍✈️", "👩‍✈️", "👮‍♂️", "👮‍♀️", "🕵️‍♂️", "🕵️‍♀️", "💂‍♂️", "💂‍♀️", "🕵️", "👷‍♂️",
    "👷‍♀️", "👷", "🤴", "👸", "👳‍♂️", "👳‍♀️", "👲", "🧕", "🧑‍🎤", "👨‍🎤", "👩‍🎤", "👨‍🎨", "👩‍🎨",
    "🧑‍🚀", "👨‍🚀", "👩‍🚀", "🧑‍🚒", "👨‍🚒", "👩‍🚒", "🧑‍⚖️", "👨‍⚖️", "👩‍⚖️",
    "⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏉", "🥏", "🎱", "🏓", "🏸", "🥅", "🏒", "🏑", "🥍",
    "🏏", "⛳", "🏹", "🎣", "🤿", "🥊", "🥋", "🎽", "🛹", "🛷", "⛸️", "🥌", "🛶", "⛵", "🚤",
    "🛥️", "🛳️", "⛴️", "🚢", "✈️", "🛩️", "🚁", "🚟", "🚠", "🚡", "🚀", "🛸",
    "❤️", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣️", "💕", "💞", "💓", "💗", "💖",
    "💘", "💝", "💟", "☮️", "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐",
    "⛎", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓", "🆔", "⚛️", "🉑",
    "🏳️", "🏴", "🏁", "🚩", "🏳️‍🌈", "🏳️‍⚧️", "🇨🇳", "🇺🇸", "🇬🇧", "🇫🇷", "🇯🇵", "🇰🇷", "🇩🇪", "🇷🇺", "🇮🇳"
]

# Emoji正则表达式，精准匹配所有emoji（支持单字符和复合emoji，适配多种Unicode区段）
EMOJI_PATTERN = re.compile(
    "[" +
    "\U0001F600-\U0001F64F" +  # 表情
    "\U0001F300-\U0001F5FF" +  # 符号和象形文字
    "\U0001F680-\U0001F6FF" +  # 交通运输
    "\U0001F1E0-\U0001F1FF" +  # 旗帜
    "\U00002700-\U000027BF" +  # Dingbats
    "\U0001F900-\U0001F9FF" +  # 补充表情
    "\U00002600-\U000026FF" +  # 杂项符号
    "\U0001F700-\U0001F77F" +  # 炼金术符号
    "\U0001FA70-\U0001FAFF" +  # 补充象形文字
    "\U0001F780-\U0001F7FF" +  # 几何扩展
    "\U0001F800-\U0001F8FF" +  # 补充箭头
    "\U0001FA00-\U0001FA6F" +  # 国际象棋符号
    "]+", flags=re.UNICODE
)

def random_emoji():
    """
    随机返回一个新的emoji表情
    """
    return random.choice(ALL_EMOJIS)

def replace_emojis_in_str(s):
    """
    将字符串中所有emoji精准替换为随机新emoji（数量、位置不变）
    """
    def repl(match):
        return random_emoji()
    return EMOJI_PATTERN.sub(repl, s)

def process_json_emojis(obj):
    """
    递归遍历JSON对象，对所有字符串字段中的emoji精准替换
    """
    if isinstance(obj, dict):
        return {k: process_json_emojis(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_json_emojis(i) for i in obj]
    elif isinstance(obj, str):
        return replace_emojis_in_str(obj)
    else:
        return obj

def update_emojis_in_json_file(input_path, output_path):
    """
    处理单个json文件，将其中所有emoji替换后写入output_path
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {input_path}, 错误: {e}")
        return

    new_data = process_json_emojis(data)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        print(f"已生成文件: {output_path}")
    except Exception as e:
        print(f"写入文件失败: {output_path}, 错误: {e}")

def main():
    """
    主程序，自动查找并处理emojis文件夹下所有json文件，将结果输出到output目录下（可覆盖旧文件）
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    emojis_dir = base_dir
    output_dir = os.path.join(emojis_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(emojis_dir):
        if file.endswith('.json'):
            input_path = os.path.join(emojis_dir, file)
            output_path = os.path.join(output_dir, file)
            update_emojis_in_json_file(input_path, output_path)

if __name__ == "__main__":
    main()
