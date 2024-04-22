from app.app_init import app
from app.routes.service import api

app.register_blueprint(api)

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)