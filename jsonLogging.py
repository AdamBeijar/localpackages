import json
import sys
import time

defaultConfig = {
    "logFile": "log.json",
    "logLevel": "INFO",
    "stringFormat": """ {time} {level}}
        {message} \n""",
    "dateFormat": "%Y-%m-%d %H:%M:%S",
}


class logging:
    def __init__(self, config=defaultConfig):
        """Initialize the logging class, pass a config dictionary that looks like this
        {
            "logFile": xxxx.xxx,
            "logLevel": XXXX,
            "stringFormat": {time} {level} {message}
            "dateFormat": XXXXXXXXXXXXX
        }
        """
        self.config = config
        self.log_setup(config)

    def log_setup(self, config):
        """Setup logging, you need to pass the config file to this function containing
        file location and log level"""
        if config["logFile"]:
            self.fileName = config["logFile"]
        else:
            self.fileName = defaultConfig["logFile"]
        if self.fileName == "stdout":
            self.logFile = sys.stdout
            self.json = False
        # if logFile ends with .json, then we will log in json format
        elif self.fileName.endswith(".json"):
            self.logFile = open(self.fileName, "a")
            self.json = True
        elif self.fileName == "":
            self.logFile = open("bot.log", "a")
            self.json = False
        elif self.fileName == "none":
            self.logFile = None
            self.json = False
        else:
            self.logFile = open(self.fileName, "a")
            self.json = False
        if config["stringFormat"]:
            self.stringFormat = config["stringFormat"]
        else:
            self.stringFormat = defaultConfig["stringFormat"]

        if config["dateFormat"]:
            self.dateFormat = config["dateFormat"]
        else:
            self.dateFormat = defaultConfig["dateFormat"]
        self.logLevels = {
            "debug": 0,
            "info": 1,
            "warning": 2,
            "error": 3,
            "critical": 4,
        }
        if config["logLevel"]:
            self.logLevel = self.logLevels[config["logLevel"].lower()]
        else:
            self.logLevel = self.logLevels[defaultConfig["logLevel"].lower()]

    def log(self, message=None, level="info", line=None):
        """msg is a dictionary containing the following keys:
        level: debug, info, warning, error, critical
        message: the message to log
        time: the time the message was logged
        you may either put logLevel as an int or level as a string if you dont put a level it will be set to info
        """
        if type(level) == int:
            logLevel = level
            level = list(self.logLevels.keys())[
                list(self.logLevels.values()).index(int(level))
            ]
        else:
            logLevel = self.logLevels[level.lower()]
        if not message:
            level = "error"
            message = "No message passed to log function"
        msg = {
            "levelName": str(level),
            "logLevel": int(logLevel),
            "message": str(message),
            "time": time.strftime(self.config["dateFormat"], time.localtime()),
        }
        if line:
            msg["line"] = line
        if self.logFile is not None:
            if msg["logLevel"] >= self.logLevel:
                if msg["logLevel"] >= 3:
                    output_str, output_json = self.createErrorLog(msg)
                else:
                    output_str, output_json = self.createLog(msg)
                if self.json:
                    # write json to a file and put a comma on the last one before you added and put the new one on a new line
                    self.logFile.write(",\n" + json.dumps(output_json))
                    print(output_str)
                else:
                    if self.logFile == sys.stdout:
                        self.logFile.write(str(output_str))
                    else:
                        self.logFile.write(str(output_str))
                        print(output_str)

    def createLog(self, msg):
        json_message = {
            "level": msg["logLevel"],
            "levelName": msg["levelName"],
            "message": msg["message"],
            "timestamp": time.strftime(self.config["dateFormat"], time.localtime()),
        }
        str_message = self.config["stringFormat"].format(
            time=msg["time"], level=msg["levelName"], message=msg["message"]
        )
        return str_message, json_message

    def createErrorLog(self, msg):
        json_message = {
            "level": msg["logLevel"],
            "levelName": msg["levelName"],
            "message": msg["message"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }
        str_message = self.config["stringFormat"].format(
            time=msg["time"], level=msg["levelName"], message=msg["message"]
        )
        return str_message, json_message
