import time
from http import HTTPStatus

import requests


class Task:
    def __init__(self, task_id, base_url):
        self.task_id = task_id
        self.base_url = base_url
        self.status = None
        self.result = None

    def wait(self):
        while self.status not in ('done', 'error'):
            if self.status:
                time.sleep(1)
            self.get_status()
            if not self.status:
                print("Error getting status")
                return
        self.get_result()

    def get_status(self) -> None:
        response = requests.get(f'{self.base_url}/status/{self.task_id}')
        jdata = self._print(response)
        self.status = jdata.get('status')

    def get_result(self) -> None:
        response = requests.get(f'{self.base_url}/result/{self.task_id}')
        jdata = self._print(response)
        self.status = jdata.get('result')

    @staticmethod
    def create(ticket_type, data, base_url):
        json_data = {
            'task_type': ticket_type,
            'data': data
        }
        response = requests.post(f'{base_url}/create', json=json_data)
        Task._print(response)
        if response.status_code == HTTPStatus.OK:
            task_id = response.json().get('id')
            if task_id:
                return Task(task_id, base_url)
        return None

    @staticmethod
    def _print(response) -> dict:
        if response.status_code == HTTPStatus.OK:
            print(response.text)
            return response.json()

        if response.status_code == HTTPStatus.NOT_FOUND:
            print("Not found")
        else:
            print(f"Error : {response.text}")
        return {}
