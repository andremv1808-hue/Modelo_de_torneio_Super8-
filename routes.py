from main import app, workbook, wb
from flask import render_template, request


@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/jogos", methods=['POST'])

def receber():
    p1 = workbook['B3'] = request.form.get('atleta1')
    p2 = workbook['B4'] = request.form.get('atleta2')
    p3 = workbook['B5'] = request.form.get('atleta3')
    p4 = workbook['B7'] = request.form.get('atleta4')
    p5 = workbook['B8'] = request.form.get('atleta5')
    p6 = workbook['B6'] = request.form.get('atleta6')
    p7 = workbook['B9'] = request.form.get('atleta7')
    p8 = workbook['B10'] =request.form.get('atleta8')
    wb.save(filename='Pasta1project.xlsx')
    return render_template("jogos_page.html", p1 = p1, p2 = p2, p3 = p3, p4 = p4, p5 = p5, p6 = p6, p7 = p7, p8 = p8 )
