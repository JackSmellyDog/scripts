import functools
import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def execute_webdriver_task(_func=None, *, headless=False):
    def add_params_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            wd = None
            result = None

            try:
                options = Options()
                options.headless = headless
                wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

                result = func(wd, *args, **kwargs)
            except Exception as e:
                print(f'Something went wrong! {e}')
            finally:
                if wd:
                    wd.quit()

            return result

        return inner
    
    if _func is None:
        return add_params_func
    else:
        return add_params_func(_func)


@execute_webdriver_task(headless=True)
def test_func(wd):
    print('It works!')
    wd.get('https://google.com')
    time.sleep(3)

def main():
    test_func()

if __name__ == '__main__':
    main()


