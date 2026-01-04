#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
传感器标定参数统计分析脚本
功能：读取多组标定参数，计算统计量，识别异常数据
作者：何枭雄
日期：2025-01-15
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import argparse
from pathlib import Path

# 设置中文字体（Windows系统）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class CalibrationAnalyzer:
    """标定参数分析器"""
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.calibration_data = []
        self.df = None
    
    def load_calibration_files(self):
        """加载所有标定参数文件"""
        print(f"[INFO] 从 {self.data_dir} 加载标定文件...")
        
        json_files = list(self.data_dir.glob('*.json'))
        
        if not json_files:
            print("[ERROR] 未找到标定文件")
            return False
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                    # 提取关键参数
                    params = {
                        'file_name': json_file.name,
                        'rotation_x': data.get('rotation', {}).get('x', 0),
                        'rotation_y': data.get('rotation', {}).get('y', 0),
                        'rotation_z': data.get('rotation', {}).get('z', 0),
                        'translation_x': data.get('translation', {}).get('x', 0),
                        'translation_y': data.get('translation', {}).get('y', 0),
                        'translation_z': data.get('translation', {}).get('z', 0),
                    }
                    
                    self.calibration_data.append(params)
            
            except Exception as e:
                print(f"[WARN] 读取 {json_file.name} 失败: {str(e)}")
        
        print(f"[INFO] 成功加载 {len(self.calibration_data)} 个标定文件")
        
        # 转换为DataFrame
        self.df = pd.DataFrame(self.calibration_data)
        return True
    
    def calculate_statistics(self):
        """计算统计量"""
        if self.df is None or self.df.empty:
            print("[ERROR] 没有数据")
            return
        
        print("\n" + "="*60)
        print("标定参数统计分析")
        print("="*60)
        
        # 排除文件名列
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            data = self.df[col]
            mean_val = data.mean()
            std_val = data.std()
            min_val = data.min()
            max_val = data.max()
            median_val = data.median()
            
            print(f"\n【{col}】:")
            print(f"  均值:     {mean_val:.6f}")
            print(f"  标准差:   {std_val:.6f}")
            print(f"  最小值:   {min_val:.6f}")
            print(f"  最大值:   {max_val:.6f}")
            print(f"  中位数:   {median_val:.6f}")
            if mean_val != 0:
                cv = (std_val / abs(mean_val)) * 100
                print(f"  变异系数: {cv:.2f}%")
        
        print("\n" + "="*60 + "\n")
    
    def detect_outliers(self, threshold=3):
        """检测异常值（使用3-sigma原则）"""
        print(f"[INFO] 检测异常值（阈值: {threshold} sigma）...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = []
        
        for col in numeric_cols:
            data = self.df[col]
            mean_val = data.mean()
            std_val = data.std()
            
            if std_val == 0:
                continue
            
            # 3-sigma原则
            lower_bound = mean_val - threshold * std_val
            upper_bound = mean_val + threshold * std_val
            
            # 找出异常值
            outlier_mask = (data < lower_bound) | (data > upper_bound)
            outlier_indices = self.df[outlier_mask].index.tolist()
            
            if outlier_indices:
                for idx in outlier_indices:
                    outliers.append({
                        'file': self.df.loc[idx, 'file_name'],
                        'parameter': col,
                        'value': data.loc[idx],
                        'mean': mean_val,
                        'std': std_val,
                        'deviation': abs(data.loc[idx] - mean_val) / std_val
                    })
        
        if outliers:
            print(f"\n[WARN] 发现 {len(outliers)} 个异常值：\n")
            for outlier in outliers:
                print(f"  文件: {outlier['file']}")
                print(f"    参数: {outlier['parameter']}")
                print(f"    值: {outlier['value']:.6f}")
                print(f"    均值: {outlier['mean']:.6f}, 标准差: {outlier['std']:.6f}")
                print(f"    偏离: {outlier['deviation']:.2f} sigma")
                print()
        else:
            print("[INFO] 未发现异常值\n")
        
        return outliers
    
    def plot_distribution(self, output_file='calibration_distribution.png'):
        """绘制参数分布图"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('标定参数分布图', fontsize=16)
        
        for idx, col in enumerate(numeric_cols):
            ax = axes[idx // 3, idx % 3]
            
            data = self.df[col]
            ax.hist(data, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
            ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2,
                      label=f'均值: {data.mean():.4f}')
            ax.axvline(data.median(), color='green', linestyle=':', linewidth=2,
                      label=f'中位数: {data.median():.4f}')
            ax.set_title(col, fontsize=12)
            ax.set_xlabel('参数值', fontsize=10)
            ax.set_ylabel('频数', fontsize=10)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"[INFO] 分布图已保存到: {output_file}")
        plt.close()
    
    def export_report(self, output_file='calibration_report.csv'):
        """导出统计报告"""
        if self.df is None:
            return
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        stats = []
        for col in numeric_cols:
            data = self.df[col]
            mean_val = data.mean()
            std_val = data.std()
            cv = (std_val / abs(mean_val) * 100) if mean_val != 0 else 0
            
            stats.append({
                '参数名称': col,
                '均值': f'{mean_val:.6f}',
                '标准差': f'{std_val:.6f}',
                '最小值': f'{data.min():.6f}',
                '最大值': f'{data.max():.6f}',
                '中位数': f'{data.median():.6f}',
                '变异系数(%)': f'{cv:.2f}'
            })
        
        stats_df = pd.DataFrame(stats)
        stats_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"[INFO] 统计报告已导出到: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='标定参数统计分析工具',
        epilog='示例: python calibration_analysis.py -d ./calibration_data/ -o -p'
    )
    parser.add_argument('-d', '--dir', required=True, help='标定文件目录')
    parser.add_argument('-o', '--outlier', action='store_true', help='检测异常值')
    parser.add_argument('-p', '--plot', action='store_true', help='生成分布图')
    parser.add_argument('-t', '--threshold', type=float, default=3.0, 
                       help='异常值检测阈值（sigma），默认3.0')
    
    args = parser.parse_args()
    
    print("="*60)
    print("标定参数统计分析工具 v1.0")
    print("="*60)
    
    analyzer = CalibrationAnalyzer(args.dir)
    
    if analyzer.load_calibration_files():
        analyzer.calculate_statistics()
        
        if args.outlier:
            analyzer.detect_outliers(threshold=args.threshold)
        
        if args.plot:
            analyzer.plot_distribution()
        
        analyzer.export_report()
        
        print("\n[SUCCESS] 分析完成！")
    else:
        print("\n[FAILED] 分析失败！")


if __name__ == '__main__':
    main()

