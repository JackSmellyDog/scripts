import string
import random
import datetime
import sqlite3
import argparse
import functools

DEFAULT_NUMBER_LENGTH = 11
DEFAULT_PREFIXES_FILENAME = 'valid_prefixes.csv'

DB_FILENAME = 'used-numbers.db'

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS used_numbers (
        number       TEXT PRIMARY KEY,
        created_date DATE
    );
"""


def read_prefixes(filename: str = DEFAULT_PREFIXES_FILENAME, separator=';', operator=None):
    prefix_to_operator_list = []
    with open(filename, 'r') as f:
        prefix_to_operator_list = [line.rstrip().split(separator) for line in f.readlines()]

    if operator:
        return [prefix_to_operator[0] for prefix_to_operator in list(filter(lambda po: po[1] == operator, prefix_to_operator_list))]

    return [prefix_to_operator[0] for prefix_to_operator in prefix_to_operator_list]


def pick_random_prefix(prefixes: list):
    return random.choice(prefixes)


def generate_number(prefix: str, length: int = DEFAULT_NUMBER_LENGTH):
    suffix_length = length - len(prefix)
    suffix = ''.join(random.choices(string.digits, k=suffix_length))

    return f'{prefix}{suffix}'


def now(format: str):
    return datetime.datetime.today().strftime(format)


def transactional(_func=None, *, readonly=False):
    def add_params_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = None
            connection = sqlite3.connect(DB_FILENAME)

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


@transactional(readonly=True)
def generate_numbers(cur, amount: int, prefixes: list):
    result = set()

    while len(result) < amount:
        random_prefix = pick_random_prefix(prefixes)
        number = generate_number(random_prefix)

        is_present = cur.execute(
            'SELECT EXISTS(SELECT 1 FROM used_numbers WHERE number = ?)', (number,)).fetchone()[0]

        if not is_present:
            result.add(number)

    return result


@transactional
def save_numbers_db(cur, numbers: set):
    today = now('%d.%m.%Y %H:%M:%S')
    numbers_with_creation_date = list(map(lambda number: (number, today), numbers))

    cur.executemany(
        'INSERT INTO used_numbers (number, created_date) VALUES (?, ?)', numbers_with_creation_date)


@transactional
def create_table_if_absent(cur):
    cur.execute(CREATE_TABLE_QUERY)


def save_numbers_file(numbers):
    saving_date_time = now('%d-%m-%Y-%H-%M-%S')

    with open(f'{saving_date_time}-{len(numbers)}.txt', 'w') as f:
        f.write('\n'.join(numbers))


def read_console_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--Amount', help='Amount of uniqe numbers to generate')
    parser.add_argument('-o', '--Operator', help='Operator id')

    args = parser.parse_args()

    return int(args.Amount), args.Operator


def main():
    amount, operator = read_console_args()

    create_table_if_absent()
    numbers = generate_numbers(amount=amount, prefixes=read_prefixes(operator=operator))
    save_numbers_db(numbers=numbers)
    save_numbers_file(numbers=numbers)


if __name__ == '__main__':
    main()
