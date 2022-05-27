#import sys

class WifuxLogger:
    @staticmethod
    def warning(msg):
        message= "\033[93mWARNING:"+str(msg)+"\033[0m"
        return message
    @staticmethod
    def error(msg):
        #sys.print_exception(msg)
        message = "\033[91mERROR:"+str(msg)+"\033[0m"
        return message
    @staticmethod
    def info(msg):
        message = "\033[94mINFO:"+str(msg)+"\033[0m"
        return message
    @staticmethod
    def debug(msg):
        message = "\033[92mDEBUG:"+str(msg)+"\033[0m"
        return message
