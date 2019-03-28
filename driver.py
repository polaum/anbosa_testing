import logging
import os
import time
from multiprocessing import Process

from appium import webdriver
import requests
from requests.exceptions import ConnectionError

from common import TimeLimit, Retry
from common.config import APPIUM_PORT


class AndroidAppium(webdriver.Remote):
    def __init__(self, app_path, **kwargs):
        if 'desired_capabilities' not in kwargs:
            kwargs['desired_capabilities'] = {}
        kwargs['desired_capabilities'].update({
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'app': app_path,
            'newCommandTimeout': 0
        })
        if 'command_executor' not in kwargs:
            _command_executor = f'http://localhost:{APPIUM_PORT}/wd/hub'
            try:
                assert requests.get(_command_executor + '/status').ok
                logging.info('successfully communicated with appium instance running on port %s', APPIUM_PORT)
            except (ConnectionError, AssertionError):
                logging.info('failed to find an appium instance, starting one')
                p = Process(target=os.system, args=(f'appium -p {APPIUM_PORT} --log-level=warn',))
                p.start()
                Retry().this(lambda: requests.get(_command_executor + '/status').raise_for_status())
            kwargs['command_executor'] = f'http://localhost:{APPIUM_PORT}/wd/hub'
        super().__init__(**kwargs)
