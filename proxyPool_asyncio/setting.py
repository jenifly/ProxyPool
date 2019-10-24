# Redis数据库的地址和端口
HOST = 'localhost'
PORT = 6379

# 如果Redis有密码，则添加这句密码，否则设置为None或''
PASSWORD = ''

# 获得代理测试时间界限
GET_PROXY_TIMEOUT = 9
GET_PROXYPAGE_TIMEOUT = 6

# 代理池数量界限
POOL_LOWER_THRESHOLD = 20
POOL_UPPER_THRESHOLD = 100

# 检查周期
VALID_CHECK_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20

# 测试API
TEST_API = 'http://httpbin.org/get'

WEB_API_PORT = 2345