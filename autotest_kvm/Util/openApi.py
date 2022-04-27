import requests
from jsonpath import jsonpath
from Data.common_api import PRO_GPU_URL
from autotest_kvm.Util import support
from autotest_kvm.Util.function import get_token
from autotest_kvm.Util.request import Request

conf = support.read_yaml("cloud_os")["pro-login"]
params = support.read_yaml("cloud_os")["cq-gpu-params"]
Req = Request()


class KVMApi():
    def __init__(self):
        user = conf['username']
        pwd = conf['password']
        Access_Token = get_token(user, pwd)
        self.header = {'Access-Token': Access_Token}
        self.url = PRO_GPU_URL

    def create_kvm(self):
        """

        :return:
        """
        body = {
            "az_id": params['az_id'],
            "is_gpu": params['is_gpu'],
            "gpu_id": params['gpu_id'],
            "utc_time": params['utc_time'],
            "use_number": 1,
            "start_number": 1,
            "vpc_id": params['vpc_id'],
            "region_id": params['region_id'],
            "net_info": {
                "vpc_id": params['vpc_id'],
                "vpc_segment_address": params['vpc_segment_address'],
                "subnet_info": [
                    {
                        "subnet_id": params['subnet_id'],
                        "ip_address": [

                        ],
                        "ip_type": "subnet"
                    }
                ]
            },
            "ecs_spec_info": {
                "ecs_goods_id": params['ecs_goods_id'],
                "spec_family_id": params['spec_family_id'],
                "gic_goods_id": params['gic_goods_id'],
                "ecs_family_name": params['ecs_family_name'],
                "cpu": params['cpu'],
                "ram": params['ram'],
                "gpu": params['gpu'],
                "support_gpu_driver": params['support_gpu_driver'],
                "billing_info": {
                    "gic_goods_id": params['gic_goods_id'],
                    "billing_scheme_id": params['billing_scheme_id'],
                    "billing_cycle_id": "minute",
                    "billing_items": {
                        "ram": {
                            "id": params['ram_bill_id'],
                            "key": "ram"
                        },
                        "local_disk-space": {
                            "id": params['local_disk-space_bill_id'],
                            "key": "local_disk-space"
                        },
                        "local_disk-IOPS": {
                            "id": params['local_disk-IOPS_bill_id'],
                            "key": "local_disk-IOPS"
                        },
                        "gpu": {
                            "id": params['gpu_bill_id'],
                            "key": "gpu"
                        },
                        "os": {
                            "id": params['os_bill_id'],
                            "key": "os"
                        },
                        "cpu": {
                            "id": params['cpu_bill_id'],
                            "key": "cpu"
                        },
                        "local_disk-throughput": {
                            "id": params['local_disk-throughput_bill_id'],
                            "key": "local_disk-throughput"
                        }
                    }
                }
            },
            "disk_info": {
                "billing_info": {
                    params['disk_bill_info']: {
                        "gic_goods_id": params['gic_goods_id'],
                        "billing_scheme_id": params['disk_billing_scheme_id'],
                        "billing_cycle_id": "minute",
                        "billing_items": {
                            "storage_space": {
                                "id": params['disk_storage_space_id'],
                                "key": "storage_space"
                            },
                            "iops": {
                                "id": params['disk_iops_id'],
                                "key": "iops"
                            },
                            "handling_capacity": {
                                "id": params['disk_handling_capacity_id'],
                                "key": "handling_capacity"
                            }
                        }
                    }

                },
                "system_disk": {
                    "ecs_goods_id": params['ecs_goods_id'],
                    "ebs_goods_id": params['ebs_goods_id'],
                    "gic_goods_id": "",
                    "disk_feature": params['disk_feature'],
                    "disk_type": params['disk_type'],
                    "disk_size": params['disk_size'],
                    "is_follow_delete": 1,
                    "ebs_number": 1,
                    "iops": 2520,
                    "handling_capacity": 96,
                    "storage_space": params['disk_size'],
                    "local_disk-IOPS": 2520,
                    "local_disk-space": params['disk_size'],
                    "local_disk-throughput": 96
                },
                "data_disks": [],
            },
            "os_id": params['os_id'],
            "os_type": params['os_type'],
            "num": params['num'],
            "ecs_name": params['ecs_name'],
            "username": params['username'],
            "password": params['password'],
        }
        url = self.url + '/gic_business/v1/ecs/create_ecs/'
        res = Req.request(url, 'post', self.header, body)
        return res


    def startup_kvm(self, EcsIds):
        """
        云主机开机
        :param ecsID:需要开机的主机id
        :return:
        """
        url = self.url + '/gic_business/v1/ecs/operate/'
        body = {
            'ecs_ids': EcsIds,
            'op_type': 'start_up_ecs'
        }
        # post提交方式有两种 表单提交 为data=body json提交为json=body
        # res = requests.post(self.url + '/gic_business/v1/ecs/operate/', headers=self.header, json=body).json()
        res = Req.request(url, 'post', self.header, body)
        print("msg:", res['message'])
        return res

    def shutdown_kvm(self, EcsIds):
        """
        云主机关机
        :param EcsIds:需要关机的云主机id
        :return:
        """
        url = self.url + '/gic_business/v1/ecs/operate/'
        body = {
            'ecs_ids': EcsIds,
            'op_type': 'shutdown_ecs'
        }
        # res = requests.post(self.url + '/gic_business/v1/ecs/operate/', headers=self.header, json=body).json()
        res = Req.request(url, 'post', self.header, body)
        print("msg:", res['message'])
        return res

    def get_kvm_list(self, pageSize):
        """
        获取云主机列表信息
        :param PageIndex: 页数
        :param PageSize: 每页显示数量
        :return:
        """
        body = {
            "page_index": 1,
            "page_size": pageSize
        }
        res = requests.get(self.url + '/gic_business/v1/ecs/ecs_list/', headers=self.header, json=body).json()
        print("msg:", res['message'])
        return res
        # ecs_info = jsonpath.jsonpath(res, '$..[?(@.)]')

    def get_kvm_status(self, ecsIds):
        body = {
            "page_index": 1,
            "page_size": 300,
            "search_info": ecsIds
        }
        res = requests.get(self.url + '/gic_business/v1/ecs/ecs_list/', headers=self.header, json=body).json()
        ecs_list = res['data']['ecs_list']
        for item in ecs_list:
            status = item['status']
            return status

        # for i in range(0, len(ecsId)):
        #     print(ecsId[i])
        #     ecsStatus[i] = jsonpath(res, "$..[?(@.ecs_id == '" + ecsId[i] + "')].status")
        # ecs_status = ','.join(str(i) for i in ecsStatus)
        # print(ecs_status)
        # return ecs_status
        # for ecs_id in ecsId:
        #     print(ecs_id)
        #     ecsStatus = jsonpath(res, "$..[?(@.ecs_id == '" + ecs_id + "')].status")
        #     #ecs_status = ','.join(str(i) for i in ecsStatus)
        # return ecsStatus

    def get_ecs_info(self, ecsId):
        body = {
            "ecs_id": ecsId
        }
        url = 'http://cos-ecs-service.gic.pre/ecs_service/v1/ecs/ecs_info/'
        res = Req.request(url, "post", self.header, body)
        return res
