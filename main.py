from flask import Flask, render_template, Response, flash, send_file
from camera import VideoCamera
from op import OP
import cv2
from livereload import Server


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
myop = OP()

warn_path = "templates/warning.jpg"
clear_path = "templates/ok.jpg"

@app.route('/')
def index():
    return render_template('index.html', phone=False)


def gen(camera):
    while True:
        # with app.app_context():
        #     if True:
        #         render_template('index.html', phone=True)
        #     else:
        #         render_template('index.html', phone=False)
        frame = camera.get_frame(myop)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_warning():
    while True:
        with app.app_context():
            yield send_file(clear_path, mimetype='image/jpg')
        # if myop.phone_detected:
        #     yield send_file(warn_path, mimetype='image/jpg')
        # else:
        #     yield send_file(clear_path, mimetype='image/jpg')


@app.route('/warning_feed')
def warning_feed():
    return Response(gen_warning(), mimetype='image/jpg')
    # return send_file(clear_path, mimetype='image/jpg')
    # print("hoora")
#     return "hello"


if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve()
    app.run()
