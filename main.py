import signal
import sys
from website import create_app
from website.models import User
from website.models import *



app = create_app()
app.config['SECRET_KEY']='6b6466ab36b643cd8185b7e283ac5007'

if __name__ == '__main__':
    with app.app_context():
        print(get_all_users())
    app.run(debug=True)

    