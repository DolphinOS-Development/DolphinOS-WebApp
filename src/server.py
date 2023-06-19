import scripts
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/poweroff/')
def poweroff():
  print ('Shutting down System!')

  return scripts.poweroff()

@app.route('/reboot/')
def reboot():
  print ('Rebooting System!')

  return scripts.reboot()

if __name__ == '__main__':
  app.run(debug=True)
