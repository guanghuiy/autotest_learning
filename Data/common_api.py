import os

GET_TOKEN_URL = "http://api2.capitalonline.net/gic/v1/get_token/"
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML_PATH = os.path.join(BASE_PATH, "Data")
TEST_GPU_URL = "http://cloudos-ecs-front.gic.test"
PRO_GPU_URL = "https://cds-os-ecs-front.capitalonline.net"
