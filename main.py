import signal
import sys
from website import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)     #set ixt to False when run it in prodaction
