# Logging to the file
log_enable = True

# Logging to a single file
_log_const = False

# Logging File Place & Name
if _log_const:
    log_file = "Bot/Logs/Client.log"
else:
    from datetime import datetime
    log_file = "Bot/Logs/{0}.log".format(datetime.now().strftime("%m%d%Y-%H%M%S"))

# Logging file mode (w - rewrite, a - append)
log_mode = "w"

# Logging File Encoding
log_encoding = "utf-8"

# Logging Records Format
log_format = "[%(asctime)s] %(levelname)s : %(message)s"

# Logging Date Format for Records
log_dateformat = "%m/%d/%Y %I:%M:%S %p"
