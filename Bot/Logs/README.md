# Logging guide
`Bot/config/logging.py` - Logging config
```py
# Log to the file
log_enable = True
_log_const = False

# Logging File Place & Name
if _log_const:
    log_file = "Bot/Logs/Client.log"
else:
    from datetime import datetime
    log_file = "Bot/Logs/{0}.log".format(datetime.now().strftime("%m%d%Y-%H%M%S"))

# Log file mode (w - rewrite, a - append)
log_mode = "w"

# Logging File Encoding
log_encoding = "utf-8"

# Logging Records Format
log_format = "[%(asctime)s] %(levelname)s : %(message)s"

# Logging Date Format for Records
log_dateformat = "%m/%d/%Y %I:%M:%S %p"
```

## F.A.Q.
- **Q: I don't want to save log files.**
  - A: Change `True` in `log_enable` to `False`.
- **Q: I want to save logs in a single file.**
  - A: Change `False` in `_log_const` to `True`.
- **Q: Old log file overwrites when I launch the bot again. I want to keep my logs for all sessions in a single file.**
  - A: If you followed the previous method - change `log_mode` from `w` to `a`.
