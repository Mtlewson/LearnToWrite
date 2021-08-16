import logging
import time

# Configure logging parameters
#log_date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
log_date = time.strftime("%d-%m-%Y-%H_%M_%S", time.localtime())
log_name = "log_" + log_date + ".log"
logging.basicConfig(filename="log_files/"+log_name, filemode="a", format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    level=logging.DEBUG)
