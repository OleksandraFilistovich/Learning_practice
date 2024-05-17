import time
import json
import random
import hashlib

import ujson
import asyncio
import aiohttp
import requests

from multilogin_const import *


MLX_BASE = "https://api.multilogin.com"
MLX_LAUNCHER = "https://launcher.mlx.yt:45001/api/v1"
LOCAL_HOST = "http://127.0.0.1"
HEADERS = {'Accept': 'application/json',
           'Content-Type': 'application/json',}


class Multilogin():

    def __init__(
            self,
            browser_type: str,
            folder_id: str,
            ) -> None:
        
        self.FOLDER_ID = folder_id
        self.browser_type = browser_type

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


    def sign_in(self):

        payload = {
            'email': USERNAME,
            'password': hashlib.md5(PASSWORD.encode()).hexdigest()
        }
        response = requests.post(f'{MLX_BASE}/user/signin', json=payload)

        if response.status_code != 200:
            print(f'\nFailed to login: {response.text}\n')
        else:
            json_response = json.loads(response.text)
            token = json_response.get('data').get('token')

            bearer = 'Bearer ' + token
            self.headers['Authorization'] = bearer

            print(f'Success! Token: {self.headers["Authorization"]}')
    

    def get_browser_core(self):
        
        type = "mimic" if self.browser_type == "chrome" else "stelthfox"
        url = f"https://launcher.mlx.yt:45001/api/v1/load_browser_core?browser_type={type}&version=123"
        payload={}

        response = requests.request("GET", url, headers=self.headers, data=payload)
        return response.json()["status"]["message"]


    '''def refresh_token(self):
        payload = {
            'email': USERNAME,
            'password': hashlib.md5(PASSWORD.encode()).hexdigest()
        }
        response = requests.post(f'{MLX_BASE}/user/refresh_token', json=payload)
        if response.status_code != 200:
            print(f'Failed to refresh: {response.text}')
        else:
            json_response = json.loads(response.text)
            token = json_response.get('data').get('token')
            bearer = 'Bearer ' + token
            self.headers['Authorization'] = bearer
            print(f'Success! Token: {self.headers["Authorization"]}')'''


    def start(self, profile_id: str, headless: bool) -> str:
        url = f"{MLX_LAUNCHER}/profile/f/{self.FOLDER_ID}/p/{profile_id}/start"
        response = requests.get(url=url, headers=self.headers,
                                params={"automation_type": "selenium", "headless_mode": headless})
        print(response.json())
        return response.json()["status"]["message"]


    def quick_start(self, headless: bool) -> str:
        url = f"{MLX_LAUNCHER}/profile/quick"
        body = {
                "browser_type": "mimic" if self.browser_type == "chrome" else "stelthfox",
                "os_type": "Linux",
                "automatization": "selenium",
                "is_headless": headless,
                "parameters": {
                    "flags": {
                        "audio_masking": "mask",
                        "fonts_masking": "mask",
                        "geolocation_masking": "mask",
                        "geolocation_popup": "mask",
                        "graphics_masking": "mask",
                        "graphics_noise": "mask",
                        "localization_masking": "mask",
                        "media_devices_masking": "mask",
                        "navigator_masking": "mask",
                        "ports_masking": "mask",
                        "proxy_masking": "mask",
                        "screen_masking": "mask",
                        "timezone_masking": "mask",
                        "webrtc_masking": "mask"
                    },
                    "storage": {
                        "is_local": True,
                        "save_service_worker": False
                    },
                    "fingerprint": {}
                }}
        response = requests.get(url=url, headers=self.headers, json=body)
        print(response.json())
        return response.json()["status"]["message"]


    def stop(self, profile_id: str) -> str:
        url = f"{MLX_LAUNCHER}/profile/stop/p/{profile_id}"
        response = requests.get(url=url, headers=self.headers)
        print(response.json())
        return response.json()["status"]["message"]
    

    async def create_profile(self) -> str:
        url = f"{MLX_BASE}/profile/create"
        name = f"profile-{random.randint(0,100000)}"
        body = {
                "browser_type": "mimic" if self.browser_type == "chrome" else "stelthfox",
                "os_type": "Linux",
                "folder_id": self.FOLDER_ID,
                "name": name,
                "parameters": {
                    "flags": {
                        "audio_masking": "mask",
                        "fonts_masking": "mask",
                        "geolocation_masking": "mask",
                        "geolocation_popup": "mask",
                        "graphics_masking": "mask",
                        "graphics_noise": "mask",
                        "localization_masking": "mask",
                        "media_devices_masking": "mask",
                        "navigator_masking": "mask",
                        "ports_masking": "mask",
                        "proxy_masking": "mask",
                        "screen_masking": "mask",
                        "timezone_masking": "mask",
                        "webrtc_masking": "mask"
                    },
                    "storage": {
                        "is_local": True,
                        "save_service_worker": False
                    },
                    "fingerprint": {
                        "navigator": None,
                        "screen": None,
                        "media_devices": None,
                        "audio": None,
                        "graphic": None,
                        "fonts": None
                    }
                }}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=self.headers, json=body) as response:
                print(f"Response: {response}")
                print(response.status)
                print(await response.text())
    

    def get_folders(self):
        url = "https://api.multilogin.com/workspace/folders"
        response = requests.get(url=url, headers=self.headers)
        print(response.json())
        return response.json()["data"]["folders"][0]["folder_id"]


    def __repr__(self):
        return f' folder_id: {self.FOLDER_ID};\n browser: {self.browser_type}'



async def main():
    multilogin = Multilogin(BROWSER_TYPE, FOLDER_ID)
    print(multilogin)

    multilogin.sign_in()
    #time.sleep(10)

    await multilogin.create_profile()
    time.sleep(10)

    #print(multilogin.get_folders())
    #time.sleep(10)

    #multilogin.get_browser_core()
    #time.sleep(10)

    multilogin.start(PROFILE_ID, False)
    time.sleep(10)

    multilogin.stop(PROFILE_ID)

if __name__ == '__main__':
    asyncio.run(main())
