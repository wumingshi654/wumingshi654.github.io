import re
import os
import sys
import shutil

def add_markdown_anchors_v3(file_path: str):
    """
    为Markdown文件中的有序列表和对应的二级标题添加双向锚点链接 (V3)。

    - 点击列表的 "序号" 进行跳转。
    - 使用兼容性更强的HTML <a id="..."> 标签作为跳转目标。
    - 仅处理第一个 "## [数字]" 标题之前的有序列表。

    参数:
        file_path (str): Markdown文件的绝对路径。
    """
    # 1. 验证文件路径是否有效
    if not os.path.isfile(file_path):
        print(f"错误：文件不存在于 '{file_path}'")
        return
    if not file_path.lower().endswith('.md'):
        print(f"错误：文件 '{file_path}' 不是一个Markdown文件 (.md)。")
        return

    print(f"正在处理文件: {file_path}")

    try:
        # 2. 创建原始文件的备份
        backup_path = file_path + '.bak'
        shutil.copy2(file_path, backup_path)
        print(f"已创建备份文件: {backup_path}")

        # 3. 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 4. 找到第一个 "## [数字]" 标题的位置，以此为界限分割文件内容
        first_heading_match = re.search(r"^(##\s*\d+\s*)$", content, re.MULTILINE)

        if not first_heading_match:
            print("注意：在文件中未找到格式为 '## [数字]' 的标题，未进行任何操作。")
            os.remove(backup_path)
            print(f"已删除不必要的备份文件: {backup_path}")
            return

        split_index = first_heading_match.start()
        content_before_headings = content[:split_index]
        content_after_headings = content[split_index:]

        # 5. 定义替换函数
        
        # 函数一: 用于处理列表项
        def replace_list_item(match):
            number = match.group(1)
            text = match.group(2).strip()
            list_anchor = f"ref-{number}"
            heading_anchor = f"toc-{number}"
            
            # --- 这是本次修改的核心 ---
            # 将序号部分 [数字.] 创建为链接，文字内容保持不变
            return f'<a id="{list_anchor}"></a>[{number}.](#{heading_anchor}) {text}'

        # 函数二: 用于处理标题
        def replace_heading(match):
            heading_text = match.group(1)
            number = match.group(2)
            list_anchor = f"ref-{number}"
            heading_anchor = f"toc-{number}"
            return f'{heading_text} <a id="{heading_anchor}"></a> [↩](#{list_anchor})'

        # 6. 对相应部分执行替换操作

        # 仅对 "## 1" 之前的内容应用列表项的修改
        list_pattern = re.compile(r"^(\d+)\.\s+(?!\[)(.*)$", re.MULTILINE)
        modified_before = list_pattern.sub(replace_list_item, content_before_headings)

        # 仅对 "## 1" 及之后的内容应用标题的修改
        heading_pattern = re.compile(r"^(##\s*(\d+))\s*$", re.MULTILINE)
        modified_after = heading_pattern.sub(replace_heading, content_after_headings)

        # 7. 合并内容并写回文件
        final_content = modified_before + modified_after

        if final_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print("成功为文件更新了锚点链接。")
        else:
            print("文件内容无需修改（可能已经处理过）。")
            os.remove(backup_path)
            print(f"已删除不必要的备份文件: {backup_path}")

    except Exception as e:
        print(f"处理文件时发生错误: {e}")
        if 'backup_path' in locals() and os.path.exists(backup_path):
            shutil.move(backup_path, file_path)
            print("已从备份中恢复原始文件。")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        markdown_file_path = sys.argv[1]
        add_markdown_anchors_v3(markdown_file_path)
    else:
        print("使用方法: python your_script_name.py \"<markdown文件的完整路径>\"")
        print("\n示例:")
        print(r'python your_script_name.py "D:\path\to\your\file.md"')