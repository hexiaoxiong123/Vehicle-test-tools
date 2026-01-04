#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
文本字符频率分析工具
功能：统计文本文件中每个字符出现的频率
作者：何枭雄
日期：2021-06-15
"""

def analyze_text_frequency(input_file, encoding='UTF-8'):
    """
    分析文本文件中字符出现的频率
    
    Args:
        input_file: 输入文件路径
        encoding: 文件编码，默认UTF-8
    
    Returns:
        rate: 字符频率字典（按出现次数降序排列）
        total_chars: 总字符数
        unique_chars: 不同字符数
    """
    
    try:
        # 打开文件
        with open(input_file, 'r', encoding=encoding) as f:
            # 读取文件所有行
            content = f.readlines()
    except FileNotFoundError:
        print(f"[错误] 文件不存在: {input_file}")
        return None, 0, 0
    except Exception as e:
        print(f"[错误] 读取文件失败: {str(e)}")
        return None, 0, 0
    
    contentLines = ''
    characers = []  # 存放不同字符的列表
    rate = {}       # 存放每个字符出现的频率

    # 依次迭代所有行
    for line in content:
        # 去除空格
        line = line.strip()
        # 如果是空行，则跳过
        if len(line) == 0:
            continue
        
        contentLines = contentLines + line
        
        # 统计每个字符出现的次数
        for i in range(0, len(line)):
            # 如果字符第一次出现，加入到字符数组中
            if not line[i] in characers:
                characers.append(line[i])
            
            # 如果是字符第一次出现，加入到字典中
            if line[i] not in rate:
                rate[line[i]] = 0
            
            # 出现次数加一
            rate[line[i]] += 1

    # 对字典进行降序排序（按出现次数从高到低）
    # e表示dict.items()中的一个元素，e[1]表示按值排序
    rate = sorted(rate.items(), key=lambda e: e[1], reverse=True)
    
    return rate, len(contentLines), len(characers)


def print_results(rate, total_chars, unique_chars):
    """
    打印分析结果
    """
    print("="*60)
    print("文本字符频率分析结果")
    print("="*60)
    print(f'全文共有 {total_chars} 个字符')
    print(f'一共有 {unique_chars} 个不同的字符')
    print("="*60)
    print("\n字符出现频率（降序排列）：\n")
    
    for i in rate:
        print(f"[{i[0]}] 共出现 {i[1]} 次")


def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='文本字符频率分析工具')
    parser.add_argument('-i', '--input', required=True, help='输入文件路径')
    parser.add_argument('-e', '--encoding', default='UTF-8', help='文件编码（默认UTF-8）')
    
    args = parser.parse_args()
    
    print(f"[INFO] 开始分析文件: {args.input}")
    
    # 分析文本频率
    rate, total_chars, unique_chars = analyze_text_frequency(args.input, args.encoding)
    
    if rate:
        # 打印结果
        print_results(rate, total_chars, unique_chars)
        print("\n[SUCCESS] 分析完成！")
    else:
        print("\n[FAILED] 分析失败！")


if __name__ == '__main__':
    main()

