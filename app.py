# /// script
# dependencies = [
#   "flask",
#   "pandas",
#   "gspread",
#   "oauth2client",
# ]
# ///

import pandas as pd
from flask import Flask, render_template, request, redirect, session, url_for, flash
from sheets import get_users, register_user
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ANNOUNCEMENT_SHEET_ID = os.getenv("ANNOUNCEMENT_SHEET_ID")
MATERIALS_SHEET_ID = os.getenv("MATERIALS_SHEET_ID")
SEMESTER_MATERIALS_SHEET_ID = os.getenv("SEMESTER_MATERIALS_SHEET_ID")
WEEKLY_PLANER_SHEET_ID = os.getenv("WEEKLY_PLANER_SHEET_ID")

app = Flask(__name__)

app.secret_key = SECRET_KEY



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/timetable.html')
def timetable(): 
    return render_template('timetable.html')

@app.route('/announcements.html')
def announcements():
    Sheet_ID = ANNOUNCEMENT_SHEET_ID
    df  = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{Sheet_ID}/export?format=csv") 
    announcements = df.to_dict(orient='records') # converitng it to required format
    announcements = announcements[::-1]
    
    return render_template("announcements.html", announcements=announcements)

@app.route('/materials.html')
def materials_home():

    Sheet_ID = MATERIALS_SHEET_ID
    try:
        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{Sheet_ID}/export?format=csv")
        df.columns = df.columns.str.strip()
        semesters = sorted(df['year'].dropna().unique())
        return render_template("materials_home.html", semesters=semesters)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/materials/<semester>')
def semester_materials(semester):
    if 'username' not in session:
        return redirect(url_for('login'))

    Sheet_ID = SEMESTER_MATERIALS_SHEET_ID
    try:
        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{Sheet_ID}/export?format=csv")
        df.columns = df.columns.str.strip()
        semester_data = df[df['year'].str.strip() == semester.strip()]

        grouped_materials = {}

        for _, item in semester_data.iterrows():
            subject = item.get('Subject', '').strip()
            chapter = str(item.get('Chapter', '')).strip()
            my_notes_link = item.get('My Notes', '').strip()
            teachers_notes_link = item.get('teachers_notes', '').strip()

            if not subject or not chapter:
                continue

            if subject not in grouped_materials:
                grouped_materials[subject] = {'my_notes': {}, 'teachers_notes': {}}

            if my_notes_link and my_notes_link != '--':
                grouped_materials[subject]['my_notes'][chapter] = my_notes_link

            if teachers_notes_link and teachers_notes_link != '--':
                grouped_materials[subject]['teachers_notes'][chapter] = teachers_notes_link

        return render_template('semester_materials.html', semester=semester, grouped_materials=grouped_materials)
    except Exception as e:
        return f"An error occurred: {e}"
        
@app.route('/weekly.html')
def weekly_planner():
    import pandas as pd
    def spreadsheet_to_week_tasks():
        Sheet_ID = WEEKLY_PLANER_SHEET_ID
        df  = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{Sheet_ID}/export?format=csv") # taking data from spreadsheet
        week_tasks = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in days:
            # Safely access columns, handling cases where a day might be missing.
            if day in df.columns:
                # Drop NaN values and convert to a list.  Handles empty task lists.
                tasks = df[day].dropna().tolist()
                week_tasks[day] = tasks
            else:
                print(f"Warning: Day '{day}' not found as a column in the spreadsheet.  Assuming no tasks for this day.")
                week_tasks[day] = []  # Ensure every day has an entry, even if it's an empty list.

        week_date = df.loc[0, 'Week']

        return week_tasks, week_date
    
    week_tasks, week_date = spreadsheet_to_week_tasks()

    return render_template('weekly.html', week_tasks=week_tasks, week_date= week_date)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = get_users()
        username = request.form['username']
        password = request.form['password']
        print(username[:7])
        if username[:7] == 'BT23MME' and len(username) == 10:
            if any(u['Username'] == username for u in users):
                flash('Username already exists.', 'error')
            else:
                register_user(username, password)
                session['username'] = username
                session['message'] = f"{session['username']} Registered!"
                return redirect(url_for('login'))
        else:
            flash('Invalid username format :"BT23MMEXXX"', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = get_users()
        username = request.form['username']
        password = request.form['password']

        
        if any(u['Username'] == username and str(u['Password']) == password for u in users):
            session['username'] = username
            session['message'] = f"Welcome, {session['username']}!"
            return render_template('index.html', username  = session['username'])
        else:
            flash('Invalid user name or Passward.', 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True)