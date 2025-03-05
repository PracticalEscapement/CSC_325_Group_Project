import signal
import sys
from website import create_app


#dfjhbgjdfb
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)     #set it to False when run it in prodaction