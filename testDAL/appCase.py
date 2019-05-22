#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/3/7 19:16 
# @Author : Zero 
# @Site :  
# @File : appCase.py 
# @Software: PyCharm
import json
import os
from common import operateYaml
from testMode import appCase
from common import operateElement as bo
import sys
from common import OperateFile as operateFile
from common.variable import GetVariable as common
from common import testLogScreen
import time
from common.commonElemnt import Element as element
class AppCase():
    def __init__(self, **kwargs):
        '''

        :param kwargs:
        test_module:'模块名'
        GetAppCaseInfo:'用例介绍'
        package:'包名'
        devices:'设备名'
        '''
        self.test_module = kwargs['test_module']
        self.GetAppCaseInfo = kwargs['GetAppCaseInfo']
        self.GetAppCase = kwargs["GetAppCase"]
        # self.test_module = kwargs['test_module']
        self.driver = kwargs["driver"]
    def getModeList(self, f):
        bs = []
        gh = operateYaml.getYam(f)
        for i in range(len(gh)):
            if i  == 0 :
                self.GetAppCaseInfo.test_id = gh[i].get("test_id", "false")
                self.GetAppCaseInfo.test_intr = gh[i].get("test_intr", "false")
                # self.GetAppCaseInfo.test_module = gh[i].get("test_module", "false")
                # bt = self.GetAppCase
            self.GetAppCase.element_info = gh[i].get("element_info", "false")
            self.GetAppCase.element_id = gh[i].get("element_id", "false")
            self.GetAppCase.enable = gh[i].get("enable", "false")
            self.GetAppCase.index = gh[i].get("index", "false")
            # 操作类型
            self.GetAppCase.operate_type = gh[i].get("operate_type", "false")
            # 输入文字
            self.GetAppCase.text = gh[i].get("text", "false")  # 对应by_link_text

            # 验证类型
            self.GetAppCase.find_type = gh[i].get("find_type", "false")

            self.GetAppCase.time = gh[i].get("time", 0)

            bs.append(json.loads(json.dumps(self.GetAppCase().to_primitive())))
        return bs
    def execCase(self, f, **kwargs):
        '''

        :param f: 用例文件
        :param kwargs:
        test_name：用例名
        ls_last：最后一个用例，1，0
        :return:
        '''
        bc = self.getModeList(f)
        go = bo.OperateElement(self.driver)
        ce = element(common.COMMONELEMENT)
        _d_report_common = {"test_success": 0, "test_failed": 0, "test_sum": 0}  # case的运行次数
        ch_check = {}
        _d_report_common['test_sum'] += 1
        result = True
        for k in bc:
            if k["operate_type"] != "false" and 1 == 1:
                # k["devices"] = self.devices
                if ce.isElemnet(k["element_id"]):
                    k = ce.joinElement(k, k["element_id"])
                    if k["enable"] == 1:
                        go.opearate_element(k)
                        # if go.findElement(ch_check):
                        #     pass
                        # else:
                        #     self.report(go, k, _d_report_common, kwargs)
                        # if go.findElement(ch_check) is False:
                        #     return False
                    else:
                        print("元素{0}enable为{1}不被启用".format(k["element_id"], k["enable"]))
                else:
                    print("操作元素不存在")
            else:
                if ce.isElemnet(k["element_id"]):
                    k = ce.joinElement(k, k["element_id"])
                    if k["enable"] == 1:
                        ch_check = k
                    else:
                        print("元素{0}enable为{1}不被启用".format(k["element_id"], k["enable"]))
                else:
                    print("验证元素不存在")
        # time.sleep(5)

        # return True
        self.report(go, ch_check, _d_report_common, kwargs)
    # 整体用例运行
    def report(self, go, ch_check, _d_report_common, kwargs):
        if go.findElement(ch_check):
            _d_report_common["test_success"] += 1
            self.GetAppCaseInfo.test_result = "成功"
            self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
            self.GetAppCaseInfo.test_image = None
            self.GetAppCaseInfo.test_reason = ""
        else:
            _d_report_common['test_failed'] += 1
            self.GetAppCaseInfo.test_result = "失败"
            self.GetAppCaseInfo.test_reason = "找不到元素"
            self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
            ng_img = testLogScreen.screenshotNG(caseName=kwargs["test_name"], driver=self.driver,
                                                resultPath=common.SCREEN_IMG_PATH)
            self.GetAppCaseInfo.test_image = ng_img
        self.GetAppCaseInfo.test_name = kwargs["test_name"]
        self.GetAppCaseInfo.test_module = self.test_module
        # self.GetAppCaseInfo.test_phone_name = self.get_phone_name()[0]
        info_case = json.loads(json.dumps(self.GetAppCaseInfo().to_primitive()))
        self.write_detail(info_case, f=common.REPORT_INFO_PATH, key="info")  # 写入所有的case包括，init,info中的excel中的case情况
    # 整体用例运行
    # def report(self, _d_report_common, kwargs, result):
    #     if result:
    #         _d_report_common["test_success"] += 1
    #         self.GetAppCaseInfo.test_result = "成功"
    #         self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
    #         self.GetAppCaseInfo.test_image = None
    #         self.GetAppCaseInfo.test_reason = ""
    #     else:
    #         _d_report_common['test_failed'] += 1
    #         self.GetAppCaseInfo.test_result = "失败"
    #         self.GetAppCaseInfo.test_reason = "找不到元素"
    #         self.write_report_collect(_d_report_common, f=common.REPORT_COLLECT_PATH)  # 写入case运行的总个数
    #         ng_img = testLogScreen.screenshotNG(caseName=kwargs["test_name"], driver=self.driver,
    #                                             resultPath=common.SCREEN_IMG_PATH)
    #         self.GetAppCaseInfo.test_image = ng_img
    #     self.GetAppCaseInfo.test_name = kwargs["test_name"]
    #     self.GetAppCaseInfo.test_module = self.test_module
    #     # self.GetAppCaseInfo.test_phone_name = self.get_phone_name()[0]
    #     info_case = json.loads(json.dumps(self.GetAppCaseInfo().to_primitive()))
    #     self.write_detail(info_case, f=common.REPORT_INFO_PATH, key="info")  # 写入所有的case包括，init,info中的excel中的case情况
    '''
    读取文件执行结果
    '''
    def read_detail_report(self, f=""):
       op = operateFile.OperateFile(f, "r")
       return op.read_txt_row()
    # 写入统计case的info,init情况,累计执行结果到列表中
    def write_detail(self, json, f="", key="info"):
        '''

        :param json: 存储的json
        :param f: 存储的文件文字，一般是info,和init的位置
        :param key:  info和init两个值,要和f的路径匹配;REPORT_INFO_PATH对应info,REPORT_INIT对应init
        这里的key就是init,当f的值为REPORT_INFO_PATH,这里
        注：这里得统计方法会在原文件基础上进行统计
        :return:
        '''
        _read_json_temp = self.read_detail_report(f)
        _result = {}
        if len(_read_json_temp) > 0:
            _read_json = eval(_read_json_temp)
            _read_json[key].append(json)
            _result = _read_json
        else:
            _result[key] = []
            _result[key].append(json)
        op = operateFile.OperateFile(f, "w")
        op.write_txt("%s \n"% str(_result))

    # 写入统计总的case的运行次数
    def write_report_collect(self, json, f=""):
        _read_json_temp = self.read_detail_report(f)
        op = operateFile.OperateFile(f, "w")
        _result = {}
        if len(_read_json_temp) > 0:
            _read_json = eval(_read_json_temp)
            for i in _read_json:
                if i == "test_success" or i == "test_failed" or i == "test_sum":  # 统计总的case的运行次数
                    _result[i] = int(_read_json[i]) + int(json[i])
                else:
                    _result[i] = _read_json[i]
        if len(_result) > 0:
            op.write_txt(str(_result))
        else:
            op.write_txt(str(json))
    #写入统计case的info，init情况
    # def write_detail
# b = AppCase(GetAppCaseInfo=appCase.GetAppCaseInfo, package="123", devices="456", GetAppCase=appCase.GetAppCase)
# s = b.getModeList(os.getcwd()+"\home_login.yaml")
# print("s:",s)