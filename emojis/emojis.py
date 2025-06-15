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
    替换文件中的Emoji表情符号为新的、不同的Emoji
    
    参数:
    input_file_path (str): 输入文件路径
    output_file_path (str): 输出文件路径
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取文件内容
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

        # 找出所有Emoji
        emojis = emoji_pattern.findall(content)
        total_emojis = len(emojis)
        print(f"在文件中找到 {total_emojis} 个Emoji")

        if total_emojis == 0:
            print("没有需要替换的Emoji，直接复制文件")
            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(content)
            return

        # 为每个Emoji生成一个新的不同的Emoji
        new_emojis = []
        used_emojis = set()
        for i, _ in enumerate(emojis):
            available_emojis = [emoji for emoji in emoji_list if emoji not in used_emojis]
            if not available_emojis:
                print(f"警告: Emoji列表中的Emoji不够用了，已使用 {len(used_emojis)} 个不同Emoji，将重新使用池")
                available_emojis = emoji_list
            new_emoji = random.choice(available_emojis)
            new_emojis.append(new_emoji)
            used_emojis.add(new_emoji)
            
            # 显示进度
            if (i + 1) % 100 == 0 or (i + 1) == total_emojis:
                print(f"已处理 {i + 1}/{total_emojis} 个Emoji")

        # 替换文件中的Emoji
        for old_emoji, new_emoji in zip(emojis, new_emojis):
            content = content.replace(old_emoji, new_emoji, 1)

        # 将修改后的内容写回文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

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
