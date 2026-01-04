#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车辆日志解析脚本
功能：从大型日志文件中提取关键信息（GPS、车速、方向盘转角等）
作者：何枭雄
日期：2025-01-15
"""

import re
import csv
import argparse
from datetime import datetime


class LogParser:
    """日志解析器类"""
    
    def __init__(self, log_file, output_file):
        self.log_file = log_file
        self.output_file = output_file
        self.data = []
    
    def parse_log(self):
        """解析日志文件"""
        print(f"[INFO] 开始解析日志文件: {self.log_file}")
        
        # 正则表达式匹配模式
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'
        gps_pattern = r'GPS: lat=([-\d.]+), lon=([-\d.]+), alt=([-\d.]+)'
        speed_pattern = r'Speed: ([\d.]+) km/h'
        steering_pattern = r'SteeringAngle: ([-\d.]+) deg'
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                line_count = 0
                for line in f:
                    line_count += 1
                    
                    # 提取时间戳
                    timestamp_match = re.search(timestamp_pattern, line)
                    if not timestamp_match:
                        continue
                    
                    timestamp = timestamp_match.group(0)
                    
                    # 提取GPS坐标
                    gps_match = re.search(gps_pattern, line)
                    lat, lon, alt = ('N/A', 'N/A', 'N/A')
                    if gps_match:
                        lat, lon, alt = gps_match.groups()
                    
                    # 提取车速
                    speed_match = re.search(speed_pattern, line)
                    speed = speed_match.group(1) if speed_match else 'N/A'
                    
                    # 提取方向盘转角
                    steering_match = re.search(steering_pattern, line)
                    steering = steering_match.group(1) if steering_match else 'N/A'
                    
                    # 如果该行包含有效数据，则保存
                    if gps_match or speed_match or steering_match:
                        self.data.append({
                            'timestamp': timestamp,
                            'latitude': lat,
                            'longitude': lon,
                            'altitude': alt,
                            'speed_kmh': speed,
                            'steering_angle': steering
                        })
                    
                    # 每处理10000行显示进度
                    if line_count % 10000 == 0:
                        print(f"[INFO] 已处理 {line_count} 行，提取到 {len(self.data)} 条有效数据")
        
        except FileNotFoundError:
            print(f"[ERROR] 文件不存在: {self.log_file}")
            return False
        except Exception as e:
            print(f"[ERROR] 解析出错: {str(e)}")
            return False
        
        print(f"[INFO] 解析完成！共提取 {len(self.data)} 条有效数据")
        return True
    
    def export_to_csv(self):
        """导出为CSV文件"""
        if not self.data:
            print("[WARN] 没有数据可以导出")
            return False
        
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['timestamp', 'latitude', 'longitude', 'altitude', 
                             'speed_kmh', 'steering_angle']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.data)
            
            print(f"[INFO] 数据已导出到: {self.output_file}")
            return True
        
        except Exception as e:
            print(f"[ERROR] 导出失败: {str(e)}")
            return False
    
    def get_statistics(self):
        """统计分析"""
        if not self.data:
            return
        
        print("\n========== 数据统计 ==========")
        print(f"总记录数: {len(self.data)}")
        
        # 统计有效GPS记录
        valid_gps = sum(1 for d in self.data if d['latitude'] != 'N/A')
        print(f"有效GPS记录: {valid_gps}")
        
        # 统计有效速度记录
        valid_speed = sum(1 for d in self.data if d['speed_kmh'] != 'N/A')
        print(f"有效车速记录: {valid_speed}")
        
        # 计算平均速度
        if valid_speed > 0:
            speeds = [float(d['speed_kmh']) for d in self.data if d['speed_kmh'] != 'N/A']
            avg_speed = sum(speeds) / len(speeds)
            max_speed = max(speeds)
            min_speed = min(speeds)
            print(f"平均车速: {avg_speed:.2f} km/h")
            print(f"最高车速: {max_speed:.2f} km/h")
            print(f"最低车速: {min_speed:.2f} km/h")
        
        print("==============================\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='车辆日志解析工具',
        epilog='示例: python log_parser.py -i vehicle_log.txt -o output.csv -s'
    )
    parser.add_argument('-i', '--input', required=True, help='输入日志文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出CSV文件路径')
    parser.add_argument('-s', '--stats', action='store_true', help='显示统计信息')
    
    args = parser.parse_args()
    
    print("="*60)
    print("车辆日志解析工具 v1.0")
    print("="*60)
    
    # 创建解析器实例
    log_parser = LogParser(args.input, args.output)
    
    # 解析日志
    if log_parser.parse_log():
        # 显示统计信息
        if args.stats:
            log_parser.get_statistics()
        
        # 导出CSV
        log_parser.export_to_csv()
        
        print("\n[SUCCESS] 任务完成！")
    else:
        print("\n[FAILED] 任务失败！")


if __name__ == '__main__':
    main()

