#!/usr/bin/python
# -*- coding:utf-8 -*-
#############################################################
#   > File Name: rf_testcase_generator.py
#   > Author: 何枭雄
#   > Mail: hcvbnawsedrf1156@gmail.com
#   > Created Time: Mon 15 Aug 2022 09:06:13 AM CST
#   > Description: Robot Framework测试用例自动生成工具
#############################################################

"""
Robot Framework测试用例自动生成器

功能：
1. 遍历指定目录，自动生成Robot Framework测试用例
2. 自动生成对应的Python测试库文件
3. 生成执行脚本

使用场景：
- 批量生成编译输出检查用例
- 自动化测试用例维护
- 提高测试效率

使用方法：
    python rf_testcase_generator.py /path/to/test/module
"""

import os.path
import os
import time
import threading
import multiprocessing
import datetime
import argparse
import sys
import platform
import re
import psutil


#############################################################
# 参数解析类
#############################################################
class InputArgparseClass(object):
    """
    命令行参数解析类
    """

    def __init__(self):
        """
        初始化参数解析器
        """
        self.parser = argparse.ArgumentParser(
            description='Robot Framework测试用例自动生成工具',
            epilog='示例: python rf_testcase_generator.py /path/to/module'
        )
        self.parser.add_argument("path", type=str, 
                                help='要生成测试用例的模块路径（绝对路径）')
        self.__args = self.parser.parse_args()
        return

    def argparse_get_cmf(self):
        """
        获取解析后的参数
        """
        return self.__args


#############################################################
# 文档处理类
#############################################################
class DocumentProcessingClass(object):
    """
    处理文件夹和文件，生成文件列表字典
    
    输出格式: [{"/path/to/dir":[file1, file2, file3]}, ...]
    """

    def __init__(self, filepath):
        """
        初始化文档处理器
        """
        self.filepath_cmv = filepath
        self.filelist_cmv = []
        self.filedict_cmv = {'': []}

        self.createfiledict_cmf()
        return

    def createfiledict_cmf(self):
        """
        遍历目录，创建文件字典
        """
        for filepath, dirs, files in os.walk(self.filepath_cmv):

            if files == []:
                continue

            self.filedict_cmv = {'': []}
            for filename in files:
                if filepath not in self.filedict_cmv.keys():
                    self.filedict_cmv = {filepath: [filename]}
                else:
                    self.filedict_cmv[filepath].append(filename)

            self.filelist_cmv.append(self.filedict_cmv)

        return self.filelist_cmv


