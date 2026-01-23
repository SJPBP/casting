from Formatter import Formatter
from FileHandler import FileHandler
import logging

class Logger:
    def __init__(self, logging_name, caller, logging_level="debug"):
        """
        Parameters

        logging_name: Always use __name__ 
        caller: Always use __file__ 
        logging_level: The level of logs to capture, levels are debug, info, warning, error, critcal
        """
        # Create logging for the Logger file
        self_logging_level = logging.DEBUG
        self_logging_name = __name__
        self_filename = "Logger"

        self.logger = self._get_logging(logging_level=self_logging_level, 
                                       logging_name=self_logging_name, 
                                       filename=self_filename)

        self.logger.info("Created logging for Logger")


        self.logging_name = logging_name
        self.filename = self._get_filename(caller)
        self.logging_level = logging_level
        

    def get_logger(self):
        # Get logging data from caller
        logging_level = self._get_in_logging_level_value(self.logging_level)
        logging_name = self.logging_name
        filename = self.filename

        self.logger.info(f"Creating logging for {filename}")

        logger = self._get_logging(logging_level=logging_level,
                                  logging_name=logging_name,
                                  filename=filename)

        self.logger.info(f"Created logging for {filename}")

        return logger

    def _get_in_logging_level_value(self, logging_level):
        """
        Takes string and change it into it's logging value e.g. info becomes logging.INFO

        Parameter:
        logging_level: string with different logging levels
        """
        match logging_level:
            case "info":
                logging_level = logging.INFO
            case "debug": 
                logging_level = logging.DEBUG
        return logging_level
    
    def _get_logging(self, logging_name, logging_level, filename):
        logger = logging.getLogger(logging_name)

        logger.setLevel(logging_level)
        
        formatter = Formatter(logging).get_formatter()

        # Create log file  
        file_handler: FileHandler = FileHandler(logging=logging, filename=filename)       

        # Change format of log 
        file_handler.setFormatter(formatter)
        
        # # Handler to output to terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Adding handlers to logger
        logger.addHandler(file_handler.get_handler())
        logger.addHandler(stream_handler)
        
        return logger

    def _get_filename(self, caller: str):
        # Get the filename with file extension
        caller = caller.split("/")[-1]

        # Remove the extension
        caller = caller.split(".")[0]
        return caller

