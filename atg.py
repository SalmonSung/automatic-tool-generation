import os
import config

if __name__ == "__main__":
    if not os.path.exists(config.APP_PATH_RESULT):
        os.makedirs(config.APP_PATH_RESULT)
    if not os.path.exists(config.APP_PATH_DATASET):
        os.makedirs(config.APP_PATH_DATASET)
