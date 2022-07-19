from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, engagements

docConnection = singledocs.Docs()
engagementConnection = engagements.Engagements()

def engagements():
	asset_name = request.args.get('asset_name')
	asset_id = request.args.get('asset_id')
	assets = docConnection.getAssets()
	if asset_name:
		return render_template("engagements.html", asset_name=asset_name, asset_id=asset_id, assets=assets)
	else:
		return render_template("engagements.html", assets=assets)

def createengagement():
	linked_assets = request.form['linked_assets']
	engagement_form_location = request.form['engagement_form_location']
	engagement_main_contact = request.form['engagement_main_contact']
	engagement_risk_rating = request.form['engagement_risk_rating']
	engagement_received_on = request.form['engagement_received_on']
	engagement_action_taken = request.form['engagement_action_taken']
	engagement_notes = request.form['engagement_notes']
	asset_list = []
	asset_name_list = []
	if linked_assets:
		for asset_id in linked_assets.split(','):
			asset_list.append(asset_id)
			asset_name = docConnection.getDoc(asset_id)['_source']['asset_stuff']['asset_name']
			asset_name_list.append(asset_name)

	try:
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		engagementConnection.createEngagement(asset_name_list,asset_list,engagement_form_location,engagement_main_contact,engagement_risk_rating,engagement_received_on,engagement_action_taken,engagement_notes)
		return redirect(url_for("viewengagements"))
	except:
		return redirect(url_for("error"))

def openengagements():
	data = engagementConnection.getOpenEngagements()
	return render_template('viewengagements.html', data=data)

def viewengagements():
	asset_id = request.args.get('asset_id')
	asset_name = request.args.get('asset_name')

	if asset_id:
		data = engagementConnection.getEngagementsForAsset(asset_id)
		return render_template('viewengagements.html', data=data, asset_name=asset_name)
	else:
		data = engagementConnection.getEngagements()
		return render_template('viewengagements.html', data=data)

def updateengagement():
	engagement_id = request.args.get('engagement_id')
	data = docConnection.getDoc(engagement_id)
	assets = docConnection.getAssets()
	return render_template('updateengagement.html', data=data, assets=assets)

def updateengagementapi():
	linked_assets = linked_assets = request.form['linked_assets']
	engagement_id = request.form['engagement_id']
	engagement_form_location = request.form['engagement_form_location']
	engagement_main_contact = request.form['engagement_main_contact']
	engagement_risk_rating = request.form['engagement_risk_rating']
	engagement_received_on = request.form['engagement_received_on']
	engagement_action_taken = request.form['engagement_action_taken']
	engagement_notes = request.form['engagement_notes']
	engagement_status = request.form['engStatus']

	asset_list = []
	asset_name_list = []
	if linked_assets:
		for asset_id in linked_assets.split(','):
			asset_list.append(asset_id)
			asset_name = docConnection.getDoc(asset_id)['_source']['asset_stuff']['asset_name']
			asset_name_list.append(asset_name)

	try:
		engagementConnection.updateengagementapi(asset_name_list,asset_list,engagement_id,engagement_form_location,engagement_main_contact,engagement_risk_rating,engagement_received_on,engagement_action_taken,engagement_notes,engagement_status)
		return redirect(url_for("viewengagements"))
	except:
		return redirect(url_for("error"))
