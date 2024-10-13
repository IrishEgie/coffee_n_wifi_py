from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    loc = StringField('Location URL (Google Maps)', validators=[DataRequired(), URL()])
    opening = StringField('Opening Time (e.g., 11AM)', validators=[DataRequired()])
    closing = StringField('Closing Time (e.g., 11PM)', validators=[DataRequired()])
    cafe_rating = SelectField('Cafe Rating', choices=[('☕️', '1 ☕️'), 
                                                       ('☕️☕️', '2 ☕️'), ('☕️☕️☕️', '3 ☕️'), 
                                                       ('☕️☕️☕️☕️', '4 ☕️'), ('☕️☕️☕️☕️☕️', '5 ☕️')],
                               validators=[DataRequired()])
    wifi_rating = SelectField('WiFi Rating', choices=[('💪', '1 💪'), 
                                                       ('💪💪', '2 💪'), ('💪💪💪', '3 💪'), 
                                                       ('💪💪💪💪', '4 💪'), ('💪💪💪💪💪', '5 💪')],
                               validators=[DataRequired()])
    power_rating = SelectField('Power Outlet Rating', choices=[('🔌', '1 🔌'), 
                                                                ('🔌🔌', '2 🔌'), ('🔌🔌🔌', '3 🔌'), 
                                                                ('🔌🔌🔌🔌', '4 🔌'), ('🔌🔌🔌🔌🔌', '5 🔌')],
                                validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


from flask import flash, redirect, url_for

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Collect the form data
        cafe_name = form.cafe.data
        loc = form.loc.data
        opening_time = form.opening.data
        closing_time = form.closing.data
        cafe_rating = form.cafe_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data

        # Write the data to CSV
        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{cafe_name}, {loc}, {opening_time}, {closing_time}, {cafe_rating}, {wifi_rating}, {power_rating}")
        
        # Print success message to the console
        print("Successfully added cafe:", cafe_name)

        # Flash a success message to the user
        flash(f'Successfully added cafe: {cafe_name}!', 'success')

        return redirect(url_for('cafes'))  # Redirect to the cafes page after submission

    return render_template('add.html', form=form)




@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        next(csv_data)
        list_of_rows = [row for row in csv_data]
        print(list_of_rows) 
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
