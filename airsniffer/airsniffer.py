import sensorManager
from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return app.send_static_file("dashboard.html")

@app.route('/air-quality-get')
def aqget():
    return sensorManager.getAirQuality()

@app.route('/history-get')
def hsget():
    return sensorManager.getHistory()
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
