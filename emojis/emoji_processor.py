import json
import re
from pathlib import Path
from typing import Dict, List

# 完整的安卓支持表情符号列表
ANDROID_EMOJIS = [
    "👮", "🦸", "🧙", "🚴", "👨‍⚕️", "👩‍⚕️", "👨‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫",
    "👨‍⚖️", "👩‍⚖️", "👨‍🌾", "👩‍🌾", "👨‍🍳", "👩‍🍳", "👨‍🔧", "👩‍🔧", "👨‍🏭", "👩‍🏭",
    "👨‍💼", "👩‍💼", "👨‍🔬", "👩‍🔬", "👨‍💻", "👩‍💻", "👨‍🎤", "👩‍🎤", "👨‍🎨", "👩‍🎨",
    "👨‍✈️", "👩‍✈️", "👨‍🚀", "👩‍🚀", "👨‍🚒", "👩‍🚒", "🕵️", "💂", "🥷", "👷",
    "🤴", "👸", "👳", "👲", "🧕", "🤵", "👰", "🤰", "🤱", "👼",
    "🎅", "🤶", "🧑‍🎄", "🦸", "🦹", "🧙", "🧚", "🧛", "🧜", "🧝",
    "🧞", "🧟", "💆", "💇", "🚶", "🧍", "🧎", "🏃", "💃", "🕺",
    "🕴️", "👯", "🧖", "🧗", "🤺", "🏇", "⛷️", "🏂", "🏌️", "🏄",
    "🚣", "🏊", "⛹️", "🏋️", "🚴", "🚵", "🤸", "🤼", "🤽", "🤾",
    "🤹", "🧘", "🛀", "🛌", "👭", "👫", "👬", "💏", "💑", "👪",
    "❤️", "🎉", "⏰", "😊", "😄", "😃", "😂", "🤣", "😍", "🥰",
    "😘", "😗", "😚", "😙", "🥲", "😏", "😳", "🥺", "😭", "😡",
    "🤬", "🤯", "🥶", "🥵", "😱", "😨", "😰", "😥", "😓", "🤗",
    "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😪",
    "😴", "😷", "🤧", "🤮", "🤢", "🥴", "😵", "🤠", "🥳", "😎",
    "🤓", "🧐", "😕", "😟", "🙁", "☹️", "😮", "😯", "😲", "😦",
    "😧", "🙂", "🙃", "☺️", "😇", "🤩", "🥸", "🤪", "🤨", "🥱",
    "😈", "👿", "💀", "☠️", "💩", "🤡", "👹", "👺", "👻", "👽",
    "👾", "🤖", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
    "😾", "👋", "🤚", "🖐️", "✋", "🖖", "👌", "🤌", "🤏", "✌️",
    "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️",
    "👍", "👎", "✊", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲",
    "🙏", "✍️", "💅", "🤳", "💪", "🦾", "🦵", "🦿", "🦶", "👂",
    "🦻", "👃", "🧠", "🫀", "🫁", "🦷", "🦴", "👀", "👅", "👄",
    "👶", "🧒", "👦", "👧", "🧑", "👨", "👩", "🧓", "👴", "👵"
]

def extract_emojis(text: str) -> List[str]:
    """提取字符串中所有唯一的Unicode表情符号"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和象形文字
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F1E0-\U0001F1FF"  # 国旗
        "\U00002500-\U00002BEF"  # 其他符号
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U0001F900-\U0001F9FF"  # 补充符号
        "\U0001FA70-\U0001FAFF"  # 扩展
        "]+",
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
    sorted_emojis = sorted(emojis)  # 排序确保一致性
    mapping = {}
    
    # 创建安卓表情池
    emoji_pool = ANDROID_EMOJIS.copy()
    
    for emoji in sorted_emojis:
        if not emoji_pool:
            # 如果表情池用尽，重新填充
            emoji_pool = ANDROID_EMOJIS.copy()
        
        # 分配下一个安卓表情
        android_emoji = emoji_pool[0]
        mapping[emoji] = android_emoji
        emoji_pool.remove(android_emoji)  # 从池中移除已使用的表情
    
    return mapping

def process_json_file(file_path: Path, mapping: Dict[str, str]) -> str:
    """处理JSON文件并返回内容，保持原始格式"""
    content = file_path.read_text(encoding='utf-8')
    return replace_emojis(content, mapping)

def replace_emojis(text: str, mapping: Dict[str, str]) -> str:
    """使用映射替换文本中的所有表情符号"""
    for orig, replacement in mapping.items():
        text = text.replace(orig, replacement)
    return text

def main():
    # 文件路径配置
    input_file = Path('input.json')  # 您的JSON文件
    output_file = Path('output.json')  # 输出文件
    
    # 读取文件内容
    content = input_file.read_text(encoding='utf-8')
    
    # 提取所有唯一表情符号
    all_emojis = extract_emojis(content)
    
    # 创建全局表情映射
    emoji_mapping = create_emoji_mapping(all_emojis)
    
    # 处理文件
    processed_content = replace_emojis(content, emoji_mapping)
    
    # 保存处理后的内容
    with output_file.open('w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"处理完成！结果已保存至 {output_file}")
    print(f"替换了 {len(emoji_mapping)} 个不同的表情符号")
    print("示例映射:")
    for orig, new in list(emoji_mapping.items())[:5]:
        print(f"{orig} → {new}")

if __name__ == "__main__":
    main()
