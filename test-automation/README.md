# 自动化测试工具

## 概述

包含Robot Framework测试用例自动生成工具和Selenium Web自动化测试示例。

---

## 工具列表

### 1. rf_testcase_generator.py - Robot Framework用例生成器

自动生成Robot Framework测试用例的工具，大幅提高测试用例编写效率。

**功能特点**：
- 自动遍历目录结构
- 生成标准化测试用例
- 自动生成Python测试库文件
- 生成执行脚本
- 支持JSON/YAML/META文件内容断言

**使用方法**：
```bash
python rf_testcase_generator.py /path/to/test/module
```

**生成内容**：
```
./testcase/[模块名]/
└── 01_Compilation_Output_Check.robot    # 测试用例文件

./libraries/[模块名]/
└── Test[模块名].py                       # Python测试库

./run_[模块名].sh                         # 执行脚本
```

**生成的测试用例包含**：
- 编译输出路径检查
- 编译输出文件检查
- 配置文件内容断言
- Setup/Teardown结构

**应用场景**：
- 编译输出验证
- 配置文件检查
- 数据文件验证
- 批量测试用例生成

---

### 2. selenium_demo.py - Selenium自动化测试示例

基于Selenium的Web自动化测试框架示例。

**功能**：
- 自动化浏览器操作
- 支持Chrome、Firefox等浏览器
- 隐式等待设置
- 窗口最大化

**使用方法**：
```bash
# 确保已安装chromedriver
python selenium_demo.py
```

**扩展方向**：
- 页面元素定位
- 表单自动填写
- 截图功能
- 多浏览器兼容

---

## 技术要点

### Robot Framework用例生成器

**核心技术**：
- `os.walk()` 遍历目录树
- `argparse` 命令行参数解析
- 字符串格式化生成代码
- 文件操作和目录管理

**代码结构**：
1. `InputArgparseClass` - 参数解析
2. `DocumentProcessingClass` - 文档处理
3. `RFTestFileCreateClass` - 测试文件生成

**生成的测试库功能**：
- `compilation_path_check()` - 路径存在性检查
- `compilation_file_check()` - 文件存在性检查
- `read_file()` - 读取JSON/YAML/META文件
- `arrest_result()` - 使用jsonpath断言内容

---

## 使用示例

### 为perception模块生成测试用例

```bash
# 假设模块路径为 /data/output/perception
python rf_testcase_generator.py /data/output/perception

# 生成的文件结构
testcase/perception/
└── 01_Compilation_Output_Check.robot

libraries/perception/
└── TestPerception.py

run_perception.sh

# 执行测试
bash run_perception.sh
```

### 生成的测试用例示例

```robotframework
*** Settings ***
Force Tags        priority-P0    owner-xiaoxiong.he    branch-dev
Documentation     Basic test for /data/output/perception
Library           ../../libraries/perception/TestPerception.py

*** Variables ***
${AD_PERCEPTION_DIR}    /data/output/perception

*** Test Cases ***
AD_PERCEPTION_OUTPUT_CHECK_0101 Compilation_Path_Check
    [Documentation]    Perception Compile output path detection
    [Timeout]          300
    [Setup]            Setup
    ${Returnvar} =     Compilation Path Check    /data/output/perception
    SHOULD BE TRUE     ${Returnvar}
    [Teardown]         Teardown

AD_PERCEPTION_OUTPUT_CHECK_0101 Compilation_File_Check
    [Documentation]    /data/output/perception Compile output file detection
    [Timeout]          300
    [Setup]            Setup
    ${Filepath} =    CATENATE    /data/output/perception
    ${Returnvar} =     Compilation File Check    ${Filepath}    config.json
    SHOULD BE TRUE     ${Returnvar}
    ${data} =     read_file    ${Filepath}    config.json
    [Teardown]         Teardown
```

---

## 实际应用

### 在高精地图项目中的应用

我在朗歌onemap高精地图项目中，使用这个工具批量生成了：
- 地图数据输出验证用例
- 配置文件完整性检查用例
- 算法版本验证用例

**效果**：
- 测试用例编写效率提升 **80%**
- 测试用例标准化，易于维护
- 支持参数化配置，灵活性高

---

## 依赖安装

```bash
pip install psutil jsonpath pyyaml robotframework
```

---

## 注意事项

1. 输入路径必须是绝对路径
2. 生成的用例需要根据实际情况调整断言值
3. 执行前确保Robot Framework已安装
4. 测试库文件可以根据需要扩展功能

---

## 作者

何枭雄
- 5年汽车测试经验
- 擅长自动化测试工具开发
- Robot Framework实践者

