# emojis/replace_emojis.py

import os
import glob
import json
import re
import random
from typing import Any

# -----------------------------------------------------------------------------
# 配置区，可根据需要调整
# -----------------------------------------------------------------------------

# 待替换的 Emoji 候选池（示例中只列出部分，实际请填入你的完整列表）
EMOJI_POOL = [
    # 食物和饮料相关Emoji (156个)
    "🍎", "🍏", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐",
    "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🫒", "🥑",
    "🍆", "🥔", "🥕", "🌽", "🌶️", "🫑", "🥒", "🥬", "🥦", "🧄",
    "🧅", "🍄", "🥜", "🌰", "🍞", "🥐", "🥖", "🫓", "🥨", "🥯",
    "🥞", "🧇", "🧀", "🍖", "🍗", "🥩", "🥓", "🍔", "🍟", "🍕",
    "🌮", "🌯", "🫔", "🥙", "🧆", "🥚", "🍳", "🥘", "🍲", "🫕",
    "🥣", "🥗", "🍱", "🍘", "🍙", "🍚", "🍛", "🍜", "🍝", "🍠",
    "🍢", "🍣", "🍤", "🍥", "🥮", "🍡", "🥟", "🥠", "🥡", "🦀",
    "🦞", "🦐", "🦑", "🍦", "🍧", "🍨", "🥧", "🍰", "🎂", "🍮",
    "🍭", "🍬", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🧂", "🫘",
    "🍯", "🧈", "🥛", "🍼", "☕", "🫖", "🍵", "🍶", "🍾", "🍷",
    "🍸", "🍹", "🍺", "🍻", "🥂", "🥃", "🥤", "🧋", "🧃", "🧉",
    "🧊", "🥢", "🍽️", "🔪", "🍴", "🥄", "🧂", "🧂", "🧂", "🧂",
    "🍚", "🍜", "🍝", "🍟", "🍔", "🍕", "🌮", "🌯", "🥪", "🥙",
    "🍳", "🍘", "🍙", "🍢", "🍡", "🍧", "🍨", "🍦", "🍰", "🎂",
    "🍬", "🍭", "🍫", "🍿", "🍩", "🍪", "🌰", "🥜", "🧂", "🫘",
    "🍯", "🧈", "🥛", "🍼", "☕", "🫖", "🍵", "🍶", "🍾", "🍷",
    "🍸", "🍹", "🍺", "🍻", "🥂", "🥃", "🥤", "🧋", "🧃", "🧉",
    
    # 动物和自然相关Emoji (182个)
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
    "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🐣",
    "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝",
    "🐛", "🦋", "🐌", "🐞", "🐜", "🕷️", "🦂", "🦟", "🦗", "🐢",
    "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐", "🦀", "🐡", "🐠",
    "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍",
    "🦧", "🦣", "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦬",
    "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🐐", "🦌", "🦙",
    "🦥", "🦘", "🦨", "🦡", "🦃", "🕊️", "🦢", "🦚", "🦜", "🦝",
    "🐕‍🦺", "🦮", "🐕", "🐈", "🐈‍⬛", "🐾", "🌱", "🌲", "🌳", "🌴",
    "🌵", "🌾", "🌿", "🍀", "🍁", "🍃", "🍂", "🌼", "🌻", "🌷",
    "🌹", "🥀", "🌺", "🌸", "💐", "🌱", "🌾", "🌿", "🍀", "🍁",
    "🍃", "🍂", "🌼", "🌻", "🌷", "🌹", "🥀", "🌺", "🌸", "💐",
    "🌎", "🌍", "🌏", "🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓",
    "🌔", "🌙", "🌚", "🌛", "🌜", "🌟", "⭐", "💫", "🌠", "☁️",
    "🌈", "🌤️", "⛅", "🌥️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️", "❄️",
    "☃️", "⛄", "💨", "💧", "💦", "🌊", "🌫️", "🌪️", "🔥", "🗻",
    "🏔️", "🌋", "🗾", "🏝️", "🏜️", "🌅", "🌄", "🌇", "🌆", "🌉",
    "🌌", "🌃", "🌙", "🌚", "🌛", "🌜", "🌟", "⭐", "💫", "🌠",
    "☁️", "🌈", "🌤️", "⛅", "🌥️", "🌦️", "🌧️", "⛈️", "🌩️", "🌨️",
    "❄️", "☃️", "⛄", "💨", "💧", "💦", "🌊", "🌫️", "🌪️", "🔥",
    
    # 旅行和地点相关Emoji (211个)
    "✈️", "🛫", "🛬", "🚁", "🚀", "🛸", "🚢", "🛳️", "⛴️", "🚂",
    "🚅", "🚆", "🚊", "🚉", "🚌", "🚍", "🚎", "🚐", "🚑", "🚒",
    "🚓", "🚔", "🚕", "🚖", "🚗", "🚘", "🚙", "🚚", "🚛", "🚜",
    "🛵", "🚲", "🚏", "⛽", "🚧", "🚨", "🚥", "🚦", "🏮", "🏰",
    "🏯", "🏭", "🏢", "🏬", "🏤", "🏥", "🏦", "🏨", "🏩", "🏪",
    "🏫", "🏭", "🏰", "🗼", "🗽", "🗿", "🗺️", "🗾", "🏝️", "🏜️",
    "🏕️", "🏖️", "🏔️", "🌋", "🗻", "🏞️", "🌅", "🌄", "🌇", "🌆",
    "🌉", "🌌", "🌃", "🏙️", "🌃", "🏙️", "🌆", "🌉", "🌅", "🌄",
    "🌇", "🌌", "🗺️", "🗾", "🏝️", "🏜️", "🏕️", "🏖️", "🏔️", "🌋",
    "🗻", "🏞️", "🌅", "🌄", "🌇", "🌆", "🌉", "🌌", "🌃", "🏙️",
    "🚪", "🛏️", "🛋️", "🪑", "🪜", "🚽", "🛁", "🛀", "🚿", "🧽",
    "🧴", "🧼", "🪥", "🪒", "🪞", "🛍️", "🛒", "🛎️", "📺", "📷",
    "📸", "🎥", "🎞️", "📽️", "💿", "💽", "💾", "📀", "🖥️", "💻",
    "🖨️", "🖱️", "🖲️", "🗄️", "📅", "📆", "📇", "📈", "📉", "📊",
    "📋", "📌", "📍", "📎", "📏", "📐", "✂️", "🖍️", "🖊️", "🖋️",
    "✒️", "📝", "📄", "📰", "📑", "📓", "📔", "📕", "📖", "📗",
    "📘", "📙", "📚", "📛", "🔖", "🏷️", "🎫", "🎟️", "🎫", "🎟️",
    "🏆", "🥇", "🥈", "🥉", "🏅", "🎖️", "🎗️", "🏵️", "🌹", "🌺",
    "🌸", "💐", "🌼", "🌻", "🌷", "🥀", "🍁", "🍂", "🍃", "🍀",
    "🌿", "🌾", "🌵", "🌴", "🌳", "🌲", "🌱", "💫", "🌟", "⭐",
    "🌠", "🌌", "🌃", "🌆", "🌇", "🌄", "🌅", "🏙️", "🌉", "🗾",
    "🏝️", "🏜️", "🏕️", "🏖️", "🏔️", "🌋", "🗻", "🏞️", "🗺️", "🗿",
    "🗽", "🗼", "🏰", "🏯", "🏨", "🏩", "🏬", "🏤", "🏥", "🏦",
    "🏪", "🏫", "🏭", "🚉", "🚊", "🚆", "🚅", "🚂", "🚢", "🛳️",
    "⛴️", "🚁", "✈️", "🛫", "🛬", "🚀", "🛸"
]

