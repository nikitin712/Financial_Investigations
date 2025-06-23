import psycopg2
import pandas as pd

pd.set_option('display.max_rows', None)  # Выводить все строки
pd.set_option('display.max_columns', None)  # Выводить все столбцы
pd.set_option('display.width', None)  # Автоматически подбирать ширину
pd.set_option('display.max_colwidth', None)  # Показывать полное содержимое ячеек


def connection_db():
    conn = psycopg2.connect(dbname='Cases_and_persons_involved_in_OFR',
                            user='postgres',
                            password='Q1w2e3r4',
                            host='localhost')
    if conn:
        return conn.cursor(), conn
    else:
        return False, False


cursor, connection = connection_db()


def print_data(df, page_size=10):
    if df.empty:
        print("DataFrame пуст")
        return

    current_page = 0
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size

    while True:
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, total_rows)

        print(f"\nPage {current_page + 1}/{total_pages} (rows {start_idx + 1}-{end_idx} из {total_rows})")

        print(df.iloc[start_idx:end_idx].to_string())
        if total_pages == 1:
            return

        print("\nNext action:")
        print("n - next page     p - previous page")
        print("f - first page    l - last page")
        print("r - return        number - go to the page with number")

        action = input("\nEnter: ").lower()

        if action == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif action == 'p' and current_page > 0:
            current_page -= 1
        elif action == 'f':
            current_page = 0
        elif action == 'l':
            current_page = total_pages - 1
        elif action == 'r':
            break
        elif action.isdigit():
            page_num = int(action) - 1
            if 0 <= page_num < total_pages:
                current_page = page_num
            else:
                print(f"Page should be from 1 to {total_pages}")
        else:
            print("Incorrect")







def select():
    while True:
        print('=' * 100)
        print('''You are in select mode. 
Choose name of table between 'Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies',
where you want to find info, enter '0' to return to menu or '9' to finish:''', end=' ')
        name_of_table = input()
        if name_of_table == '0':
            return True
        elif name_of_table == '9':
            return False

        while name_of_table not in ['Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies']:
            print('''Choose only between 'Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies',
enter '0' to return to menu or '9' to finish:''', end=' ')
            name_of_table = input()
            if name_of_table == '0':
                return True
            elif name_of_table == '9':
                return False

        query = f'SELECT * FROM public."{name_of_table}"'
        df = pd.read_sql(query, connection)
        print_data(df)
    # flag = select()
    # return flag


def insert():
    print('=' * 100)
    print('''You are in insert mode. 
Choose name of table between 'Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies',
where you want to insert info, enter '0' to return to menu or '9' to finish:''', end=' ')

    name_of_table = input()
    if name_of_table == '0':
        return True
    elif name_of_table == '9':
        return False

    while name_of_table not in ['Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies']:
        print('''Choose only between 'Cities', 'Persons', 'Accounts', 'Bodies', 'Transactions', 'Cases', 'Cases_Bodies', 
enter '0' to return to menu or '9' to finish:''', end=' ')
        name_of_table = input()
        if name_of_table == '0':
            return True
        elif name_of_table == '9':
            return False

    cursor.execute(f'''SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = '{name_of_table}';''')
    names = [i[0] for i in cursor.fetchall()]

    cursor.execute(f'SELECT * FROM public."{name_of_table}"')
    d = cursor.fetchall()
    print('In selected table names of columns are :', names)

    current_pk_data = [i[0] for i in d]
    list_for_insert = []
    for i in range(len(names)):
        print(f'type {names[i]} for table {name_of_table} in format and type as {d[0][i]}')
        data = input()
        if type(d[0][i]) == int:
            if i == 0:
                # Primary key (integer)
                while data.lower() != data.upper() or any(list(map(lambda x: data == str(x), current_pk_data))):
                    print(f'''Incorrect format. You try to put string into number.
Type number not between {current_pk_data}''')
                    data = input()
            else:
                # integer
                while data.lower() == data.upper():
                    print('Incorrect format. You try to put string into number. Type number')
                    data = input()
            list_for_insert.append(int(data))
        elif '.' in data and '.' in d[0][i]:
            # numeric
            while data.count('.') > 1 or len(set('!?@;:/*|+=-_`~') & set(data)) != 0 \
                    or len(data[data.find('.') + 1:]) > 2:
                print('incorrect format of numeric. Enter in format 000000.00')
                data = input()
            list_for_insert.append(float(data))
        elif ':' in data and d[0][i].count(':') == 2:
            # date
            while data.count(':') != 2 or len(set('!?@;.,/*|+=-_`~') & set(data)) != 0 or len(data.split(':')[0]) != 4 \
                    or len(data.split(':')[1]) != 2 or len(data.split(':')[2]) != 2:
                print('incorrect date. Enter in format "YYYY-MM-DD"')
                data = input()
            list_for_insert.append(data)
        else:
            if ':' in d[0][i] and ':' not in data or '.' not in data and '.' in d[0][i]:
                print('Unknown data. return to menu...')
                return False
            else:
                list_for_insert.append(data)

    print(tuple(list_for_insert))
    cursor.execute(f'''INSERT INTO public."{name_of_table}" VALUES
{tuple(list_for_insert)};''')
    connection.commit()

    print('\nSuccessful insert. Return to menu')
    return True


