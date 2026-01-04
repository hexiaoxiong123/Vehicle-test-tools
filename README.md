# Automotive Test Tools

> 汽车测试工具集 - 用于智能驾驶和高精地图测试的实用工具

## 项目简介

本项目包含作者在5年汽车测试工作中开发的实用工具，主要用于：
- 智能驾驶系统测试（NOA、ADAS）
- 高精地图数据验证
- 车载系统监控
- 自动化测试

## 技术栈

- **Python**: 数据分析、自动化测试
- **Shell**: 系统监控
- **Robot Framework**: 自动化测试框架
- **Selenium**: Web自动化测试

## 项目结构

```
automotive-test-tools/
├── README.md                           # 项目说明
├── vehicle-monitoring/                 # 车载系统监控
│   ├── vehicle_system_monitor.sh      # 系统健康监控脚本
│   └── README.md
├── data-analysis/                      # 数据分析工具
│   ├── log_parser.py                  # 日志解析工具
│   ├── calibration_analysis.py        # 标定参数分析工具
│   ├── data_converter.py              # 数据格式转换工具
│   ├── requirements.txt               # Python依赖
│   └── README.md
├── test-automation/                    # 自动化测试工具
│   ├── rf_testcase_generator.py       # Robot Framework用例生成器
│   ├── selenium_demo.py               # Selenium自动化示例
│   └── README.md
└── text-analysis/                      # 文本分析工具
    ├── text_frequency_analyzer.py     # 文本频率分析
    └── README.md
```

## 功能模块

### 1. 车载系统监控

**vehicle_system_monitor.sh** - 实时监控车载系统运行状态

功能：
- GPS定位状态检测（差分定位、收星数量）
- CPU使用率监控
- 内存使用监控
- 磁盘空间监控
- 4G网络连接检测
- NTP时间同步检查

使用场景：路测前系统健康检查，确保测试环境正常

---

### 2. 数据分析工具

#### log_parser.py - 车辆日志解析工具

从GB级日志文件中提取关键信息：
- GPS轨迹数据
- 车速、方向盘转角
- 传感器数据

```bash
python log_parser.py -i vehicle_log.txt -o output.csv -s
```

#### calibration_analysis.py - 传感器标定参数分析

统计分析多组标定参数：
- 计算均值、标准差、变异系数
- 检测异常值（3-sigma原则）
- 生成可视化分布图

```bash
python calibration_analysis.py -d calibration_data/ -o -p
```

#### data_converter.py - 数据格式转换

支持JSON、CSV、YAML格式互转

```bash
python data_converter.py -i data.json -o data.csv
```

---

### 3. 自动化测试工具

#### rf_testcase_generator.py - Robot Framework测试用例生成器

自动生成Robot Framework测试用例和库文件，用于：
- 编译输出路径检测
- 文件存在性验证
- JSON/YAML配置文件内容断言

```bash
python rf_testcase_generator.py /path/to/test/module
```

特点：
- 自动遍历目录结构
- 生成标准化测试用例
- 包含Setup/Teardown
- 支持参数化测试

#### selenium_demo.py - Web自动化测试示例

基于Selenium的Web自动化测试框架示例

---

### 4. 文本分析工具

#### text_frequency_analyzer.py - 文本频率分析

统计文本中字符出现频率，用于：
- 日志关键字分析
- 错误信息统计
- 数据模式识别

---

## 使用场景

### 智能驾驶测试
- 使用 `log_parser.py` 解析路测日志
- 使用 `vehicle_system_monitor.sh` 监控车载系统
- 使用 `calibration_analysis.py` 分析传感器标定数据

### 高精地图测试
- 使用 `data_converter.py` 转换地图数据格式
- 使用 `rf_testcase_generator.py` 生成自动化测试用例

### 自动化测试
- 使用 `rf_testcase_generator.py` 批量生成测试用例
- 使用 `selenium_demo.py` 进行Web端测试

---

## 安装依赖

```bash
# 安装Python依赖
cd data-analysis
pip install -r requirements.txt

# Shell脚本（Linux/Unix）
chmod +x vehicle-monitoring/vehicle_system_monitor.sh
```

---

## 项目背景

这些工具在以下项目中实际使用：

### 1. 全场景辅助驾驶系统测试（2020-2022）
- 领克车型NOA系统测试
- 使用CANoe、Python进行数据分析
- 使用Robot Framework进行自动化测试

### 2. 高精地图数据测试（2022-2025）
- 朗歌onemap高精地图项目
- 使用QGIS、Python进行数据验证
- 使用自动化工具提高测试效率

---

## 技术特点

- ✅ 实用性强：来自真实项目需求
- ✅ 易于使用：提供命令行参数
- ✅ 代码规范：包含注释和文档
- ✅ 可扩展：模块化设计

---

## 作者

**何枭雄**
- 5年汽车测试经验
- 专注于智能驾驶和高精地图测试
- 擅长Python数据分析、CANoe报文分析

---

## 许可证

MIT License

---

## 更新日志

- 2025-01: 整理并开源测试工具集
- 2024-12: 优化数据分析工具
- 2023-06: 新增Robot Framework用例生成器
- 2022-10: 新增车载系统监控脚本

---

## 联系方式

如有问题或建议，欢迎联系：
- Email: hcvbnawsedrf1156@gmail.com
- 微信: 19313455442

