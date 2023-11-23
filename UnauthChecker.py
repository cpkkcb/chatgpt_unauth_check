# -*- coding = utf-8 -*-
# @Time : 2023/11/14
# @Author : cdbc
# @File :UnauthChecker.py

import requests


class UnauthChecker:
    """
    未授权访问检查工具
    """

    def __init__(self, url_file: str, result_file: str):
        self._url_file = url_file
        self._result_file = result_file
        self._cache = set() # 缓存检测是否重复访问

    def _fetch_url(self, url: str) -> bool:
        """
        检查指定URL是否存在未授权访问情况
        """
        # 去除末尾斜杠
        url = url.rstrip('/')
        if url in self._cache:
            return False

        burp0_url = f"{url}/api/session"
        burp0_headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close"
        }
        try:
            res = requests.post(burp0_url, headers=burp0_headers, timeout=10)
            self._cache.add(url)
            if "auth\":true" in res.text:
                print(f"{url} 该链接不存在未授权访问情况")
            else:
                if "auth\":false" in res.text:
                    burp0_json = {"options": {}, "prompt": "1"}
                    res_new = requests.post(
                        f"{url}/api/chat-process", headers=burp0_headers, json=burp0_json, timeout=8)
                    if 'role' in res_new.text:
                        with open(self._result_file, "a", encoding="utf-8") as f:
                            f.write(url + '\n')
                        print(f"{url} 该链接存在未授权访问情况，请及时修复！！")
                    else:
                        print(f"{url} 该链接无法直接访问")
        except Exception as e:
            print(f"{url} 链接访问超时或出错，请重新尝试")

    def check(self):
        """
        对URL文件中的所有链接逐一进行检查
        """
        with open(self._url_file, "r") as file:
            for url in file:
                self._fetch_url(url.strip())


if __name__ == "__main__":
    checker = UnauthChecker("url.txt", "result.txt")
    checker.check()
