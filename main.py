from functions import *

try:
    while True:
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
            print('Finish work in...3...2...1...')
        else:
            cursor.close()
            connection.close()
            print('Finish work in...3...2...1...')
        break

except KeyboardInterrupt:
    print("\nПрограмма завершается по запросу пользователя")
    cursor.close()
    connection.close()
    print('Finish work in...3...2...1...')
