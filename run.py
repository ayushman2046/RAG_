
import os
from app import create_app

app = create_app(os.getenv("ENV") or "dev")

if __name__ == '__main__':
    # the changes are mine, infact the whole project is mine
    app.run(host="0.0.0.0", port=5000, debug = True)