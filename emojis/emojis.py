import os
import glob
import json
import re
import random
from typing import Any, List

# -----------------------------------------------------------------------------
# Emoji 候选池：请在此处填入你的完整列表，共数百个
# -----------------------------------------------------------------------------
EMOJI_POOL: List[str] = [
    # 样例：请根据需要完整填写
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
    "⛴️", "🚁", "✈️", "🛫", "🛬", "🚀", "🛸",
    # 如需更多请自行扩充
]

# 精确匹配单个 Emoji 的正则（Unicode 常用块）
EMOJI_PATTERN = re.compile(
    r'('
    u'[\U0001F300-\U0001F5FF]'
    u'|[\U0001F600-\U0001F64F]'
    u'|[\U0001F680-\U0001F6FF]'
    u'|[\U0001F1E0-\U0001F1FF]'
    u'|[\u2600-\u27BF]'
    r')',
    flags=re.UNICODE
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = BASE_DIR
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def find_emojis_in_head(text: str) -> List[str]:
    """
    查找文本第一段（第一个 '┃' 前）中的所有 Emoji。
    """
    head = text.split('┃', 1)[0]
    return [m.group(0) for m in EMOJI_PATTERN.finditer(head)]


def collect_all_emojis(obj: Any, key: str = "name") -> List[str]:
    """
    递归收集所有 dict 中 key="name" 第一段的 Emoji，保持顺序。
    """
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and isinstance(v, str):
                found.extend(find_emojis_in_head(v))
            else:
                found.extend(collect_all_emojis(v, key))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(collect_all_emojis(item, key))
    return found


def precise_replace_head_emojis(text: str, new_emojis: List[str]) -> str:
    """
    只替换文本第一段（第一个 '┃' 前）中的 Emoji，且一一对应、精准替换。
    """
    head, *tail = text.split('┃', 1)
    matches = list(EMOJI_PATTERN.finditer(head))
    if len(matches) != len(new_emojis):
        raise ValueError("Emoji数目不一致，无法精准替换。")
    # 替换时倒序处理，防止下标偏移
    head_list = list(head)
    for match, new_emoji in zip(reversed(matches), reversed(new_emojis)):
        start, end = match.span()
        head_list[start:end] = [new_emoji]
    new_head = ''.join(head_list)
    return new_head + ('┃' + tail[0] if tail else '')


def replace_name_head_emojis(obj: Any, new_emojis: List[str], key: str = "name"):
    """
    递归精准替换所有 dict 中 key="name" 第一段的 Emoji，保持 Emoji 数量不变，顺序一致。
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and isinstance(v, str):
                old_count = len(find_emojis_in_head(v))
                this_new = [new_emojis.pop(0) for _ in range(old_count)]
                obj[k] = precise_replace_head_emojis(v, this_new)
            else:
                replace_name_head_emojis(v, new_emojis, key)
    elif isinstance(obj, list):
        for item in obj:
            replace_name_head_emojis(item, new_emojis, key)


def process_file(input_path: str, output_path: str):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. 读取 JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[错误] 无法解析 JSON 文件 {os.path.basename(input_path)}: {e}")
        return False

    # 2. 收集所有需要替换的 emoji
    old_emojis = collect_all_emojis(data)
    total = len(old_emojis)
    if total == 0:
        print(f"[跳过] `{os.path.basename(input_path)}` 中 “name” 字段第一段无 Emoji。")
        return False

    # 3. 检查 Emoji 池是否充足
    if total > len(set(EMOJI_POOL)):
        print(f"[错误] 需要替换 {total} 个 Emoji，但池中只有 {len(set(EMOJI_POOL))} 个，请补充 EMOJI_POOL。")
        return False

    # 4. 随机抽取不重复的新 Emoji
    new_emojis = random.sample(list(set(EMOJI_POOL)), k=total)

    # 5. 替换
    data_copy = json.loads(json.dumps(data, ensure_ascii=False))  # 深拷贝
    replace_name_head_emojis(data_copy, new_emojis.copy())

    # 6. 写文件（如内容有变化才写）
    orig_json = json.dumps(data, ensure_ascii=False, indent=2)
    new_json = json.dumps(data_copy, ensure_ascii=False, indent=2)
    if orig_json != new_json:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_json)
        print(f"[完成] `{os.path.basename(input_path)}` → `{os.path.basename(output_path)}`，已精准替换 {total} 个 Emoji")
        return True
    else:
        print(f"[无变化] `{os.path.basename(input_path)}` Emoji 替换后内容无变化。")
        return False


def main():
    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    if not json_files:
        print("⚠️ 未找到任何 .json 文件。")
        return

    changed_files = []
    for path in json_files:
        fname = os.path.basename(path)
        out = os.path.join(OUTPUT_DIR, fname)
        changed = process_file(path, out)
        if changed:
            changed_files.append(os.path.relpath(out))

    print("🎉 全部处理完成，输出目录：", OUTPUT_DIR)
    # 输出变更文件列表，供GitHub Actions读取
    if changed_files:
        with open(os.path.join(OUTPUT_DIR, ".changed_files.txt"), "w", encoding="utf-8") as f:
            for fn in changed_files:
                f.write(fn + "\n")


if __name__ == "__main__":
    main()
