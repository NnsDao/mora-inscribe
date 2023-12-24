#!/usr/bin/env python

import os
# import sys
import environ
from pathlib import Path



def loadEnvFile():
    base_dir = Path(__file__).resolve().parent
    env_name = os.getenv("ENV_CONFIG_NAME",'') or ''
    if env_name :
        env_path = "{}/envs/{}.{}".format(base_dir , '.env',env_name)
    else:
        env_path = "{}/{}".format(base_dir , '.env')

    if os.path.exists(env_path) :
        environ.Env.read_env(env_path )
