from flask import Flask, render_template, request, redirect, url_for, session
from elasticstuff import search, logger
from webhandlers import assetsflask, engagementsflask, testsflask, issuesflask, thirdpartyflask, servicesflask, statsflask, reportsflask, loginflask
from waitress import serve
import config
import flask_login
from datetime import timedelta
import flask


application = Flask(__name__)
config_values = config.StaticValues().config_file
application.config.from_object(config_values['config_type'])
application.config["CACHE_TYPE"] = "null"
#application.permanent_session_lifetime = timedelta(minutes=60)

searchConnection = search.Search()

login_manager = flask_login.LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'
#logger_instance = logger.Logger()

@application.before_request
def before_request():
    flask.session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=20)
    flask.session.modified = True
    flask.g.user = flask_login.current_user

@login_manager.user_loader
def user_loader(username):
    return loginflask.user_loader(username)

@application.route('/login', methods=['GET'])
def login():
	return loginflask.login()

@application.route('/loginapi', methods=['POST'])
def loginapi():
    return loginflask.loginapi()

@application.route('/onboardotp', methods=['GET'])
def onboardotp():
    return loginflask.onboardotp()

@application.route('/onboardotpapi', methods=['POST'])
def onboardotpapi():
    return loginflask.onboardotpapi()

@application.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@application.route('/changepassword')
@flask_login.login_required
def changepassword():
    return loginflask.changepassword()

@application.route('/changepasswordapi', methods=['POST'])
@flask_login.login_required
def changepasswordapi():
    return loginflask.changepasswordapi()

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@application.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.cache_control.max_age = 0
    response.headers['Server'] = 'Report-a-Tron'
    return response

@application.before_request
def checkPermissions():
    if flask_login.current_user.is_anonymous:
        pass
    else:
        if flask_login.current_user.role in config_values['authorization'][request.path]:
            pass
        else:
            return render_template('autherror.html')

@application.route("/")
@flask_login.login_required
def main():
	return render_template('index.html')

@application.route("/createasset")
@flask_login.login_required
def createasset():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return assetsflask.createasset()

@application.route("/error")
@flask_login.login_required
def error():
	return render_template('error.html')

@application.route("/viewassets")
@flask_login.login_required
def viewassets():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return assetsflask.viewassets()

@application.route("/createassetapi", methods=['POST'])
@flask_login.login_required
def createassetapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return assetsflask.createassetapi()

@application.route("/updateasset")
@flask_login.login_required
def updateasset():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return assetsflask.updateasset()

@application.route("/updateassetapi", methods=['POST'])
@flask_login.login_required
def updateassetapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return assetsflask.updateassetapi()

@application.route("/engagements", methods=['GET'])
@flask_login.login_required
def engagements():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.engagements()

@application.route("/createengagement", methods=['POST'])
@flask_login.login_required
def createengagement():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.createengagement()

@application.route("/openengagements")
@flask_login.login_required
def openengagements():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.openengagements()

@application.route("/viewengagements")
@flask_login.login_required
def viewengagements():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.viewengagements()

@application.route("/updateengagement")
@flask_login.login_required
def updateengagement():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.updateengagement()

@application.route("/updateengagementapi", methods=['POST'])
@flask_login.login_required
def updateengagementapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return engagementsflask.updateengagementapi()

@application.route("/createtest", methods=['GET'])
@flask_login.login_required
def createtest():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return testsflask.createtest()

@application.route("/createtestapi", methods=['POST'])
@flask_login.login_required
def createtestapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return testsflask.createtestapi()

@application.route("/viewtests", methods=['GET'])
@flask_login.login_required
def viewtests():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return testsflask.viewtests()

@application.route("/updatetest")
@flask_login.login_required
def updatetest():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return testsflask.updatetest()

@application.route("/updatetestapi", methods=['POST'])
@flask_login.login_required
def updatetestapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return testsflask.updatetestapi()

@application.route("/viewissues", methods=['GET'])
@flask_login.login_required
def viewissues():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return issuesflask.viewissues()

@application.route("/createissue", methods=['GET'])
@flask_login.login_required
def createissue():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return issuesflask.createissue()

@application.route("/createissueapi", methods=['POST'])
@flask_login.login_required
def createissueapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return issuesflask.createissueapi()

@application.route("/updateissue", methods=['GET'])
@flask_login.login_required
def updateissue():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return issuesflask.updateissue()

@application.route("/updateissueapi", methods=['POST'])
@flask_login.login_required
def updateissueapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return issuesflask.updateissueapi()

@application.route("/testreport", methods=['GET'])
@flask_login.login_required
def testreport():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return reportsflask.testReport()

@application.route("/servicereport", methods=['GET'])
@flask_login.login_required
def servicereport():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return reportsflask.serviceReport()

@application.route("/assetreport", methods=['GET'])
@flask_login.login_required
def assetreport():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return reportsflask.assetReport()

@application.route("/stats")
@flask_login.login_required
def stats():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return render_template('stats.html')

@application.route("/viewstats")
@flask_login.login_required
def viewstats():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return statsflask.viewstats()

@application.route("/search")
@flask_login.login_required
def search():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    searchTerm = request.args.get('searchTerm')
    data = searchConnection.search(searchTerm)
    return render_template('searchresults.html', data=data)

@application.route("/viewthirdparty")
@flask_login.login_required
def viewthirdparty():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return thirdpartyflask.viewthirdparty()

@application.route("/createthirdparty")
@flask_login.login_required
def createthirdparty():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return render_template('createthirdparty.html')

@application.route("/updatethirdparty")
@flask_login.login_required
def updatethirdparty():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return thirdpartyflask.updatethirdparty()

@application.route("/updatethirdpartyapi", methods=['POST'])
@flask_login.login_required
def updatethirdpartyapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return thirdpartyflask.updatethirdpartyapi()

@application.route('/viewservices')
@flask_login.login_required
def viewservices():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return servicesflask.viewservices()

@application.route('/viewservicedetail')
@flask_login.login_required
def viewservicedetail():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    service_id = request.args.get('service_id')
    return servicesflask.viewservicedetail(service_id)

@application.route('/createservice')
@flask_login.login_required
def createservice():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return servicesflask.createservice()

@application.route('/createserviceapi', methods=['POST'])
@flask_login.login_required
def createserviceapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return servicesflask.createserviceapi()

@application.route('/updateservice')
@flask_login.login_required
def updateservice():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    service_id = request.args.get('service_id')
    return servicesflask.updateservice(service_id)

@application.route('/updateserviceapi', methods=['POST'])
@flask_login.login_required
def updateserviceapi():
    #logger_instance.createLog({"transaction_event": {"path": request.base_url, "method": request.method, "remote_addr": request.remote_addr, "user_agent": str(request.user_agent), "data": str(request.form)}}, session['user_id'])
    return servicesflask.updateserviceapi()

@application.route('/breakout-a-tron', methods=['GET'])
@flask_login.login_required
def breakout():
    return render_template('breakout-a-tron.html')

#@application.route("/thereport")
#@flask_login.login_required
#def thereport():
#	return render_template('thereport.html')

@application.route("/<variable>", methods=['GET'])
@flask_login.login_required
def thereport():
	return reportsflask.showReport()

if __name__ == "__main__":
    if config_values['deployment_server'] == "waitress":
        serve(application, host=config_values['server_ip'], port=int(config_values['server_port']))
    else:
        application.run(host=config_values['server_ip'], port=int(config_values['server_port']))
