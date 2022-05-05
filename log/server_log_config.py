# import sys
# sys.path.append('..')
# import logging
# import logging.handlers as lh
#
# log_server = logging.getLogger('log_server')
#
# format_log_server = logging.Formatter('%(created)f %(levelname)s %(module)s %(message)s %(')
#
# fl_log_server = lh.TimedRotatingFileHandler('log/log_server/log_server.log', when='D', interval=1)
# fl_log_server.setLevel(logging.DEBUG)
# fl_log_server.setFormatter(format_log_server)
#
# console_log_server = logging.StreamHandler()
# console_log_server.setFormatter(format_log_server)
# console_log_server.setLevel(logging.DEBUG)
#
# log_server.addHandler(fl_log_server)
# log_server.addHandler(console_log_server)
# log_server.setLevel(logging.DEBUG)