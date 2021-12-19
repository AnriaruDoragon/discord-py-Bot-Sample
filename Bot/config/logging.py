from datetime import datetime

log_file = "Bot/Logs/{0}.log".format(datetime.now().strftime("%m%d%Y-%H%M%S"))
log_encoding = "utf-8"
log_format = "[%(asctime)s] %(levelname)s : %(message)s"
log_dateformat = "%m/%d/%Y %I:%M:%S %p"