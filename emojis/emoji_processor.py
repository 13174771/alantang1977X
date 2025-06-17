import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Set, Union, Any

# Emoji 表情集合，包含动物与自然、食物与饮料、活动、物体、旅行与地点等类别
EMOJI_POOL = [
    # 动物与自然
    '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', 
    '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦', '🐤', '🐣', 
    '🌱', '🌲', '🌳', '🌴', '🌵', '🌼', '🌸', '🌹', '🌺', '🌻', 
    '🌍', '🌎', '🌏', '🌕', '🌖', '🌗', '🌘', '🌙', '🌚', '🌛', 
    '☀️', '⭐', '✨', '🌠', '☁️', '🌧️', '⛅', '❄️', '💦', '🔥',
    
    # 食物与饮料
    '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', 
    '🍑', '🍍', '🥭', '🍅', '🥝', '🍆', '🌶️', '🥔', '🥕', '🌽', 
    '🍞', '🥐', '🥖', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', 
    '🌯', '🍳', '🥘', '🍲', '🥗', '🍿', '🍱', '🍘', '🍙', '🍚', 
    '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🍦',
    
    # 活动
    '⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🏉', '🎱', '🏓', '🏸', 
    '⛳', '🏌️', '🚴', '🚵', '🏊', '⛷️', '🎿', '🎮', '🕹️', '🎲', 
    '🃏', '🎯', '🎳', '🏇', '🎪', '🎭', '🎨', '🎬', '📽️', '🎤', 
    '🎧', '🎼', '🎹', '🥁', '🎷', '🎸', '🎻', '🏅', '🥇', '🥈', 
    '🥉', '🏆', '⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🏉', '🎱',
    
    # 物体
    '📱', '📞', '📟', '📠', '💻', '⌨️', '🖥️', '🖨️', '🕹️', '🎮', 
    '💽', '💾', '💿', '📀', '📼', '📷', '📸', '🎥', '📽️', '🔋', 
    '🔌', '💡', '🔦', '🚪', '🪑', '🛋️', '🚽', '🛁', '🚿', '🔧', 
    '🔨', '⚒️', '🛠️', '🧰', '🔩', '🔪', '🍴', '🥄', '🔍', '🔎', 
    '🔬', '🔭', '🎪', '🎭', '🎨', '🎬', '📽️', '🎤', '🎧', '🎼',
    
    # 旅行与地点
    '✈️', '🚁', '🚀', '⛵', '🚢', '🚂', '🚅', '🚆', '🚇', '🚊', 
    '🚉', '🚌', '🚍', '🚎', '🚐', '🚑', '🚒', '🚓', '🚔', '🚕', 
    '🚖', '🚗', '🚘', '🚙', '🏠', '🏡', '🏘️', '🏚️', '🏗️', '🏭', 
    '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏩', '🏪', '🏫', 
    '🏛️', '🗼', '🏯', '🏰', '🌆', '🌇', '🏙️', '🌃', '🗽', '🗾'
]

# Emoji 正则表达式模式
EMOJI_REGEX = re.compile(r'[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001F1E0-\U0001F1FF]')

class EmojiProcessor:
    def __init__(self):
        """初始化Emoji处理器"""
        self.emoji_pool = EMOJI_POOL
        self.emoji_index = 0
    
    def get_next_emoji(self) -> str:
        """获取下一个Emoji，当池用尽时循环使用"""
        emoji = self.emoji_pool[self.emoji_index]
        self.emoji_index = (self.emoji_index + 1) % len(self.emoji_pool)
        return emoji
    
    def replace_emojis(self, content: str) -> str:
        """替换文本中的Emoji为新的Emoji"""
        # 提取所有Emoji并去重
        unique_emojis = set(EMOJI_REGEX.findall(content))
        
        # 创建Emoji映射
        emoji_mapping = {old_emoji: self.get_next_emoji() for old_emoji in unique_emojis}
        
        # 替换Emoji
        return EMOJI_REGEX.sub(lambda match: emoji_mapping.get(match.group(0), match.group(0)), content)
    
    def process_json(self, content: Union[Dict, List]) -> Union[Dict, List]:
        """处理JSON内容，递归替换其中的Emoji"""
        if isinstance(content, dict):
            return {k: self.process_json(v) for k, v in content.items()}
        elif isinstance(content, list):
            return [self.process_json(item) for item in content]
        elif isinstance(content, str):
            return self.replace_emojis(content)
        else:
            return content
    
    def process_file(self, input_path: Path, output_path: Path) -> None:
        """处理单个文件"""
        try:
            # 读取文件内容
            if input_path.suffix.lower() == '.json':
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                # 处理JSON内容
                processed_content = self.process_json(content)
                # 写入JSON文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(processed_content, f, ensure_ascii=False, indent=2)
            else:
                # 处理普通文本文件
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                processed_content = self.replace_emojis(content)
                # 写入JSON文件
                output_data = {
                    "original_file": str(input_path),
                    "content": processed_content
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"已处理: {input_path} -> {output_path}")
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {e}")
    
    def process_directory(self, input_dir: Path, output_dir: Path) -> None:
        """处理目录中的所有文件"""
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 处理所有文件
        for item in input_dir.iterdir():
            if item.is_file():
                # 构建输出文件路径，保持文件名相同但扩展名为.json
                output_file = output_dir / (item.stem + '.json')
                self.process_file(item, output_file)
            elif item.is_dir():
                # 递归处理子目录
                sub_output_dir = output_dir / item.name
                self.process_directory(item, sub_output_dir)

def main():
    """主函数"""
    # 获取当前工作目录
    current_dir = Path.cwd()
    
    # 默认输入和输出目录
    input_dir = current_dir / 'emojis'
    output_dir = input_dir / 'output'  # 修改输出目录为 emojis/output
    
    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"错误: 输入目录 '{input_dir}' 不存在")
        return
    
    # 处理目录
    processor = EmojiProcessor()
    processor.process_directory(input_dir, output_dir)
    
    print("处理完成!")
    print(f"处理后的文件已保存在: {output_dir}")

if __name__ == "__main__":
    main()    
