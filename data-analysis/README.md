# 数据分析工具集

## 概述

用于智能驾驶和高精地图测试的数据分析工具，包括日志解析、标定参数分析、数据格式转换等功能。

---

## 工具列表

### 1. log_parser.py - 车辆日志解析工具

从大型日志文件（GB级）中提取关键信息。

**功能**：
- 提取GPS轨迹数据（经纬度、海拔）
- 提取车速、方向盘转角
- 支持实时进度显示
- 统计分析功能

**使用方法**：
```bash
# 基本用法
python log_parser.py -i vehicle_log.txt -o output.csv

# 带统计信息
python log_parser.py -i vehicle_log.txt -o output.csv -s
```

**输出格式**：CSV文件，包含以下字段
- timestamp: 时间戳
- latitude: 纬度
- longitude: 经度
- altitude: 海拔
- speed_kmh: 车速（km/h）
- steering_angle: 方向盘转角（度）

---

### 2. calibration_analysis.py - 传感器标定参数分析工具

统计分析多组标定参数，识别异常数据。

**功能**：
- 计算均值、标准差、变异系数
- 检测异常值（3-sigma原则）
- 生成可视化分布图
- 导出统计报告

**使用方法**：
```bash
# 基本统计
python calibration_analysis.py -d ./calibration_data/

# 检测异常值
python calibration_analysis.py -d ./calibration_data/ -o

# 生成分布图
python calibration_analysis.py -d ./calibration_data/ -o -p

# 自定义异常检测阈值
python calibration_analysis.py -d ./calibration_data/ -o -t 2.5
```

**输入格式**：JSON文件，包含标定参数
```json
{
  "rotation": {"x": 0.001234, "y": -0.002156, "z": 0.000987},
  "translation": {"x": 0.125, "y": -0.032, "z": 1.450}
}
```

**输出**：
- 统计报告（CSV格式）
- 分布图（PNG格式）
- 异常值列表

---

### 3. data_converter.py - 数据格式转换工具

在JSON、CSV、YAML格式之间互相转换。

**功能**：
- 自动识别输入输出格式
- 支持三种格式互转
- 保持数据完整性

**使用方法**：
```bash
# JSON转CSV
python data_converter.py -i data.json -o data.csv

# CSV转JSON
python data_converter.py -i data.csv -o data.json

# JSON转YAML
python data_converter.py -i data.json -o data.yaml

# 手动指定格式
python data_converter.py -i data.txt -o data.csv --if json --of csv
```

---

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- numpy - 数值计算
- pandas - 数据处理
- matplotlib - 数据可视化
- pyyaml - YAML格式支持

---

## 应用场景

### 智能驾驶测试
```bash
# 1. 解析路测日志
python log_parser.py -i noa_test_20250115.log -o test_data.csv -s

# 2. 分析车速分布
# 使用pandas分析输出的CSV文件

# 3. 转换为JSON供其他工具使用
python data_converter.py -i test_data.csv -o test_data.json
```

### 传感器标定
```bash
# 1. 收集多组标定数据（保存为JSON）

# 2. 统计分析并检测异常
python calibration_analysis.py -d ./calib_data_20250115/ -o -p

# 3. 查看生成的报告和分布图
```

---

## 技术要点

- 使用正则表达式高效提取日志信息
- 使用pandas进行数据处理和统计
- 使用matplotlib生成可视化图表
- 使用argparse提供友好的命令行接口
- 支持进度显示，适合大文件处理

---

## 性能

- 处理1GB日志文件：约1-2分钟
- 分析100组标定数据：约5秒
- 格式转换1万条记录：约3秒

---

## 作者

何枭雄 - 汽车测试工程师
- 擅长Python数据分析
- 5年车载测试经验

