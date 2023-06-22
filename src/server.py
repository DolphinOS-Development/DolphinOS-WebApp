import scripts
from flask import Flask, render_template, request, redirect, url_for
import nmcli


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/poweroff')
def poweroff():
  print ('Shutting down System!')
  return scripts.poweroff()

@app.route('/reboot')
def reboot():
  print ('Rebooting System!')
  return scripts.reboot()

@app.route('/wifi')
def wifi_settings():
  info = nmcli.device.show_all()
  connection_info = None
  for connection in info:
    if connection.get('GENERAL.DEVICE') == 'wlo1':
        connection_info = connection
        break
  
  conn_name = None
  ip_address = None
  if connection_info != None:
    if connection_info.get('GENERAL.STATE') == '100 (connected)':
      conn_name = connection_info.get('GENERAL.CONNECTION')
      ip_address = connection_info.get('IP4.ADDRESS[1]')

  networks = nmcli.device.wifi()
  return render_template('wifi_settings.html', networks=networks, conn_name=conn_name, ip_address=ip_address)

@app.route('/connect', methods=['POST'])
def connect():
  try:
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    nmcli.device.wifi_connect(ssid, password)
    connection_info = nmcli.connection.show(ssid)
    ip_address = connection_info.get('IP4.ADDRESS[1]')
    return redirect(url_for('success', ssid=ssid, ip_address=ip_address))
  except Exception as e:
    print(f'Error: {str(e)}')
    return redirect(url_for('failure'))

@app.route('/success')
def success():
  ssid = request.args.get('ssid')
  ip_address = request.args.get('ip_address')
  return render_template('success.html', ssid=ssid, ip_address=ip_address)

@app.route('/failure')
def failure():
  return render_template('failure.html')

@app.route('/open_dolphin')
def open_dolphin():
  print ('Opening dolphin!')
  scripts.end_dolphin()
  return scripts.open_and_run_dolphin()

if __name__ == '__main__':
  app.run(debug=True)