def search_by_name():
    print('=' * 100)
    print('''You are in search mode. 
Enter name of private person in format 'Last_name First_name Second_name' 
or name of professional body in format 'name_of_body' to find info about. 
If you want to finish enter '0' to return to menu or '9' to finish:''', end=' ')

    action = input()
    if action == '0':
        return True
    elif action == '9':
        return False

    while len(action.rstrip().split()) != 3 and len(action.rstrip().split()) != 1:
        print('''Incorrect format... 
Enter name of private person in format 'Last_name First_name Second_name' 
or name of professional body in format 'name_of_body' to find info about. 
If you want to finish enter '0' to return to menu or '9' to finish:''', end=' ')
        action = input()
        if action == '0':
            return True
        elif action == '9':
            return False

    if len(action.split()) == 3:
        query = f'''SELECT person_id, last_name, first_name, second_name, birthday, city_name
                            FROM public."Persons" as p
                            INNER JOIN public."Cities" as c ON p.city_id = c.city_id
                            WHERE p.last_name = '{action.split()[0]}' and p.first_name = '{action.split()[1]}'
                                    and p.second_name = '{action.split()[2]}';'''
        df = pd.read_sql(query, connection)

        if len(df) != 0:
            print(f'Here all info about {action}:')
            print_data(df)

            print(f'\nLook professional bodies, that {action} has or had:')
            print(" 'fiz' - private person\n 'ENT' - entepreneur\n 'OOO' - otkritoe akcionernoe obshestvo\n 'GUP' - government unitarnoe predpriyatie\n")
            query = f'''SELECT body_type, body_name, start_date, end_date, b."INN" as b_INN 
                FROM public."Persons" as p
                INNER JOIN public."Bodies" as b ON p.person_id = b."CEO_id_or_person_id"
                WHERE p.last_name = '{action.split()[0]}' and p.first_name = '{action.split()[1]}'
                                    and p.second_name = '{action.split()[2]}';'''
            df = pd.read_sql(query, connection)
            if len(df) != 0:
                print_data(df)
            else:
                print('No bodies')

        else:
            print('No info about person')
    else:
        print(" 'fiz' - private person\n 'ENT' - entepreneur\n 'OOO' - otkritoe akcionernoe obshestvo\n 'GUP' - government unitarnoe predpriyatie")
        query = f'''SELECT body_type, body_name, b."INN" as body_INN, start_date, 
        end_date, p.last_name, p.first_name, p.second_name, p.birthday
        FROM public."Persons" p 
        INNER JOIN public."Bodies" b ON p.person_id = b."CEO_id_or_person_id"
        WHERE body_name = '{action}';'''
        df = pd.read_sql(query, connection)
        print_data(df)

        print(f'\nAccounts of {action}:')
        query = f'''SELECT account_id, account_number, body_name, a.open_date, a.close_date, p.last_name, p.first_name, p.second_name
                    FROM public."Accounts" a 
                    INNER JOIN public."Bodies" b ON a.body_id = b.body_id
                    INNER JOIN public."Persons" p ON b."CEO_id_or_person_id" = p.person_id
                    WHERE body_name = '{action}';'''
        df = pd.read_sql(query, connection)
        print_data(df)

    return True


def menu():
    while True:
        print('=' * 100)
        print('''You are in menu. 
1) enter '1' to find info in DataBase
2) enter '2' to insert data into DataBase
3) enter '3' to find info about private person or professional body
4) enter '9' to finish work
Enter option:''', end=' ')
        op = input()
        while op not in ['1', '2', '3', '9']:
            print('''Choose only between:
1) enter '1' to find info in DataBase
2) enter '2' to insert data into DataBase
3) enter '3' to find info about private person or professional body
4) enter '9' to finish work
Enter option:''', end=' ')
            op = input()
        flag = False
        if op == '9':
            break
        else:
            if op == '1':
                flag = select()
            elif op == '2':
                flag = insert()
            elif op == '3':
                flag = search_by_name()
        if flag:
            continue
        else:
            break
    return
