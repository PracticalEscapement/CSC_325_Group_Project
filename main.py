import signal
import sys
from website import create_app



app = create_app()

# comment


if __name__ == '__main__':
    app.run(debug=True)     #set it to False when run it in prodaction
