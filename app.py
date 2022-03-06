from flask import Flask, render_template, redirect 
from tool_logging import Watcher, MyHandler
w = Watcher(".", MyHandler())
app = Flask(__name__)

@app.route("/")#Loading index.html
def home():
    running = w.running
    return render_template("index.html", running=running)

@app.route("/start", methods = ['POST'])#Allow post request
def start_script():
    w.run()#start watchdog script
    return redirect("/")

@app.route("/stop", methods = ['POST'])#Allow post request
def stop_script():
    w.stop()#Stop watchdog script
    return redirect("/")

