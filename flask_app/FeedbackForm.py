from flask import Flask,render_template,json,request,flash,redirect,url_for
from nylas import APIClient

app = Flask(__name__)
app.config.from_file("config.json", json.load)

def load_nylas():
	nylas = APIClient(
		app.config["NYLAS_OAUTH_CLIENT_ID"],
		app.config["NYLAS_OAUTH_CLIENT_SECRET"],
		app.config["SECRET_KEY"]
	)
	return nylas
	
@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('FeedbackForm.html')
	else:
		name = request.form['name']
		email = request.form['email']
		rating = request.form['rating']
		comments = request.form['comments']
		
		if not name:
			flash('Name is required!')
			return redirect(url_for('index'))
		elif not email:
			flash('Email is required!')
			return redirect(url_for('index'))
		elif not comments:
			flash('Comments are required!')
			return redirect(url_for('index'))			
		else:
			nylas = load_nylas()
			draft = nylas.drafts.create()
			draft.subject = "VeggiEggs Feedback - {} - {} - {}".format(name, email, rating)
			draft.body = comments
			draft.to = [{"name": "Blag", "email": "alvaro.t@nylas.com"}]

			draft.send()			
			return render_template('ConfirmationForm.html', 
									name = name, email = email, 
									rating = rating, comments=comments), {"Refresh":"5;url=/"}
		
if __name__ == "__main__":
	app.run()			
