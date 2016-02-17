from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
import os
import subprocess
import json
import requests
import random
import urllib2

# App Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

sys_password = os.environ.get('SYS_PASSWORD')
hello_msgs = ['hi', 'hey', 'yup', 'yes', 'hello', 'yes boss']

cors = CORS(app, resources={r"/": {"origins": "localhost"}})

@app.route("/", methods=['POST'])
def process_cmd():
  
  if request.method == 'POST':
    
    # Get the command.
    get_cmd = request.get_data()
    
    cmd = json.loads(get_cmd)['cmd'].strip()
    print cmd
    
    cmd_split = cmd.split(' ')
    print cmd_split

    
    def ask_google(cmd):
      os.system('say -v samantha "Asking Google"')

      search_string = urllib2.quote(cmd)
      os.system('open "http://google.com/search?q=' + search_string + '"')

    
    if (cmd_split[0] == 'heera') or (cmd_split[0] == 'veera')\
      or (cmd_split[0] == 'error') or (cmd_split[0] == 'ara')\
      or (cmd_split[0] == 'aura') or (cmd_split[0] == 'horror')\
      or (cmd_split[0] == 'arav') or (cmd_split[0] == 'aarav')\
      or (cmd_split[0] == 'tera'):
      # Call its name

      os.system('say -v samantha "' + random.choice(hello_msgs) + '"')

    
    elif cmd_split[0] == 'open':
      # Open something.

      name = cmd_split[1]
      name_split = name.split('.')
      os.system('say -v samantha "Opening ' + name + '"')
      
      
      if len(name_split) == 1:
        # Open OSX Application.
  
        path = os.popen('mdfind ' + name + ' kind:application').read()
        print path
      
        os.system('open -a ' + path)
      
      
      else:
        # Open a webpage in a default browser.

        url = 'http://' + name_split[0] + '.' + name_split[1]
        os.system('open ' + url)
    
    
    elif cmd_split[0] == 'what':
      # Open Dictionary for the meaning of a given word.

      if cmd == 'what is the weather now':
        ask_google(cmd)

      else:
        os.system('say -v samantha "Opening Dictionary"')

        word = cmd_split[-1]
        os.system('open dict://' + word)

    
    elif cmd_split[0] == 'set':
      # Set the volume or brightness.

      os.system('say -v samantha "Sure"')

      if (cmd_split[1] == 'volume') or (cmd_split[2] == 'volume'):
        # Set the volume.

        volume = cmd_split[-1]

        if volume[:1] == '1':
          print volume[:1]
          os.system('echo ' + sys_password + ' | sudo -S osascript -e "set Volume 10"')
        else:
          os.system('echo ' + sys_password + ' | sudo -S osascript -e "set Volume ' + volume[1:] + '"')

      else:
        # Set the brightness.

        brightness = cmd_split[-1]

        if len(brightness) == 1:
          print str(float(brightness)/10)
          os.system('brightness ' + str(float(brightness)/10))

        else:
          os.system('brightness ' + brightness[1:])

    
    elif (cmd_split[0] == 'how') or (cmd_split[0] == 'who'):
      # Generic questions, ask google.

      ask_google(cmd)


    elif cmd_split[0] == 'play':
      # Play movie or music.

      if cmd_split[1] == 'itunes':
        os.system('say -v samantha "Sure"')
        os.system(""" osascript -e 'tell application "iTunes" to play' """)

      else:
        play_cmd = cmd_split
        play_cmd.pop(0)

        os.system('osascript -e')


    elif (cmd_split[0] == 'pause') or (cmd_split[0] == 'stop'):
      # Pause movie or music.

      os.system(""" osascript -e 'tell application "iTunes" to pause' """)
      
    
    return 'success'
  else:
    print 'this is get request'

if __name__ == "__main__":
  app.run(debug=True)
