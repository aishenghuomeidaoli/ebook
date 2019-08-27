import time
import json
import requests
from requests import Session
from urllib.parse import urljoin

from flask import g


class JiumoDiary:
    BASE_URL = 'https://www.jiumodiary.com'
    HEADERS = {
        # "Host": "www.jiumodiary.com",
        # "Origin": "https://www.jiumodiary.com",
        "content-type": "application/x-www-form-urlencoded",
        "cache-control": "no-cache",
        # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
        #               "AppleWebKit/537.36 (KHTML, like Gecko) "
        #               "Chrome/76.0.3809.100 Safari/537.36",
    }

    def __init__(self, keyword):
        self.keyword = keyword
        self.request_id = ''
        self.results = []
        self._set_request_id()
        self._set_results()

    @staticmethod
    def _get_session():
        """获取请求会话

        :return:
        """
        if 'jiumo_session' not in g:
            g.jiumo_session = Session()

        return g.jiumo_session

    def _set_request_id(self):
        url = urljoin(self.BASE_URL, 'init_hubs.php')
        data = {
            "q": self.keyword,
            "remote_ip": "",
            # "time_int": 1566454885293
            'time_int':  int((time.time() - 30) * 1000)
        }
        response = requests.post(url, data=data, headers=self.HEADERS)
        try:
            response_data = response.json()
            if response_data['status'] == 'succeed':
                self.request_id = response_data['id']
                return
        except Exception as e:
            print(e)
            pass
        raise Exception

    def _set_results(self, limit=0):
        url = urljoin(self.BASE_URL, 'ajax_fetch_hubs.php')
        data = {
            "id": self.request_id,
            "set": limit,
        }
        response = requests.post(url, data=data, headers=self.HEADERS)
        try:
            response_data = response.json()
            if response_data['status'] == 'succeed':
                self.results.extend(response_data['sources'])
                if response_data['status_extra'] == 'more':
                    self._set_results(limit + 36)
                return

        except Exception as e:
            pass
        raise Exception