# 精确匹配单个 Emoji 的正则（涵盖常用 Unicode Block）
EMOJI_PATTERN = re.compile(
    r'['
    u'\U0001F300-\U0001F5FF'
    u'\U0001F600-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\U0001F1E0-\U0001F1FF'
    u'\u2600-\u27BF'
    r']',
    flags=re.UNICODE
)

# 输入、输出目录
INPUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(INPUT_DIR, "output")


# -----------------------------------------------------------------------------
# 工具函数
# -----------------------------------------------------------------------------

def collect_all_strings(obj: Any, collector: list):
    """
    递归遍历 JSON 结构，将所有字符串值加入 collector 列表。
    """
    if isinstance(obj, dict):
        for v in obj.values():
            collect_all_strings(v, collector)
    elif isinstance(obj, list):
        for item in obj:
            collect_all_strings(item, collector)
    elif isinstance(obj, str):
        collector.append(obj)


def replace_in_string(s: str, replacements: dict) -> str:
    """
    在单个字符串中，使用预先准备好的 replacements 映射表替换所有 Emoji。
    """
    def _sub(m):
        old = m.group(0)
        # 每次匹配取出队列中下一个 new emoji
        return replacements.pop(0)
    return EMOJI_PATTERN.sub(_sub, s)


def traverse_and_replace(obj: Any, replacements: list) -> Any:
    """
    递归遍历 JSON，遇到字符串就调用 replace_in_string，替换队列中的 Emoji。
    """
    if isinstance(obj, dict):
        return {k: traverse_and_replace(v, replacements) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [traverse_and_replace(item, replacements) for item in obj]
    elif isinstance(obj, str):
        return replace_in_string(obj, replacements)
    else:
        return obj


# -----------------------------------------------------------------------------
# 主处理逻辑
# -----------------------------------------------------------------------------

def process_file(input_path: str, output_path: str):
    # 1. 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 2. 读取并解析 JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 3. 收集所有字符串，统计要替换的 Emoji 总数
    all_strings = []
    collect_all_strings(data, all_strings)

    emoji_count = 0
    for s in all_strings:
        emoji_count += len(EMOJI_PATTERN.findall(s))

    if emoji_count == 0:
        print(f"[跳过] 文件 {os.path.basename(input_path)} 中无 Emoji。")
        return

    # 4. 从候选池中随机选取 emoji_count 个不重复的 Emoji
    if emoji_count > len(EMOJI_POOL):
        raise ValueError(
            f"需要替换 {emoji_count} 个 Emoji，但候选池中只有 {len(EMOJI_POOL)} 个，请扩充候选池。"
        )

    replacements = random.sample(EMOJI_POOL, k=emoji_count)
    # 转为可 pop 的队列
    replacements = list(replacements)

    # 5. 递归替换
    new_data = traverse_and_replace(data, replacements)

    # 6. 写回 JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print(f"[完成] {os.path.basename(input_path)} → {os.path.basename(output_path)} 替换了 {emoji_count} 个 Emoji")


def main():
    # 查找所有 .json 文件
    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    if not json_files:
        print("在目录中未找到任何 .json 文件")
        return

    # 处理每个文件
    for path in json_files:
        filename = os.path.basename(path)
        out_path = os.path.join(OUTPUT_DIR, filename)
        process_file(path, out_path)

    print("所有文件处理完成。")


if __name__ == "__main__":
    main()
