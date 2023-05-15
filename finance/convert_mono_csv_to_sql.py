import argparse
import csv
import os


def main():
    sql_file_path = 'result.sql'
    folder, card_type = read_console_args()
    convert_csv_files_to_sql(folder, card_type, sql_file_path)


def read_console_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='A path to a directory with CSV files')
    parser.add_argument('-c', '--card', help='Card Type')

    args = parser.parse_args()

    return args.dir, args.card


def convert_date_format(date_string):
    date_parts = date_string.split(' ')
    date_part = date_parts[0].split('.')
    time_part = date_parts[1]

    day = date_part[0].zfill(2)
    month = date_part[1].zfill(2)
    year = date_part[2]

    converted_date = f"{year}-{month}-{day} {time_part}"
    return converted_date


def generate_insert(row, card_type):
    date_time = convert_date_format(row[0])
    exchange_rate = row[6] if row[6] != '—' else 'NULL'
    commission = row[7] if row[7] != '—' else 'NULL'
    cashback_amount = row[8] if row[8] != '—' else 'NULL'
    details = row[1].replace("'", "''")

    return f"""INSERT INTO mono_transactions ("date_time", "details", mcc, "card_currency_amount", "operation_amount",\
    currency, exchange_rate, "commission", "cashback_amount", "balance", card_type)
    VALUES ('{date_time}', '{details}', '{row[2]}',{row[3]}, {row[4]},\
     '{row[5]}', {exchange_rate}, {commission}, {cashback_amount}, {row[9]}, '{card_type}');
    """


def convert_csv_files_to_sql(folder_path, card_type, sql_file):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for row in csv_reader:
                    insert_statement = generate_insert(row, card_type)
                    with open(sql_file, 'a') as f:
                        f.write(insert_statement + '\n')


if __name__ == '__main__':
    main()
