from flask import Flask, jsonify
import requests, json, datetime
app = Flask(__name__)

token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRS0QiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkxMDQxNzA4LCJpYXQiOjE2NTk1MDU3MDh9.NzxJB3FZxmWDyJx44pvUZOCkqME50heLRhYWD19z1go"
ptoken = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSTUIiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMjk2MDE4LCJpYXQiOjE2NjA3NjAwMTh9.Ud4qSIXGglbXaYeK-JDzL9GolEskKk9aCGrl79NMDY4"
myheader = {'Accept' : 'application/json', 'Authorization' : 'Bearer {}'.format(token)}
myPheader = {'Accept' : 'application/json', 'Authorization' : 'Bearer {}'.format(ptoken)}


userurl = "https://api.fitbit.com/1/user/-/profile.json"
userresp = requests.get(userurl, headers=myPheader).json()
@app.route("/name", methods=["GET"])
def get_name():
    global name
    name = userresp["user"]["fullName"]
    retStr = {'Name': name}
    return jsonify(retStr)


hearturl  = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json"
heartresp = requests.get(hearturl, headers=myPheader).json()
@app.route("/heartrate/last", methods=["GET"])
def get_last_heartrate():
    heart_rate = heartresp['activities-heart-intraday']['dataset'][-1]['value']
    time_taken = heartresp['activities-heart-intraday']['dataset'][-1]['time']
    current_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    time_offset = current_time - datetime.datetime.strptime(time_taken, '%H:%M:%S')
    str_time_offset:str = str(time_offset)

    retStr = {'Heartrate': heart_rate, 'time-offset':str_time_offset}
    return jsonify(retStr)


stepsurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json"
stepstimeurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d/1min.json"
stepsresp = requests.get(stepsurl, headers=myPheader).json()
stepstimeresp = requests.get(stepstimeurl, headers=myPheader).json()
@app.route("/steps/last", methods=["GET"])
def get_last_steps():
    steps = stepsresp["activities-steps"][0]["value"]
    current_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    last_steps_time = datetime.datetime.strptime(stepstimeresp["activities-steps-intraday"]["dataset"][-1]["time"], "%H:%M:%S")
    time_offset = current_time - last_steps_time
    str_time_offset:str = str(time_offset)

    retStr = {'steps': steps, 'time-offset': str_time_offset}
    return jsonify(retStr)


@app.route("/sleep/<date>")
def sleep_stages(date):
    sleepurl = "https://api.fitbit.com/1.2/user/-/sleep/date/" + date + ".json"
    sleepresp = requests.get(sleepurl, headers=myPheader).json()

    try:
        deep = sleepresp["summary"]["stages"]["deep"]
        light = sleepresp["summary"]["stages"]["light"]
        rem = sleepresp["summary"]["stages"]["rem"]
        wake = sleepresp["summary"]["stages"]["wake"]
    except:
        return "Nothing recorded on given day."

    retStr = {'deep': deep, 'light': light, 'rem': rem, 'wake': wake}
    return jsonify(retStr)
    

@app.route("/activity/<date>")
def activity_stages(date):
    myurl = "https://api.fitbit.com/1/user/-/activities/date/" + date + ".json"
    resp = requests.get(myurl, headers=myheader).json()

    sedentary = resp["summary"]["sedentaryMinutes"]
    light = resp["summary"]["lightlyActiveMinutes"]
    fair = resp["summary"]["fairlyActiveMinutes"]
    very = resp["summary"]["veryActiveMinutes"]

    retStr = {'very-active': very, 'fairly-active': fair, 'lightly-active': light, 'sedentary': sedentary}
    return jsonify(retStr)


if __name__ == '__main__':
    app.run(debug=True)