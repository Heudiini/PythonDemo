from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import csv

def read_grades_from_file(filepath):
    # Function to read grades from a CSV file and return a dictionary
    grades = {}
    with open(filepath, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        lines = list(reader)

        if not lines:
            raise ValueError('The CSV file is empty.')

        if len(lines) <= 1:
            raise ValueError('The CSV file must have more than one line.')

        header = lines[0]
        expected_columns = 11  # Assuming there are 11 columns in each line, adjust as needed

        if len(header) != expected_columns:
            raise ValueError(f'The CSV file has an incorrect number of columns. Expected {expected_columns}, but got {len(header)}.')

        for line_num, line in enumerate(lines[1:], start=2):  # Start from the second line (skip header)
            try:
                name = line[0]
                grades[name] = [int(grade) if grade != '' else None for grade in line[1:]]
            except (ValueError, IndexError) as e:
                raise ValueError(f'Error in line {line_num}: {str(e)}')
            except Exception as e:
                raise ValueError(f'Error in line {line_num}: {str(e)}. Ensure all grades are numeric.')

    return grades


def calculate_top_performers(grades_dict):
    # Function to calculate top performers based on average grades
    cleaned_grades = {name: [grade for grade in grades if grade is not None] for name, grades in grades_dict.items()}

    average_grades = {name: sum(grades) / len(grades) for name, grades in cleaned_grades.items()}
    sorted_performers = sorted(average_grades.items(), key=lambda x: (x[1], x[0]))

    top_performers = []
    current_grade = None
    current_rank = 0
    for performer, grade in sorted_performers:
        if current_grade is None or grade == current_grade:
            current_rank += 1
        else:
            current_rank += 1
        top_performers.append((performer, grade, current_rank))
        current_grade = grade

    return top_performers


def process_performers(uploaded_grades, top_performers):
    # Function to process performers and categorize them into medal groups
    medal_performers = {"Gold": [], "Silver": [], "Bronze": []}
    grade_groups = {}

    for _, (name, average_grade, _) in enumerate(top_performers, start=1):
        if average_grade not in grade_groups:
            grade_groups[average_grade] = []

        grade_groups[average_grade].append((name, average_grade))

    for average_grade, performers in sorted(grade_groups.items(), reverse=True):
        if average_grade == 4.0 and len(medal_performers["Gold"]) < 3:
            medal_performers["Gold"].extend(performers)
        elif average_grade == 3.9 and len(medal_performers["Silver"]) < 3:
            medal_performers["Silver"].extend(performers)
        elif average_grade == 3.8 and len(medal_performers["Bronze"]) < 3:
            medal_performers["Bronze"].extend(performers)

    return medal_performers


def create_upload_folder():
    # Function to create the upload folder if it doesn't exist
    upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


@app.route('/', methods=['GET', 'POST'])
def show_grades():
    # Main route function to display grades and process file uploads
    create_upload_folder()

    gold_performers = []
    silver_performers = []
    bronze_performers = []
    all_performers = []
    error_message = None
    uploaded_grades = {}
    top_performers = []
    medal_performers = {}
    file_name = None  # Initialize file_name variable

    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                raise FileNotFoundError('No file part')

            file = request.files['file']

            if file.filename == '':
                raise FileNotFoundError('No selected file')

            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                file_name = file.filename  # Set the file_name variable

                print(f'File uploaded successfully: {file_path}')

                # Read grades from the uploaded file
                uploaded_grades = read_grades_from_file(file_path)

                # Calculate top performers
                top_performers = calculate_top_performers(uploaded_grades)
                print("Top Performers:", top_performers)

                # Process grades and populate performers (gold, silver, bronze, all)
                medal_performers = process_performers(uploaded_grades, top_performers)

                return render_template(
                    'index.html',
                    medal_performers=medal_performers,
                    uploaded_grades=uploaded_grades,
                    top_performers=top_performers,
                    error=error_message,
                    upload_success=True,
                    file_name=file_name,
                )
    except FileNotFoundError as e:
        error_message = f'Error processing the file: {str(e)}'
        print(error_message)
    except IndexError as e:
        error_message = f'Error processing the file: {str(e)}'
        print(error_message)
    except ValueError as e:
        error_message = str(e)

    return render_template(
        'index.html',
        gold_performers=gold_performers,
        silver_performers=silver_performers,
        bronze_performers=bronze_performers,
        uploaded_grades=uploaded_grades,
        top_performers=top_performers,
        all_performers=all_performers,
        medal_performers=medal_performers,
        error=error_message,
        upload_success=False
    )

if __name__ == '__main__':
    app.run(debug=True)
