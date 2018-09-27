import os
import time
import cv2
import argparse

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import mimetypes as memetypes
import shutil
import cgi
import random
import string
import json

import openface

BASE62_CHARSET=string.ascii_lowercase + string.digits + string.ascii_uppercase

openFaceModelDir = os.path.join('/root/openface', 'models')
dlibModelDir = os.path.join(openFaceModelDir, 'dlib')
openfaceModelDir = os.path.join(openFaceModelDir, 'openface')

fileDir = os.path.dirname(os.path.realpath(__file__))
tmpDir = os.path.join(fileDir, '..', 'tmp')

parser = argparse.ArgumentParser()

parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)

args = parser.parse_args()
align = openface.AlignDlib(args.dlibFacePredictor)

def rand_string(n=8, charset=BASE62_CHARSET):
    res = ""
    for i in range(n):
        res += random.choice(charset)
    return res

class S(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self._set_headers()

    def send_headers(self):
        npath = os.path.normpath(self.path)
        npath = npath[1:]
        path_elements = npath.split('/')

        if path_elements[0] == "f":
            reqfile = path_elements[1]

            if not os.path.isfile(reqfile) or not os.access(reqfile, os.R_OK):
                self.send_error(404, "file not found")
                return None

            content, encoding = memetypes.MimeTypes().guess_type(reqfile)
            if content is None:
                content = "application/octet-stream"

            info = os.stat(reqfile)

            self.send_response(200)
            self.send_header("Content-Type", content)
            self.send_header("Content-Encoding", encoding)
            self.send_header("Content-Length", info.st_size)
            self.end_headers()

        elif path_elements[0] == "upload":
            self.send_response(200)
            self.send_header("Content-Type", "text/json; charset=utf-8")
            self.end_headers()

        else:
            self.send_error(404, "fuck")
            return None

        return path_elements

    def do_GET(self):
        elements = self.send_headers()
        if elements is None:
            return

        reqfile = elements[1]
        f = open(reqfile, 'rb')
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def do_POST(self):
        elements = self.send_headers()
        if elements is None or elements[0] != "upload":
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE":   self.headers['Content-Type']
            })

        _, ext = os.path.splitext(form["file"].filename)

        fname = os.path.join(tmpDir, rand_string() + ext)
        while os.path.isfile(fname):
            fname = os.path.join(tmpDir, rand_string() + ext)

        fdst = open(fname, "wb")
        shutil.copyfileobj(form["file"].file, fdst)
        fdst.close()

        ########### openface
        bgrImg = cv2.imread(fname)
        if bgrImg is None:
            raise Exception("Unable to load image: {}".format(fname))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        print("  + Original size: {}".format(rgbImg.shape))

        start = time.time()
        bb = align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            raise Exception("Unable to find a face: {}".format(imgPath))
        print("  + Face detection took {} seconds.".format(time.time() - start))

        start = time.time()
        alignedFace = align.align(args.imgDim, rgbImg, bb,
                                  landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))
        print("  + Face alignment took {} seconds.".format(time.time() - start))

        # TODO: Extract features from alignedFace
        net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
        
        # TODO: Apply sklearn model

        ############

        result = {
            "data": { "url": "/f/" + fname },
            "success": True,
            "status": 200,
        }

        self.wfile.write(json.dumps(result))

def run(server_class=HTTPServer, handler_class=S, port=80):
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

run(port=8000)
