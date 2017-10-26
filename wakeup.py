from flask import Flask, request, make_response, render_template, redirect, url_for, Response
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import plivo, plivoxml

app = Flask(__name__)
auth_id = "AUTH_ID"
auth_token = "AUTH_TOKEN"

def alarm(number):
    p = plivo.RestAPI(auth_id, auth_token)
    params = {'to': number,'from' : '16623829952','answer_url' : "http://molson194.tk/answer.xml",'answer_method' : "GET"}
    response = p.make_call(params)
    print str(response)

@app.route('/done/')
def done():
	return render_template('done.html')

@app.route('/',methods=['GET','POST'])
def main():
	scheduler = BackgroundScheduler()
	if request.method == 'POST':
		phone = '1'+request.form['area_code']+request.form['phone_middle']+request.form['phone_last']
		date = request.form['date'].encode('ascii','ignore')
		time = request.form['time'].encode('ascii','ignore')
		zone = request.form['zone'].encode('ascii','ignore')
		date_array = date.replace('-', ' ').split(' ')
		time_array = time.replace(':', ' ').split(' ')
		call_date = datetime(int(date_array[0]),int(date_array[1]),int(date_array[2]),int(time_array[0]), int(time_array[1]))
		if zone == 'ET':
			call_date = call_date + timedelta(hours=4)
		elif zone == 'CT':
			call_date = call_date + timedelta(hours=5)
		elif zone == 'MT':
			call_date = call_date + timedelta(hours=6)
		elif zone == 'PT':
			call_date = call_date + timedelta(hours=7)
		scheduler.add_job(alarm, 'date', run_date=call_date, args=[phone])
		scheduler.start()
		return redirect(url_for('done'))
	else:
		return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
