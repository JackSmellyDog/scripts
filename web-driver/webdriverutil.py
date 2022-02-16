import functools
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def _start_local_webdriver():
    pass


def execute_webdriver_task(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # do before
        web_driver_path = './chromedriver'

        wd = webdriver.Chrome(web_driver_path)

        wd.get('https://github.com/JackSmellyDog/coins-clicker/blob/master/clicker.py')
        time.sleep(5)

        val = func(wd, *args, **kwargs)

        wd.quit()

        # do after

        return val

    return inner

@execute_webdriver_task
def test_func(wd):
    print('It works!')
    wd.get('https://google.com')

def main():
    test_func()

if __name__ == '__main__':
    main()

