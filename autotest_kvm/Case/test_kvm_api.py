import jsonpath as jsonpath
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


class TestKvmApi():
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

    @pytest.mark.skip
    def test_kvm_gpu_create(self):
        """
        GPU云主机创建
        """
        response = kvm.create_kvm()
        print(response)
        code = response['code']
        assert code == "Success"

    @pytest.mark.skip
    def test_kvm_gpu_shutdown(self):
        """
        GPU云主机关机
        :return:
        """
        ecsIds = ['ins-n8ioaeiqruuhfmvx']
        response = kvm.shutdown_kvm(ecsIds)
        code = response['code']
        self.assertTrue()
        assert code == "Success"

    @pytest.mark.skip
    def test_kvm_gpu_startup(self):
        """
        GPU云主机开机
        :return:
        """
        ecsIds = ['ins-p6vuowuq0d2ofedn']
        response = kvm.startup_kvm(ecsIds)
        code = response['code']
        assert code == "Success"


    # @pytest.mark.skip
    def test_get_gpu_list(self):
        """
        获取GPU云主机列表
        :return:
        """
        ecs_id = 'ins-cxwqms4qnkzc5hhz'
        # ecs_id = ','.join(str(i) for i in ecs_ids)
        response = kvm.get_kvm_status(ecs_id)
        print(response)


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

    @pytest.mark.skip
    def test_kvm_delete(self):
        """
        删除云主机
        :return:
        """
        body = {
            "ecs_ids": ['ins-pq5s04hqbqx94euc']
        }
        res = requests.post(url + '/gic_business/v1/ecs/delete/', headers=header, json=body).json()
        print("response:", res)
        code = res['code']
        assert code == 'Success'


if __name__ == "__main__":
    t = TestKvmApi()
    t.test_kvm_gpu_shutdown()
    t.test_kvm_gpu_startup()
    t.test_get_gpu_list()
    t.test_kvm_cost()
    t.test_kvm_billing()
    t.test_kvm_gpu_create()
    t.test_kvm_delete()
    t.test_get_status()
