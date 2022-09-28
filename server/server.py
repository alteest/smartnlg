import sys
import logging
import threading

from aiohttp import web

from task import processor


routes = web.RouteTableDef()


@routes.post('/create')
async def task_create(request):
    jdata = await request.json()
    task = processor.add(jdata.get('task_type', ''), jdata.get('data', ''))
    return web.json_response({'id': task.id})


@routes.get('/status/{task_id}')
async def task_status(request):
    task = processor.get(request.match_info['task_id'])
    if task:
        return web.json_response({'status': task.status})
    raise web.HTTPNotFound()


@routes.get('/result/{task_id}')
async def task_result(request):
    task = processor.get(request.match_info['task_id'])
    if task:
        return web.json_response({'result': task.result})
    raise web.HTTPNotFound()


class Server:

    def start(self):

        # To init repository and load actions
        from action import repository

        threading.Thread(target=processor.run, daemon=True).start()

        app = web.Application()
        app.router.add_routes(routes)
        web.run_app(app)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s [%(levelname)s] - '
            '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s'
        ),
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    Server().start()
