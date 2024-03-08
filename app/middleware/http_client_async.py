"""
@Time    : 2024/3/5 18:18
@Author  : lan
@DESC    : 
"""
import aiohttp
import asyncio


async def async_get(url, params=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return response.status, await response.text()


async def async_post(url, data=None, json=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, json=json, headers=headers) as response:
            return response.status, await response.text()


async def main():
    url = 'https://httpbin.org/get'

    # 发送异步 GET 请求
    status_code, response = await async_get(url)
    print("Status code:", status_code)
    print("Response:", response)

    # 发送异步 POST 请求
    status_code, response = await async_post(url, json={'key': 'value'})
    print("Status code:", status_code)
    print("Response:", response)


# 启动事件循环并运行 main 函数
if __name__ == "__main__":
    asyncio.run(main())