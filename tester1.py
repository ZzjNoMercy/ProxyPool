import requests
from proxypool.db import RedisClient
from proxypool.setting import *
from requests import exceptions



class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    def test_single_proxy(self,proxy):
        try:
            proxies = {'http':proxy,'https': proxy}
            print('正在测试', proxy)
            r = requests.get(url = TEST_URL, headers = headers,timeout = 10,proxies = proxies)
            if r.status_code in VALID_STATUS_CODES:
                self.redis.max(proxy)
                print('代理可用', proxy)
            else:
                self.redis.decrease(proxy)
                print('请求响应码不合法 ', r.status_code, 'IP', proxy)
        except (exceptions.ConnectionError,exceptions.HTTPError,exceptions.Timeout,exceptions.ProxyError):
            self.redis.decrease(proxy)
            print('代理请求失败', proxy)

    # def run(self):
    #     print('测试器开始运行')
    #     try:
    #         count = self.redis.count()
    #         print('当前剩余', count, '个代理')
    #         for i in range(0, count, BATCH_TEST_SIZE):
    #             start = i
    #             stop = min(i + BATCH_TEST_SIZE, count)
    #             print('正在测试第', start + 1, '-', stop, '个代理')
    #             test_proxies = self.redis.batch(start, stop)
    #             for proxy in test_proxies:
    #                 self.test_single_proxy(proxy)
    #     except Exception as e:
    #         print('测试器发生错误', e.args)

    def run(self):
        print('测试器开始运行')
        count = self.redis.count()
        print('当前剩余', count, '个代理')
        for i in range(0, count, BATCH_TEST_SIZE):
            start = i
            stop = min(i + BATCH_TEST_SIZE, count)
            print('正在测试第', start + 1, '-', stop, '个代理')
            test_proxies = self.redis.batch(start, stop)
            for proxy in test_proxies:
                self.test_single_proxy(proxy)