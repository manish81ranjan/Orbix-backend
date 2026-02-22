# """
# Request logging middleware
# - Logs method, path, status, duration
# - Helpful for debugging & Render logs
# """

# import time
# from flask import request


# def register_logging(app):
#     @app.before_request
#     def start_timer():
#         request._start_time = time.time()

#     @app.after_request
#     def log_request(response):
#         duration = time.time() - getattr(request, "_start_time", time.time())
#         app.logger.info(
#             "%s %s %s %.2fms",
#             request.method,
#             request.path,
#             response.status_code,
#             duration * 1000
#         )
#         return response
import time
from flask import request

def register_logging(app):
    @app.before_request
    def _start_timer():
        request._start_time = time.time()

    @app.after_request
    def _log(resp):
        try:
            ms = int((time.time() - request._start_time) * 1000)
        except Exception:
            ms = -1
        app.logger.info("%s %s -> %s (%sms)", request.method, request.path, resp.status_code, ms)
        return resp
