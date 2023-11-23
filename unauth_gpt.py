# -*- coding = utf-8 -*-
# @Time : 2023/11/14
# @Author : cdbc
# @File :unauth_gpt.py
import requests


def check():
    with open("url.txt", "r") as file:
        for url in file:
            url = url.strip()
            burp0_url = url + "/api/session"
            burp0_headers = {"Accept": "application/json, text/plain, */*",
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                           "like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                             "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
            try:
                res = requests.post(burp0_url, headers=burp0_headers, timeout=8)
                # print(res.text)
                if "auth\":true" in res.text:
                    print(url + ' ' + '该链接需要认证')
                else:
                    if "auth\":false" in res.text:
                        # print(url + '该链接不需要认证')
                        burp0_json = {"options": {}, "prompt": "1"}
                        res_new = requests.post(url + "/api/chat-process", headers=burp0_headers, json=burp0_json,
                                                timeout=8)
                        # print(resNew.text)
                        if 'role' in res_new.text:                            # print(res.text)
                            f = open("result.txt", 'a', encoding='utf-8')
                            # f.write(url + ' ' + '延时: ' + str(delay) + ' ms' + '\n')
                            f.write(url)
                            f.close()
                            print(url + ' ' + '该链接可正常使用!!!')
                        else:
                            print(url + ' ' + '该链接无法直接访问')
            except Exception as e:
                print(e)


if __name__ == "__main__":
    check()
