import json
import re
from pathlib import Path
from typing import Dict, List

# 完整的安卓系统支持 Emoji 表情分类
ANDROID_EMOJI_CATEGORIES = {
    "人物和身体": [
        "👶","🧒","👦","👧","🧑","👨","👩","🧓","👴","👵",
        "👮","🦸","🧙","🚴","👨‍⚕️","👩‍⚕️","👨‍🎓","👩‍🎓","👨‍🏫","👩‍🏫",
        "👨‍⚖️","👩‍⚖️","👨‍🌾","👩‍🌾","👨‍🍳","👩‍🍳","👨‍🔧","👩‍🔧","👨‍🏭","👩‍🏭",
        "👨‍💼","👩‍💼","👨‍🔬","👩‍🔬","👨‍💻","👩‍💻","👨‍🎤","👩‍🎤","👨‍🎨","👩‍🎨",
        "👨‍✈️","👩‍✈️","👨‍🚀","👩‍🚀","👨‍🚒","👩‍🚒","🕵️","💂","🥷","👷",
        "🤴","👸","👳","👲","🧕","🤵","👰","🤰","🤱","👼",
        "💆","💇","🚶","🧍","🧎","🏃","💃","🕺","🕴️","👯",
        "🧖","🧗","🤺","🏇","⛷️","🏂","🏌️","🏄","🚣","🏊",
        "⛹️","🏋️","🚴","🚵","🤸","🤼","🤽","🤾","🤹","🧘",
        "🛀","🛌","👭","👫","👬","💏","💑","👪"
    ],
    "食物和饮料": [
        "🍏","🍎","🍐","🍊","🍋","🍌","🍉","🍇","🍓","🫐","🍈",
        "🍒","🍑","🥭","🍍","🥥","🥝","🍅","🍆","🥑","🥦","🥬",
        "🥒","🌶️","🫑","🌽","🥕","🫒","🥔","🍠","🥐","🥯","🍞",
        "🥖","🥨","🧀","🥚","🍳","🧈","🥞","🧇","🥓","🥩","🍗",
        "🍖","🌭","🍔","🍟","🍕","🫓","🥪","🥙","🌮","🌯","🫔",
        "🥗","🍝","🍜","🍲","🍛","🍣","🍱","🥟","🦪","🍤","🍙",
        "🍚","🍘","🍥","🥠","🥮","🍢","🍡","🍧","🍨","🍦","🥧",
        "🧁","🍰","🎂","🍮","🍭","🍬","🍫","🍿","🧋","🍩","🍪"
    ],
    "旅行和地点": [
        "🚗","🚕","🚙","🚌","🚎","🏎️","🚓","🚑","🚒","🚐","🛻",
        "🚚","🚛","🚜","🦯","🦽","🦼","🚲","🛴","🛵","🏍️","🛺",
        "🚨","🚔","🚍","🚘","🚖","🚡","🚠","🚟","🚃","🚋","🚞",
        "🚝","🚄","🚅","🚈","🚂","🚆","🚇","🚊","🚉","✈️","🛫",
        "🛬","🛰️","🚀","🛸","🚁","🛶","⛵","🛥️","🚤","🦢","🦩",
        "🗼","🗽","🗿","🗻","🏔️","⛰️","🌋","🏕️","🏖️","🏜️","🏝️",
        "🏟️","🏛️","🏗️","🧱","🏘️","🏚️","🏠","🏡","🏢","🏣","🏤",
        "🏥","🏦","🏨","🏩","🏪","🏫","🏬","🏭","🏯","🏰","💒",
        "🕌","🕍","🛕","🕋","⛪","🛤️","🛣️","🌁","🌃","🏙️","🌄"
    ],
    # 可以根据需求继续添加其他分类，如：活动、动物和自然、符号等
}

# 将所有分类扁平化为单一的表情列表
ANDROID_EMOJIS = [emoji for category in ANDROID_EMOJI_CATEGORIES.values() for emoji in category]


def extract_emojis(text: str) -> List[str]:
    """提取字符串中所有唯一的 Unicode 表情符号"""
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'
        '\U0001F300-\U0001F5FF'
        '\U0001F680-\U0001F6FF'
        '\U0001F1E0-\U0001F1FF'
        '\U00002500-\U00002BEF'
        '\U00002702-\U000027B0'
        '\U000024C2-\U0001F251'
        '\U0001F900-\U0001F9FF'
        '\U0001FA70-\U0001FAFF'
        ']+',
        flags=re.UNICODE
    )
    return list(set(emoji_pattern.findall(text)))


def create_emoji_mapping(emojis: List[str]) -> Dict[str, str]:
    """
    创建表情符号到安卓表情的映射
    规则：
    1. 每个原始表情映射到唯一的安卓表情
    2. 如果安卓表情用尽，则重新开始分配
    """
    sorted_emojis = sorted(emojis)
    mapping = {}
    emoji_pool = ANDROID_EMOJIS.copy()

    for emoji in sorted_emojis:
        if not emoji_pool:
            emoji_pool = ANDROID_EMOJIS.copy()
        mapping[emoji] = emoji_pool.pop(0)
    return mapping


def process_text(text: str, mapping: Dict[str, str]) -> str:
    """使用映射替换文本中的所有表情符号"""
    for orig, replacement in mapping.items():
        text = text.replace(orig, replacement)
    return text


def main():
    input_path = Path('input.json')
    output_path = Path('output.json')

    # 读取并解析内容
    content = input_path.read_text(encoding='utf-8')
    try:
        # 尝试加载 JSON ，保持结构
        data = json.loads(content)
        text = json.dumps(data, ensure_ascii=False)
    except json.JSONDecodeError:
        # 如果不是严格 JSON，就当作普通文本处理
        text = content

    # 提取并映射
    found = extract_emojis(text)
    mapping = create_emoji_mapping(found)
    processed = process_text(text, mapping)

    # 写入文件
    output_path.write_text(processed, encoding='utf-8')
    print(f"处理完成：替换 {len(mapping)} 个表情符号，结果已写入 {output_path}")


if __name__ == '__main__':
    main()
