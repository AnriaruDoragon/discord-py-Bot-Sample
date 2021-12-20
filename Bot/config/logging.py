from datetime import datetime

# Logging File Place & Name
log_file = "Bot/Logs/{0}.log".format(datetime.now().strftime("%m%d%Y-%H%M%S"))

# Logging File Encoding
log_encoding = "utf-8"

# Logging Records Format
log_format = "[%(asctime)s] %(levelname)s : %(message)s"

# Logging Date Format for Records
log_dateformat = "%m/%d/%Y %I:%M:%S %p"
