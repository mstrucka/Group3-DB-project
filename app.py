from dotenv import load_dotenv
load_dotenv()

import server

import logging
logging.basicConfig(
    level=logging.DEBUG, 
    filename='app.log', 
    filemode='a+', 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
)

if __name__ == '__main__':
    server.start_server()