#############################################################
# Robot Framework测试文件创建类
#############################################################
class RFTestFileCreateClass(object):
    """
    根据被测对象生成Robot Framework测试用例和库文件
    """

    def __init__(self, filepath, filelist):
        """
        初始化测试文件创建器
        """
        # 提取模块名称
        temp_modulename = filepath.split("/")
        self.modulename_cmv = temp_modulename[len(temp_modulename) - 1]

        self.filelist_cmv = filelist

        # 创建测试用例目录
        self.testcasepath_cmv = "./testcase/" + self.modulename_cmv
        if not os.path.exists(self.testcasepath_cmv):
            os.makedirs(self.testcasepath_cmv)

        # 创建库文件目录
        self.librariespath_cmv = "./libraries/" + self.modulename_cmv
        if not os.path.exists(self.librariespath_cmv):
            os.makedirs(self.librariespath_cmv)

        self.outputfilepath_cmv = filepath
        self.rftestfile_cmv = self.testcasepath_cmv + "/" + "01_Compilation_Output_Check.robot"

        self.librariesfile_cmv = self.librariespath_cmv + "/" + "Test" + self.modulename_cmv.capitalize() + ".py"
        self.runbashsh_cmv = "run_" + self.modulename_cmv + ".sh"

        # 生成文件
        self.rftestfilecreate_cmf()
        self.librariesfilecreate_cmf()
        self.runbashsh_cmf()

    def rftestfilecreate_cmf(self):
        """
        生成Robot Framework测试用例文件
        """
        with open(self.rftestfile_cmv, mode='w') as rftestfile:
            # 写入Settings部分
            rftestfile.write(
                "*** Settings ***\nForce Tags        priority-P0    owner-xiaoxiong.he    branch-dev\n")
            rftestfile.write("Documentation     Basic test for " + self.outputfilepath_cmv + "\n")
            rftestfile.write(
                "Library           ../../libraries/" + self.modulename_cmv + "/Test" + self.modulename_cmv.capitalize() + ".py\n")
            
            # 写入Variables部分
            rftestfile.write("\n*** Variables ***\n")
            self.outputfile_cmv = "${AD_" + self.modulename_cmv.upper() + "_DIR}"
            rftestfile.write(self.outputfile_cmv + "    " + self.outputfilepath_cmv + "\n")

            # 写入Test Cases部分
            rftestfile.write("\n*** Test Cases ***\n")

            self.pathindex = 1
            for list_item in self.filelist_cmv:
                for outputfilepath, outputfile in list_item.items():
                    self.fileindex = 1

                    # 生成路径检查用例
                    caseindex = ("%02d%02d") % (self.pathindex, self.fileindex)
                    rftestfile.write(
                        "AD_" + self.modulename_cmv.upper() + "_OUTPUT_CHECK_" + caseindex + " Compilation_Path_Check\n")

                    rftestfile.write("    [Documentation]    " + self.modulename_cmv.capitalize() + \
                                     " Compile output path detection\n")
                    rftestfile.write("    [Timeout]          300\n    [Setup]            Setup\n")
                    rftestfile.write("    ${Returnvar} =     Compilation Path Check    " + outputfilepath + "\n")
                    rftestfile.write("    SHOULD BE TRUE     ${Returnvar}\n")
                    rftestfile.write("    [Teardown]         Teardown\n")
                    rftestfile.write("\n\n")

                    # 生成文件检查用例
                    for outputfile_item in outputfile:
                        caseindex = ("%02d%02d") % (self.pathindex, self.fileindex)
                        rftestfile.write(
                            "AD_" + self.modulename_cmv.upper() + "_OUTPUT_CHECK_" + caseindex + " Compilation_File_Check\n")

                        rftestfile.write(
                            "    [Documentation]    " + outputfilepath + " Compile output file detection\n")
                        rftestfile.write("    [Timeout]          300\n    [Setup]            Setup\n")
                        rftestfile.write("    ${Filepath} =    CATENATE    " + outputfilepath + "\n")
                        rftestfile.write("    ${Returnvar} =     Compilation File Check    ${Filepath}    " + \
                                         outputfile_item + "\n")
                        rftestfile.write("    SHOULD BE TRUE     ${Returnvar}\n")
                        
                        # 读取文件内容
                        rftestfile.write("    ${data} =     read_file    ${Filepath}    " + \
                                         outputfile_item + "\n")
                        
                        # 根据用例编号添加特定断言
                        if caseindex=="0101":
                            rftestfile.write("    ${a}=         arrest_result    ${data}     $.file_cache.cache_path    transparent-cache/file\n")
                            rftestfile.write("    SHOULD BE TRUE     ${a}\n")
                        if caseindex=="0102":
                            rftestfile.write("    ${b}=         arrest_result    ${data}     $.identify.algorithmVersion    CSVEHXV_v1.5.0.0\n")
                            rftestfile.write("    SHOULD BE TRUE     ${b}\n")
                        if caseindex=="0103":
                            rftestfile.write("    ${c}=         arrest_result    ${data}     $.CommonConfig.CollectMode    RMS\n")
                            rftestfile.write("    SHOULD BE TRUE     ${c}\n")
                        if caseindex=="0104":
                            rftestfile.write("    ${d}=         arrest_result    ${data}     $.ins.shiftSwitch    1\n")
                            rftestfile.write("    SHOULD BE TRUE     ${d}\n")
                            
                        rftestfile.write("    [Teardown]         Teardown\n")
                        rftestfile.write("\n\n")
                        self.fileindex = self.fileindex + 1

                self.pathindex = self.pathindex + 1

    def librariesfilecreate_cmf(self):
        """
        生成Python测试库文件
        """
        with open(self.librariesfile_cmv, mode='w') as librariesfile:
            librariesfile.write("#!/usr/bin/python\n# -*- coding:utf-8 -*-\n")
            librariesfile.write("#############################################################\n")
            librariesfile.write("#   > File Name: Test" + self.modulename_cmv.capitalize() + ".py\n")
            librariesfile.write("#   > Author: Auto Generated\n")
            librariesfile.write("#   > Mail:\n")

            now = datetime.datetime.now()
            librariesfile.write("#   > Created Time: " + str(now) + "\n")
            librariesfile.write("#############################################################\n\n")

            # 导入必要的库
            librariesfile.write("import os.path\nimport os\nimport time\nimport threading\nimport multiprocessing\n")
            librariesfile.write("import datetime\nimport argparse\nimport sys\nimport platform\nimport re\n" + \
                                "import psutil\nimport json\nimport jsonpath\nimport yaml\n")

            librariesfile.write("\n#############################################################\n")
            librariesfile.write("# 测试库类\n")
            librariesfile.write("#############################################################\n")
            
            # 创建测试类
            librariesfile.write("class Test" + self.modulename_cmv.capitalize() + "(object):\n")
            librariesfile.write("    def __init__(self):\n")
            librariesfile.write("        print(\"[INFO] 初始化测试库\")\n\n")
            
            librariesfile.write("    def setup(self):\n")
            librariesfile.write("        print(\"[INFO] 测试用例Setup\")\n\n")
            
            librariesfile.write("    def teardown(self):\n")
            librariesfile.write("        print(\"[INFO] 测试用例Teardown\")\n\n")
            
            # 路径检查方法
            librariesfile.write("    def compilation_path_check(self, output_path):\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        检查编译输出路径是否存在\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        try:\n")
            librariesfile.write("            result = os.path.exists(output_path)\n")
            librariesfile.write("        except Exception as error:\n")
            librariesfile.write("            result = False\n")
            librariesfile.write("        finally:\n")
            librariesfile.write("            return result\n\n")

            # 文件检查方法
            librariesfile.write("    def compilation_file_check(self, output_path, output_filename):\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        检查编译输出文件是否存在\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        try:\n")
            librariesfile.write("            filepath = output_path + \"/\" + output_filename\n")
            librariesfile.write("            result = os.path.isfile(filepath)\n")
            librariesfile.write("        except Exception as error:\n")
            librariesfile.write("            result = False\n")
            librariesfile.write("        finally:\n")
            librariesfile.write("            return result\n\n")

            # 文件读取方法
            librariesfile.write("    def read_file(self, output_path, output_filename):\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        读取文件内容，支持JSON/YAML/META格式\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        filepath = output_path + \"/\" + output_filename\n")
            librariesfile.write("        if not os.path.exists(filepath):\n")
            librariesfile.write("            return False\n\n")

            librariesfile.write("        if filepath.endswith('.yaml'):\n")
            librariesfile.write("            with open(filepath, 'r', encoding='utf-8') as load_f:\n")
            librariesfile.write("                yaml_info = yaml.safe_load(load_f)\n")
            librariesfile.write("                return yaml_info\n")
            
            librariesfile.write("        if filepath.endswith('.json'):\n")
            librariesfile.write("            with open(filepath, 'r') as f:\n")
            librariesfile.write("                data = json.load(f)\n")
            librariesfile.write("            return data\n")
            
            librariesfile.write("        if filepath.endswith('.meta'):\n")
            librariesfile.write("            with open(filepath, 'r') as s:\n")
            librariesfile.write("                data2 = json.load(s)\n")
            librariesfile.write("            return data2\n\n")

            # 断言结果检查方法
            librariesfile.write("    def arrest_result(self, data: dict, act, ect):\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        使用jsonpath提取数据并断言\n")
            librariesfile.write("        \"\"\"\n")
            librariesfile.write("        m = jsonpath.jsonpath(data, act)\n")
            librariesfile.write("        m = str(m[0])\n")
            librariesfile.write("        if m:\n")
            librariesfile.write("            if m == ect:\n")
            librariesfile.write("                return True\n")
            librariesfile.write("            else:\n")
            librariesfile.write("                return False\n")
            librariesfile.write("        else:\n")
            librariesfile.write("            return False\n\n")

            librariesfile.write("\n#############################################################\n")
            librariesfile.write("# 主函数\n")
            librariesfile.write("#############################################################\n")
            librariesfile.write("if __name__ == \"__main__\":\n")
            librariesfile.write("    test_obj = Test" + self.modulename_cmv.capitalize() + "()\n")
            librariesfile.write("    print(\"测试库加载成功\")\n")

    def runbashsh_cmf(self):
        """
        生成执行脚本
        """
        with open(self.runbashsh_cmv, mode='w') as runbashshfile:
            runbashshfile.write("#!/bin/bash\n")
            runbashshfile.write(
                "#==============================================================================================================\n")
            runbashshfile.write("# Robot Framework测试执行脚本\n")
            runbashshfile.write(
                "#==============================================================================================================\n")
            runbashshfile.write("set -ex\n")
            runbashshfile.write("robot -L trace -d rfoutput --exclude not-readyOrnot-run \\\n")
            runbashshfile.write("        --include priority-P0 \\\n")
            runbashshfile.write("        testcase/" + self.modulename_cmv + "/")


#############################################################
# 主函数
#############################################################
if __name__ == "__main__":
    print("="*60)
    print("Robot Framework测试用例自动生成工具 v1.0")
    print("="*60)
    
    temp_argparse = InputArgparseClass()
    stability_args = temp_argparse.argparse_get_cmf()
    filelist = DocumentProcessingClass(stability_args.path)
    RFTestFileCreateClass(stability_args.path, filelist.filelist_cmv)
    
    print("\n[SUCCESS] 测试用例生成完成！")
    print(f"生成位置：./testcase/{stability_args.path.split('/')[-1]}/")

