from app import create_app, socketio
import requests


app = create_app()


if __name__ == "__main__":
    socketio.run(app, debug=True)
    ip = requests.get('https://api.ipify.org').text
    print(f"Din publika IP-adress är: {ip}")