# emojis/emojis.py
import re
import random
import os
import glob

# 定义一个包含多种Emoji的列表
emoji_list = [
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

def replace_emojis_in_file(input_file_path, output_file_path):
    """
    替换JSON文件中"name"字段值里的Emoji表情符号为新的、不同的Emoji
    
    参数:
    input_file_path (str): 输入文件路径
    output_file_path (str): 输出文件路径
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取JSON文件内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 定义Emoji的正则表达式模式
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        
        # 找出所有"name":"..."模式的字符串
        name_pattern = re.compile(r'"name":"([^"]*)"')
        name_matches = name_pattern.finditer(content)
        
        # 用于跟踪已替换的Emoji，确保唯一性
        used_emojis = set()
        total_replacements = 0
        
        # 替换每个匹配的"name"字段中的Emoji
        new_content = content
        for match in reversed(list(name_matches)):  # 从后往前替换，避免索引问题
            name_value = match.group(1)
            emojis_in_name = emoji_pattern.findall(name_value)
            
            if not emojis_in_name:
                continue
                
            # 为每个Emoji生成一个新的不同的Emoji
            new_name_value = name_value
            for old_emoji in reversed(emojis_in_name):  # 从后往前替换，避免索引问题
                available_emojis = [emoji for emoji in emoji_list if emoji not in used_emojis]
                if not available_emojis:
                    print(f"警告: Emoji列表中的Emoji不够用了，已使用 {len(used_emojis)} 个不同Emoji，将重新使用池")
                    available_emojis = emoji_list
                new_emoji = random.choice(available_emojis)
                new_name_value = new_name_value[::-1].replace(old_emoji[::-1], new_emoji[::-1], 1)[::-1]
                used_emojis.add(new_emoji)
                total_replacements += 1
            
            # 更新整个匹配的字符串
            original_text = match.group(0)
            new_text = f'"name":"{new_name_value}"'
            new_content = new_content[:match.start()] + new_text + new_content[match.end():]
        
        print(f"在文件中找到并替换了 {total_replacements} 个Emoji")
        
        # 将修改后的内容写回文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"Emoji替换完成，输出文件: {output_file_path}")
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {input_file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    """
    主函数：处理emojis文件夹下的所有JSON文件
    """
    # 获取emojis文件夹路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = script_dir
    output_dir = os.path.join(script_dir, "output")
    
    # 查找所有.json文件
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    
    if not json_files:
        print("在emojis文件夹中未找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件需要处理")
    
    # 处理每个JSON文件
    for json_file in json_files:
        file_name = os.path.basename(json_file)
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        
        print(f"\n处理文件: {file_name}")
        replace_emojis_in_file(input_path, output_path)
    
    print("\n所有文件处理完成")

if __name__ == "__main__":
    main()    
