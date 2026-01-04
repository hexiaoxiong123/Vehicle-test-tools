#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据格式转换工具
功能：在不同数据格式之间转换（JSON、CSV、YAML）
作者：何枭雄
日期：2025-01-15
"""

import json
import csv
import yaml
import argparse
from pathlib import Path


class DataConverter:
    """数据格式转换器"""
    
    def __init__(self, input_file, output_file, input_format=None, output_format=None):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        
        # 自动检测格式
        self.input_format = input_format or self.input_file.suffix[1:].lower()
        self.output_format = output_format or self.output_file.suffix[1:].lower()
        
        self.data = None
    
    def load_data(self):
        """加载数据"""
        print(f"[INFO] 加载 {self.input_format.upper()} 文件: {self.input_file}")
        
        try:
            if self.input_format == 'json':
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            
            elif self.input_format == 'csv':
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.data = list(reader)
            
            elif self.input_format in ['yaml', 'yml']:
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f)
            
            else:
                print(f"[ERROR] 不支持的输入格式: {self.input_format}")
                print("支持的格式: json, csv, yaml, yml")
                return False
            
            print(f"[INFO] 成功加载数据")
            
            # 显示数据概览
            if isinstance(self.data, list):
                print(f"[INFO] 数据类型: 列表，共 {len(self.data)} 条记录")
            elif isinstance(self.data, dict):
                print(f"[INFO] 数据类型: 字典，共 {len(self.data)} 个键")
            
            return True
        
        except FileNotFoundError:
            print(f"[ERROR] 文件不存在: {self.input_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON解析失败: {str(e)}")
            return False
        except Exception as e:
            print(f"[ERROR] 加载失败: {str(e)}")
            return False
    
    def save_data(self):
        """保存数据"""
        if self.data is None:
            print("[ERROR] 没有数据可以保存")
            return False
        
        print(f"[INFO] 保存为 {self.output_format.upper()} 文件: {self.output_file}")
        
        try:
            # 确保输出目录存在
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.output_format == 'json':
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            elif self.output_format == 'csv':
                # 如果数据是字典列表
                if isinstance(self.data, list) and self.data:
                    with open(self.output_file, 'w', newline='', encoding='utf-8-sig') as f:
                        if isinstance(self.data[0], dict):
                            fieldnames = self.data[0].keys()
                            writer = csv.DictWriter(f, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(self.data)
                        else:
                            writer = csv.writer(f)
                            writer.writerows(self.data)
                else:
                    print("[ERROR] CSV格式要求数据为非空列表格式")
                    return False
            
            elif self.output_format in ['yaml', 'yml']:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self.data, f, default_flow_style=False, 
                             allow_unicode=True, sort_keys=False)
            
            else:
                print(f"[ERROR] 不支持的输出格式: {self.output_format}")
                print("支持的格式: json, csv, yaml, yml")
                return False
            
            print(f"[INFO] 转换成功！")
            return True
        
        except Exception as e:
            print(f"[ERROR] 保存失败: {str(e)}")
            return False
    
    def convert(self):
        """执行转换"""
        if self.load_data():
            return self.save_data()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='数据格式转换工具 - 支持 JSON、CSV、YAML 互转',
        epilog='示例: python data_converter.py -i data.json -o data.csv'
    )
    parser.add_argument('-i', '--input', required=True, help='输入文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    parser.add_argument('--if', dest='input_format', 
                       help='输入格式 (json/csv/yaml)，不指定则自动检测')
    parser.add_argument('--of', dest='output_format', 
                       help='输出格式 (json/csv/yaml)，不指定则自动检测')
    
    args = parser.parse_args()
    
    print("="*60)
    print("数据格式转换工具 v1.0")
    print("="*60)
    
    converter = DataConverter(
        args.input, 
        args.output,
        args.input_format,
        args.output_format
    )
    
    if converter.convert():
        print("\n[SUCCESS] 任务完成！")
    else:
        print("\n[FAILED] 任务失败！")


if __name__ == '__main__':
    main()

