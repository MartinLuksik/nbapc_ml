#!/usr/bin/env python
"""
https://gist.github.com/bradmontgomery/2219997
Very simple HTTP server in python (Updated for Python 3.7)
Usage:
    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000
Send a GET request:
    curl http://localhost:8000
Send a HEAD request:
    curl -I http://localhost:8000
Send a POST request:
    curl -d "foo=bar&bin=baz" http://localhost:8000
"""
import argparse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import pickle
import sklearn
import simplejson
import numpy as np
import json

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><head><title>NBAPC</title></head><body><h1>NBA ML Predict center</h1><p>LeBron James is predicted to score {message} points in the next game.</p></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        # Load from file
        model = os.environ["model"]
        with open(model, 'rb') as file:
            model = pickle.load(file)
        
        # demo values(in production, the data is read from a table)
        points = score([1,35.0,28.0,43.0,37.0,35.0,20.0,23.0,39.0,21.0,30.0,1.0,1.0,0.0,0.0,0.0], model)[0]
        self._set_headers()
        self.wfile.write(self._html(points))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Condent-Type', 'application/json')
        self.end_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        
        # read in the model and make prediction
        data = simplejson.loads(self.data_string)['score']
        data = np.asarray(data)
        with open("knnreg.pkl", 'rb') as file:
            knnreg = pickle.load(file)
        points = score(data, knnreg)[0]

        # Prepare json as response
        jsonstr = json.dumps({'predictedPoints': points})

        self.wfile.write(jsonstr.encode(encoding='utf_8'))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

def score(data, model):
    prediction = model.predict([data])
    return prediction

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)