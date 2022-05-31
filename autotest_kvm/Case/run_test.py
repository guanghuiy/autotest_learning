import allure
import os

import pytest

if __name__ == '__main__':
    results_dir = "./test_result"
    report_dir = "./test_report"
    args = ['-sv', '--alluredir=%s' % results_dir, '--clean-alluredir', './Case/test_kvm_api.py']
    pytest.main(args)
    ret = os.system("allure generate %s -o %s --clean" % (results_dir, report_dir))
    print(ret)
    if ret:
        print("生成测试报告失败")
    else:
        print("生成测试报告成功")
