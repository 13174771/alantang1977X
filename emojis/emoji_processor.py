import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Union, Any

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

# Emoji 正则表达式模式，匹配常见Emoji字符
EMOJI_REGEX = re.compile(
    r'[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001F1E0-\U0001F1FF]'
)

class EmojiManager:
    """Emoji表情管理类，负责Emoji的替换和循环使用"""
    
    def __init__(self):
        """初始化Emoji管理器"""
        self.emoji_pool = EMOJI_POOL
        self.emoji_index = 0
    
    def get_next_emoji(self) -> str:
        """获取下一个Emoji，池用尽时循环使用"""
        emoji = self.emoji_pool[self.emoji_index]
        self.emoji_index = (self.emoji_index + 1) % len(self.emoji_pool)
        return emoji
    
    def replace_emojis(self, text: str) -> str:
        """替换文本中的Emoji为新的Emoji"""
        if not text:
            return text
            
        # 提取所有Emoji并去重
        unique_emojis = set(EMOJI_REGEX.findall(text))
        if not unique_emojis:
            return text
            
        # 创建Emoji映射关系
        emoji_mapping = {old_emoji: self.get_next_emoji() for old_emoji in unique_emojis}
        
        # 执行Emoji替换
        return EMOJI_REGEX.sub(
            lambda match: emoji_mapping.get(match.group(0), match.group(0)),
            text
        )


class FileProcessor:
    """文件处理类，负责不同格式文件的Emoji处理"""
    
    def __init__(self, emoji_manager: EmojiManager):
        """初始化文件处理器"""
        self.emoji_manager = emoji_manager
    
    def process_json(self, content: Union[Dict, List]) -> Union[Dict, List]:
        """递归处理JSON内容中的Emoji"""
        if isinstance(content, dict):
            return {k: self.process_json(v) for k, v in content.items()}
        elif isinstance(content, list):
            return [self.process_json(item) for item in content]
        elif isinstance(content, str):
            return self.emoji_manager.replace_emojis(content)
        return content
    
    def process_text_file(self, content: str, input_path: Path) -> Dict[str, Any]:
        """处理文本文件（非JSON）的Emoji替换"""
        processed_content = self.emoji_manager.replace_emojis(content)
        return {
            "original_file": str(input_path),
            "content": processed_content
        }
    
    def process_file(self, input_path: Path, output_path: Path) -> None:
        """处理单个文件，区分JSON和非JSON格式"""
        try:
            # 读取文件内容
            with open(input_path, 'r', encoding='utf-8') as f:
                if input_path.suffix.lower() == '.json':
                    # 处理JSON文件
                    content = json.load(f)
                    processed_content = self.process_json(content)
                    # 写入处理后的JSON文件
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        json.dump(processed_content, out_f, ensure_ascii=False, indent=2)
                else:
                    # 处理非JSON文本文件
                    content = f.read()
                    processed_data = self.process_text_file(content, input_path)
                    # 写入包含原始文件信息的JSON文件
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        json.dump(processed_data, out_f, ensure_ascii=False, indent=2)
            print(f"已处理: {input_path} -> {output_path}")
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {str(e)}")


def process_files(target_files: List[str], input_dir: Path, output_dir: Path) -> None:
    """处理指定的目标文件"""
    emoji_manager = EmojiManager()
    file_processor = FileProcessor(emoji_manager)
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for file_name in target_files:
        input_file = input_dir / file_name
        if not input_file.exists():
            print(f"警告: 文件 '{input_file}' 不存在，跳过")
            continue
            
        if input_file.is_file():
            # 处理文件
            output_file = output_dir / (input_file.stem + '.json')
            file_processor.process_file(input_file, output_file)
        else:
            print(f"警告: '{input_file}' 不是文件，跳过")


def main():
    """主函数，协调整个Emoji处理流程"""
    try:
        # 创建命令行参数解析器
        parser = argparse.ArgumentParser(description='处理指定的Emoji文件')
        parser.add_argument('--files', nargs='+', required=True, 
                            help='要处理的目标文件列表，用空格分隔')
        parser.add_argument('--input-dir', default='emojis', 
                            help='输入目录路径，默认为emojis')
        parser.add_argument('--output-dir', default='emojis/output', 
                            help='输出目录路径，默认为emojis/output')
        
        # 解析命令行参数
        args = parser.parse_args()
        
        # 转换为Path对象
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        
        # 检查输入目录是否存在
        if not input_dir.exists():
            print(f"错误: 输入目录 '{input_dir}' 不存在")
            return
        
        # 开始处理指定文件
        print(f"开始处理指定文件，输入目录: {input_dir}")
        process_files(args.files, input_dir, output_dir)
        
        print(f"处理完成! 结果保存在: {output_dir}")
        
    except Exception as e:
        print(f"程序执行出错: {str(e)}")


if __name__ == "__main__":
    main()
