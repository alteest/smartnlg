import argparse

from task import Task


class Client:

    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.post = port
        self.base_url = f'http://{self.host}:{self.post}'

    def create(self, ticket_type: str, data: str, batch: bool = False):
        task = Task.create(ticket_type, data, self.base_url)
        if batch and task:
            task.wait()

    def status(self, task_id: str) -> None:
        Task(task_id, self.base_url).get_status()

    def result(self, task_id: str) -> None:
        Task(task_id, self.base_url).get_result()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Client')
    parser.add_argument('-c', help="Create Taks", action="store",
                        nargs=2, dest='create')
    parser.add_argument('-s', help="Get task status", action="store",
                        dest='status', default='')
    parser.add_argument('-r', help="Get task result", action="store",
                        dest='result', default='')
    parser.add_argument('-b', help="Use batch mode for task creation",
                        action="store_true",
                        dest='batch', default=False)

    result = parser.parse_args()

    client = Client()
    if result.create:
        client.create(*result.create, result.batch)
    elif result.status:
        client.status(result.status)
    elif result.result:
        client.result(result.result)
