#!/usr/bin/env python
import tornado.ioloop
import tornado.web
from asyncdynamo import asyncdynamo
from tornado import gen
from tornado.web import asynchronous


DB = None


def db():
    global DB
    if DB is not None:
        return DB

    DB = asyncdynamo.AsyncDynamoDB(aws_access_key_id='your_aws_access_key_id',
                                                 aws_secret_access_key='your_aws_secret_access_key',
                                                 endpoint='http://localhost:8000')
    return DB


@gen.coroutine
def create_table(callback):
    json_open = open('create_table.json')
    db().make_request(action='CreateTable', body=json_open.read(), callback=callback)


@gen.coroutine
def put_items(callback):
    json_open = open('put_items.json')
    db().make_request(action='PutItem', body=json_open.read(), callback=callback)


@gen.coroutine
def get_items(callback):
    json_open = open('get_items.json')
    db().make_request(action='GetItem', body=json_open.read(), callback=callback)


class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    def post(self):
        create_table(self.callback)

    def callback(self, res, error=None):
        if error is not None:
            self.finish({"error": error})
        self.finish({"data": res})

    @asynchronous
    def put(self):
        put_items(self.callback)

    @asynchronous
    def get(self):
        get_items(self.callback)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
