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
    p1pos = workbook['G20'].value
    p2pos = workbook['G21'].value
    p3pos = workbook['G22'].value
    p4pos = workbook['G23'].value
    p5pos = workbook['G24'].value
    p6pos = workbook['G25'].value
    p7pos = workbook['G26'].value
    p8pos = workbook['G27'].value
    wb.save(filename='Pasta1project.xlsx')
    return render_template("jogos_page.html", p1 = p1, p2 = p2, p3 = p3, p4 = p4, p5 = p5, p6 = p6, p7 = p7, p8 = p8,  
    p1pos = p1pos, p2pos = p2pos, p3pos = p3pos, p4pos = p4pos, p5pos = p5pos, p6pos = p6pos, p7pos = p7pos, p8pos = p8pos,)
