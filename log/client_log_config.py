import sys
sys.path.append('..')
import logging

log_client = logging.getLogger('log_client')

format_log_client = logging.Formatter('%(created)f %(levelname)s %(module)s %(message)s')

fl_log_client = logging.FileHandler('log/log_client/log_client.log', encoding='utf-8')
fl_log_client.setLevel(logging.DEBUG)
fl_log_client.setFormatter(format_log_client)

console_log_client = logging.StreamHandler()
console_log_client.setFormatter(format_log_client)
console_log_client.setLevel(logging.DEBUG)


log_client.addHandler(fl_log_client)
log_client.addHandler(console_log_client)
log_client.setLevel(logging.DEBUG)