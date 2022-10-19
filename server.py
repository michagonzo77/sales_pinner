from flask_app import app
from flask_app.controllers import users_controller, businesses_controller
import os
print( os.environ.get("FLASK_APP_API_KEY") )


if __name__=="__main__":
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0") 