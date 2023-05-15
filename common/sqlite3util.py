import functools
import sqlite3


def transactional(_func=None, *, db='file::memory:?cache=shared', readonly=False):
    def add_params_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = None
            connection = sqlite3.connect(db)

            try:
                cur = connection.cursor()
                result = func(cur, *args, **kwargs)

                if not readonly:
                    connection.commit()
            except Exception as e:
                if not readonly:
                    connection.rollback()
                print(f'Something went wrong! {e}')
            finally:
                if connection:
                    connection.close()

            return result

        return inner

    if _func is None:
        return add_params_func
    else:
        return add_params_func(_func)
