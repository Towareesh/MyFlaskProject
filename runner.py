import datetime
import os

from app import app



now = datetime.datetime.now()
log = ['worked: runner.py', f'[{now.strftime("%d-%m-%Y %H:%M")}]']


if __name__ == '__main__':
    
    print(f'\u001b[34m{log[1]}\u001b[0m\u001b[32m {log[0]}\u001b[0m\n')

    # app.debug = True
    app.run(host='0.0.0.0')