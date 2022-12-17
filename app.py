from flaskr import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig

app = create_app()

if __name__ == '__main__':
   app.run(port=8000)
