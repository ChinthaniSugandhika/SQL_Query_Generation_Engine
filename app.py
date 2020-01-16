from flask import Flask, render_template, request
import  main

app = Flask(__name__)
sql_query_1=''
sql_query_2=''
text =''
tables= ''
attributes=''
conditions=''
joins = ''
table_names = ''
attribute_names = "*"
join_types = ''
condition_types = ''

@app.route('/')
def home():
    return render_template('queryGenerator.html')

@app.route('/submit', methods=['POST'])
def submit():
    global sql_query, tables, attributes, conditions, text, sql_query_1, sql_query_2
    print('xy')
    if request.method == 'POST':
        if request.form['submit_btn'] == 'generate_sql':
            text =  request.form['naturalQuery']
            output_dic = main.generateSqlQuery(text)
            sql_query_1 =  output_dic['query']
            tables = output_dic['tables']
            attributes = output_dic['attributes']
            conditions = output_dic['conditions']
            print(output_dic)
        if request.form['submit_btn'] == 're_generate_sql':
            print("xyz")
            table_names =  request.form['tableNames']
            attribute_names = request.form['attributes']
            join_types=request.form['tableJoins']
            condition_types =  request.form['conditions']
            sql_query_2 = main.regenarteSqlQuery(table_names,attribute_names,join_types,condition_types)

    return render_template('queryGenerator.html',sql_query_1=sql_query_1,tables=tables,attributes=attributes,conditions=conditions,text=text,sql_query_2=sql_query_2)

if __name__ == '__main__':
    app.run()
