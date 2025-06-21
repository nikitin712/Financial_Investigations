import psycopg2


def connection_DB():
    connection = psycopg2.connect(dbname='Cases_and_persons_involved_in_OFR',
                                  user='postgres',
                                  password='Q1w2e3r4',
                                  host='localhost')
    if connection:
        return connection.cursor(), connection
    else:
        return (False, False)

cursor, connection = connection_DB()






def select():
    print('=' * 100)
    print('''You into select mode. 
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

    cursor.execute(f'''SELECT column_name FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = '{name_of_table}';''')
    names = [i[0] for i in cursor.fetchall()]
    
    cursor.execute(f'SELECT * FROM public."{name_of_table}"')
    d = cursor.fetchall()

    dic = {}
    for i in range(len(names)):
        for j in range(len(d)):
            dic[names[i]] = max(dic.get(names[i], len(names[i])), len(str(d[j][i])))

    for i in names:
        print(i.ljust(dic[i]), end=' | ')

    print('\n' + '-' * 110)

    for i in range(len(d)):
        for j in range(len(d[i])):
            print(str(d[i][j]).ljust(dic[names[j]]), end=' | ')
        print()
    flag = select()
    return flag






def insert():
    print('=' * 100)
    print('''You into select mode. 
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

    decision = input(f'''If you want to insert data in current table enter data in format:
{' '.join(names)}
but your primary key shouldn`t be {current_pk_data}''').split()
    while len(decision) != len(names) or int(decision[0]) in current_pk_data:
        print('incorrect format')
        decision = input()


    return True






def menu():
    while True:
        print('=' * 100)
        print('''You in menu. 
1) enter '1' to find info in DataBase
2) enter '2' to insert data into DataBase
3) enter '3' ...
4) enter '9' to finish work
Enter option:''', end=' ')
        op = input()
        while op not in ['1', '2', '3', '9']:
            print('''Choose only between:
1) enter '1' to find info in DataBase
2) enter '2' to insert data into DataBase
3) enter '3' ...
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
        if flag == True:
            continue
        else:
            break
    return





print('*-' * 50, end='*\n')
print('''Hello! If you want to know more about persons for Financial Research,
look into the instructions before you start. There is numbers to operate with functions:
1) enter '0' to go to menu
2) enter '9' to finish work\n
Now enter '0' to start or '9' to finish:''', end=' ')

operation = input()

while operation != '0' and operation != '9':
    print("enter only '0' to start or '9' to finish:", end=' ')
    operation = input()

if operation == '0':
    menu()
    cursor.close()
    connection.close()
    print('Program is finishing work...3...2...1...')
else:
    cursor.close()
    connection.close()
    print('Program is finishing work...3...2...1...')
