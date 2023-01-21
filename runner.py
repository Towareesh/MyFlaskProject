import datetime
import os

from app import app


def view_reload_time():
    server_gmt_time  = datetime.datetime.now()
    view_reload_time = ['Worked: runner.py', f'[{server_gmt_time.strftime("%d-%m-%Y %H:%M")}]']

    colors_set = {'blue' : '[34m',
                  'green': '[32m'}

    paint_text = lambda text, color: f'\u001b{colors_set.get(color)}{text}\u001b[0m'

    template_view = '{0} {1}'.format(paint_text(view_reload_time[0], 'blue'),
                                     paint_text(view_reload_time[1], 'green'))
    return template_view



if __name__ == '__main__':
    
    print(view_reload_time())
    
    app.debug = True
    app.run(host='0.0.0.0')