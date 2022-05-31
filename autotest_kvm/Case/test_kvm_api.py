import logging
from time import sleep, time

import allure
import pytest

from Data.common_api import TEST_GPU_URL, PRO_GPU_URL
from autotest_kvm.Util import support
from autotest_kvm.Util.function import get_token
import requests

from autotest_kvm.Util.openApi import KVMApi

conf = support.read_yaml('cloud_os')['pro-login']
user = conf['username']
pwd = conf['password']
Access_Token = get_token(user, pwd)
header = {'Access-Token': Access_Token}
url = PRO_GPU_URL

kvm = KVMApi()
log = logging.getLogger("kvm_main_process_autotest")


@allure.feature("kvm云主机主流程自动化测试")
class TestKvmApi:

    @pytest.mark.skip
    def test_kvm_billing(self):
        """
        云主机扣费
        :return:
        """
        body = {
            "cloud_id": "ins-mfguykeqb2xi9c96",
            "now_time": "2022-03-10 00:00:00"
        }
        res = requests.post("http://billing-service.gic.pre/v1/billing/billing/one", headers=None, json=body).json()
        print("response:", res)
        code = res['msg']
        assert code == "success"

    @pytest.mark.skip
    def test_kvm_cost(self):
        """
        云主机出账
        :return:
        """
        body = {
            "customerNo": "E890358"
        }
        res = requests.post("http://acctservice.gic.pre/post_charge_new", headers=None, json=body).json()
        print("response：", res)
        code = res["msg"]
        assert code == "success"

    # @pytest.mark.skip
    @allure.title("kvm云主机创建测试")
    def test_kvm_create(self):
        """
        云主机创建
        """
        log.info("kvm云主机开始创建测试用例")
        response = kvm.create_kvm()
        code = response['code']
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(5)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                global ecs_id
                ecs_id = task['cloud_id']
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "running":
                        result = "success"
                        log.info("云主机创建任务执行完成，云主机为运行中状态！")
                        break
                    else:
                        result = "error"
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task['detail']
                    log.error("云主机创建任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response["message"]
            log.error("云主机创建任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机创建任务结束，等候2分钟继续执行下一个测试用例。")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机关机测试")
    def test_kvm_shutdown(self):
        """
        GPU云主机关机
        :return:
        """
        log.info("kvm云主机开始执行关机测试用例")
        response = kvm.shutdown_kvm(ecs_id)
        code = response["code"]
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "shutdown":
                        result = "success"
                        log.info("云主机关机任务执行成功，云主机为已关机状态！")
                        break
                    else:
                        result = "error"
                        log.error("云主机关机任务执行失败！")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task["detail"]
                    log.error("云主机关机任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.error("云主机关机任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机关机任务结束，等待2分钟继续执行下一个测试用例")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机开机测试")
    def test_kvm_startup(self):
        """
        GPU云主机开机
        :return:
        """
        log.info("kvm云主机开始执行开机测试用例")
        response = kvm.startup_kvm(ecs_id)
        code = response["code"]
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "running":
                        result = "success"
                        log.info("云主机开机任务执行成功，云主机为已运行状态！")
                        break
                    else:
                        result = "error"
                        log.error("云主机开机任务执行失败！")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task["detail"]
                    log.error("云主机开机任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.error("云主机开机任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机开机任务结束，等待2分钟继续执行下一个测试用例")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机更改密码测试")
    def test_kvm_change_password(self):
        """
        云主机重置密码测试用例
        :return:
        """
        log.info("kvm云主机开始执行重置密码测试用例")
        new_pwd = 'QQQqqq666'
        response = kvm.change_password(ecs_id, new_pwd)
        code = response['code']
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "running":
                        sleep(2)
                        ecs_info = kvm.select_ecs_info(ecs_id)
                        encrypted_pwd = ecs_info['password']
                        decode_res = kvm.decode(encrypted_pwd)
                        decode_pwd = decode_res['data']['plain_text']
                        if decode_pwd == new_pwd:
                            result = "success"
                            log.info("云主机重置密码任务执行成功，云主机为运行中状态！")
                            break
                        else:
                            result = "error"
                            log.info("云主机重置密码任务执行失败，密码没有更改为新设置的密码！")
                            break
                    else:
                        result = "error"
                        log.info("云主机重置密码任务失败")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task["detail"]
                    log.info("云主机重置密码任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.info("云主机重置密码任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机重置密码任务结束，等候2分钟后继续执行下个测试用例。")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机重启测试")
    def test_kvm_restart(self):
        """
        云主机重启
        :return:
        """
        log.info("kvm云主机开始执行重启测试用例")
        response = kvm.restart_kvm(ecs_id)
        code = response["code"]
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "running":
                        result = "success"
                        log.info("云主机重启任务执行成功，云主机为运行中状态！")
                        break
                    else:
                        result = "error"
                        log.error("云主机重启任务失败")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task["detail"]
                    log.error("云主机重启任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.info("云主机重启任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机重启任务结束，等待2分钟继续执行下一个测试用例")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机更换操作系统测试")
    def test_kvm_change_os(self):
        """
        更换操作系统
        :return:
        """
        log.info("kvm云主机开始执行更换操作系统测试用例")
        self.test_kvm_shutdown()
        new_pwd = 'QQQqqq222'
        response = kvm.change_os(ecs_id, new_pwd)
        code = response['code']
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_status = kvm.get_kvm_status(ecs_id)
                    if kvm_status == "running":
                        sleep(2)
                        ecs_info = kvm.select_ecs_info(ecs_id)
                        encrypted_pwd = ecs_info['password']
                        decode_res = kvm.decode(encrypted_pwd)
                        decode_pwd = decode_res['data']['plain_text']
                        if decode_pwd == new_pwd:
                            result = "success"
                            log.info("云主机更换操作系统任务执行成功，云主机为运行中状态！")
                            break
                        else:
                            result = "error"
                            log.error("云主机更换操作系统任务执行失败！")
                            break
                    else:
                        result = "error"
                        log.error("云主机更换操作系统任务执行失败！")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task["detail"]
                    log.error("云主机更换操作系统任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.error("云主机更换操作系统任务下发失败：%s" % err_msg)
        assert result == "success"
        log.info("云主机更换操作系统任务结束，等待2分钟继续执行下一个测试用例")
        sleep(120)

    # @pytest.mark.skip
    @allure.title("kvm云主机删除测试")
    def test_kvm_delete(self):
        """
        删除（销毁）云主机
        :return:
        """
        log.info("kvm云主机开始执行删除（销毁）测试用例")
        response = kvm.delete_kvm(ecs_id)
        code = response['code']
        if code == "Success":
            event_id = response['data']['event_id']
            sleep(3)
            end_time = time() + 600
            result = "timeout"
            while time() < end_time:
                sleep(5)
                task = kvm.select_ecs_task(event_id)
                task_status = task['status']
                task_processing = task['processing']
                task_type = task['task_type']
                log.info("云主机 %s 任务状态为：%s，任务完成进度为：%s" % (task_type, task_status, task_processing))
                if task_status == "success":
                    kvm_info = kvm.select_ecs_info(ecs_id)
                    kvm_status = kvm_info['status']
                    if kvm_status == "destroy":
                        result = "success"
                        log.info("云主机删除（销毁）任务执行成功，云主机为已销毁状态！")
                        break
                    else:
                        result = "error"
                        log.error("云主机删除（销毁）任务执行失败")
                        break
                elif task_status == "failed":
                    result = "error"
                    task_msg = task['detail']
                    log.error("云主机删除（销毁）任务执行错误：%s" % task_msg)
                    break
        else:
            result = "error"
            err_msg = response['message']
            log.error("云主机删除（销毁）任务下发失败：%s" % err_msg)
        assert result == 'success'
        log.info("云主机删除（销毁）任务结束，至此kvm主流程测试用例全部结束，请查看测试报告！")

    @pytest.mark.skip
    def test_gpu(self):
        """
        获取GPU云主机列表
        :return:
        """
        # response = kvm.get_kvm_status(ecs_id)
        # print(response)
        # kvm_status = kvm.get_kvm_status('ins-jujmkj4q7yl7xw6e')
        # print(kvm_status)
        ecs_info = kvm.select_ecs_info('ins-kmsoeyfqeyx7lw4e')
        encrypted_pwd = ecs_info['password']
        decode_res = kvm.decode(encrypted_pwd)
        decode_pwd = decode_res['data']['plain_text']
        print(decode_pwd)

        # ecs_status = jsonpath.jsonpath(response, "$..[?(@.ecs_id in '" + ecsId + "' )].status")
        # print("ecs_status:", ecs_status)
        # ecs_ids = jsonpath.jsonpath(response, "$..[?(@.ecs_name == 'amd-a5000-10c16g-001')].private_net")
        # 获取主私网ip
        # response = kvm.get_kvm_list(21)
        # private_nets = jsonpath.jsonpath(response, "$..private_net")
        # print(response)
        # print("private_nets:", private_nets)
        # code = response['code_msg']
        # assert code == "success"


if __name__ == "__main__":
    t = TestKvmApi()
    t.test_kvm_cost()
    t.test_kvm_billing()
    t.test_gpu()
    t.test_kvm_create()
    t.test_kvm_shutdown()
    t.test_kvm_startup()
    t.test_kvm_change_password()
    t.test_kvm_restart()
    t.test_kvm_change_os()
    t.test_kvm_delete()
