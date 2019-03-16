from flask import Flask, send_from_directory, url_for, json, Response, jsonify, request
from rejson import Client, Path
import sys
# from flask_restplus import Resource, Api

app = Flask(__name__, static_folder='static')
rj = Client(host='redis', port=6379)
# api = Api(app)
# api = Api(app, doc='/documentation/')
# assert url_for('doc') == '/documentation/'

def build_response_from_literal(json_string):
    return Response(json.dumps(json_string), mimetype='application/json')

@app.route('/hello')
def hello():
    return build_response_from_literal({'hello': 'Team Health Techies'})

@app.route('/api/patients', methods=['GET','POST'])
def api_patients():
    if request.method=='POST':
        obj = request.json
        patientid = obj['data']['patientinfo']['id']
        rj.jsonset(patientid, Path.rootPath(), obj)
        return build_response_from_literal({'obj': 'Successfully added patient ' + patientid})
    else:
        # GET all patients.
        keys = rj.keys("*")
        if len(keys) > 0:
            all_patients = rj.jsonmget("data", *keys) # Pass in keys as unnamed args.

            # Convert list of dicts into list strings.
            all_patients = [json.dumps(p) for p in all_patients]
            # Seperate each patient with commas and wrap it with data property.
            resp = "{ \"data\": [" + ','.join(all_patients) + "] }"
            return Response(resp, mimetype='application/json')
        else:
            # Return there's nothing stored, return dummy data.
            return build_response_from_literal({'data': [{'assessment': {'labs': {'serumcreatinine': '1.2','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {},'withoutindwelling': {'backpainCriteria2': 'Yes','criteria1': 'Yes','criteria2': 'Yes','dementia': 'Yes','frequencyCriteria2': 'Yes','hematuriaCriteria2': 'Yes','incontinenceCriteria2': 'Yes','scrotalTenderness': 'Yes','suprapubicCriteria2': 'Yes','urgencyCriteria2': 'Yes'}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','penicillinallergy': 'Yes','prostatitis': 'Yes','pyelonephritis': 'Yes','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 65,'date': '11-16-2018','gender': 'male','id': '200','name': 'Ravi Tamada','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}},{'assessment': {'labs': {'serumcreatinine': '1.4','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {'backpain': 'Yes','delirium': 'Yes','fever100repeat99': 'Yes','hypertension': 'Yes','shakes': 'Yes','suprapubic': 'Yes'},'withoutindwelling': {}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','indwelling catheter': 'yes','penicillinallergy': 'Yes','pyelonephritis': 'Yes','type': 'urethral','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 67,'date': '11-16-2018','gender': 'female','id': '201','name': 'Jane Smith','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}},{'assessment': {'labs': {'serumcreatinine': '0.8','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {'backpain': 'Yes','delirium': 'Yes','fever100repeat99': 'Yes','hypertension': 'Yes','scrotalswelling': 'Yes','shakes': 'Yes','suprapubic': 'Yes'},'withoutindwelling': {}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','indwelling catheter': 'yes','penicillinallergy': 'Yes','prostatitis': 'Yes','pyelonephritis': 'Yes','type': 'urethral','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 65,'date': '11-16-2018','gender': 'male','id': '202','name': 'Wakaru Hosokawa','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}},{'assessment': {'labs': {'serumcreatinine': '0.9','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {},'withoutindwelling': {'criteria3': 'Yes','frequencyCriteria3': 'Yes','hematuriaCriteria3': 'Yes'}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','indwelling catheter': 'yes','prostatitis': 'Yes','pyelonephritis': 'Yes','type': 'urethral','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 73,'date': '11-16-2018','gender': 'female','id': '204','name': 'Ramiya Swaminathan','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}},{'assessment': {'labs': {'serumcreatinine': '2.0','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {},'withoutindwelling': {}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','indwelling catheter': 'yes','type': 'urethral','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 77,'date': '11-16-2018','gender': 'male','id': '210','name': 'Sean Jakobson','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}},{'assessment': {'labs': {'serumcreatinine': '0.8','type': 'UC'},'vitals': {'bphigh': '120','bplow': '80','hr': '60','o2sats': '100','resprate': '30','temp': '97'},'withindwelling': {},'withoutindwelling': {}},'background': {'diagnosis': 'kidney','directives': 'once a day','incontinence': 'yes','incontnew': 'yes','indwelling catheter': 'yes','penicillinallergy': 'Yes','type': 'urethral','uti6month': 'yes','uti6organism': 'providencia','uti6treatment': 'antibiotic'},'patientinfo': {'age': 72,'date': '11-16-2018','gender': 'female','id': '310','name': 'Michelle Chu','uticoncern': 'Yes'},'prescriptions': {},'recommendations': {}}]})

@app.route('/api/patients/<patientid>')
def api_patient(patientid):
    try:
        patient = rj.jsonget(patientid, Path.rootPath())
        return build_response_from_literal(patient)
    except TypeError:
        return build_response_from_literal({'data':{}})

@app.route('/api/sbars')
def api_sbars():
    return build_response_from_literal({'data':[{'sbar-id':4955737,'situation':{'uti':'Yes'},'background':{'indwelling cathetercathetar':'yes','type':'urethral','incontinence':'yes','incontnew':'yes','uti6':'yes','uti6date':'11-08-2018','uti6organism':'providencia','uti6treatment':'antibiotic','diagnosis':'kidney','directives':'once a day','allergies':'penicillin'},'assessment':{'vitals':[{'bplow':80,'bphigh':120,'hr':60,'resprate':30,'temp':97,'o2sats':100,'timestamp':'11-08-2019 24:13:00'}],'withindwelling':[{}],'withoutindwelling':[{}],'labs':[{'type':'UC','results':{}}]},'recommendations':[{}],'prescriptions':[{}]}]})

@app.route('/api/recommendation')
def api_recommendation():
    return build_response_from_literal({'data':[{'sbar-id':'4955737','CrCl':-1.24,'drug':'Nitrofurantoin','dosage':'50mg','route':'oral (by mouth)','frequency':'twice a day'}], 'error':{}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_page(path):
    if not path:
        path = 'index.html'
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
