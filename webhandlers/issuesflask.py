from flask import Flask, render_template, request, redirect, url_for, escape
import datetime
from elasticstuff import singledocs, issues, assets
import html

docConnection = singledocs.Docs()
issueConnection = issues.Issues()

def viewissues():
    engagement_id = request.args.get('engagement_id')
    asset_id = request.args.get('asset_id')
    test_id = request.args.get('test_id')
    asset_name = request.args.get('asset_name')
    if test_id:
        data = issueConnection.getIssuesFilter({"test_id": test_id})
        return render_template('viewissues.html', data=data)
    if asset_id:
        data = issueConnection.getIssuesFilter({"asset_id": asset_id})
        return render_template('viewissues.html', data=data)
    if engagement_id:
        data = issueConnection.getIssuesFilter({"engagement_id": engagement_id})
        return render_template('viewissues.html', data=data)
    else:
        data = issueConnection.getIssues()
        return render_template('viewissues.html', data=data)

def createissue():
    #asset_id = request.args.get('asset_id')
    #engagement_id = request.args.get('engagement_id')
    test_id = request.args.get('test_id')
    asset_id = request.args.get('asset_id')
    if test_id:
        test_document = docConnection.getDoc(test_id)
        asset_id = test_document['_source']['test_stuff']['test_has_assets'][0]
        engagement_id = test_document['_source']['test_stuff']['test_has_engagements'][0]
        assets = docConnection.getAssets()

        return render_template("createissue.html", asset_id=asset_id, engagement_id=engagement_id, test_id=test_id, assets=assets)

    elif asset_id:
         assets = docConnection.getAssets()
         return render_template("createissue.html", asset_id=asset_id, assets=assets)

def createissueapi():
    linked_assets = request.form['linked_assets']
    asset_id = request.form['asset_id']
    engagement_id = request.form['engagement_id']
    test_id = request.form['test_id']
    issue_title = request.form['issue_title']
    issue_location = request.form['issue_location']
    issue_description = request.form['issue_description']
    issue_remediation = request.form['issue_remediation']
    issue_risk_rating = request.form['issue_risk_rating']
    issue_risk_impact = request.form['issue_risk_impact']
    issue_risk_likelihood = request.form['issue_risk_likelihood']
    issue_status = request.form['issue_status']
    issue_details = request.form['issue_details']
    issue_notes = request.form['issue_notes']

    issue_details = html.escape(issue_details)

    if test_id:
        test_document = docConnection.getDoc(test_id)

        asset_list = test_document['_source']['test_stuff']['test_has_assets']
        asset_name_list = test_document['_source']['test_stuff']['test_has_asset_names']
        engagement_id = test_document['_source']['test_stuff']['test_has_engagements'][0]

        try:
            timenow = datetime.datetime.now()
            issueConnection.createissue(asset_list, asset_name_list, engagement_id, test_id, issue_title, issue_location, issue_description, issue_remediation, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_status, issue_details, issue_notes, timenow)

        except Exception as error:
            return redirect(url_for("error"))

        return redirect(url_for("createissue", asset_id=asset_id, engagement_id=engagement_id, test_id=test_id))

    else:
        asset_doc = docConnection.getDoc(asset_id)
        asset_list = [linked_assets]
        asset_name_list = [asset_doc['_source']['asset_stuff']['asset_name']]

        try:
            timenow = datetime.datetime.now()
            issueConnection.createissue(asset_list, asset_name_list, None, None, issue_title, issue_location, issue_description, issue_remediation, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_status, issue_details, issue_notes, timenow)

        except Exception as error:
            return redirect(url_for("error"))

        return redirect(url_for("createissue", asset_id=asset_id))


def updateissue():
    issue_id = request.args.get('issue_id')
    assets = docConnection.getAssets()
    try:
        data = docConnection.getDoc(issue_id)
        return render_template("updateissue.html", data=data, assets=assets)
    except:
        return redirect(url_for("error"))

def updateissueapi():
    linked_assets = request.form['linked_assets']
    issue_id = request.form['issue_id']
    issue_status = request.form['issue_status']
    issue_title = request.form['issue_title']
    issue_risk_rating = request.form['issue_risk_rating']
    issue_risk_impact = request.form['issue_risk_impact']
    issue_risk_likelihood = request.form['issue_risk_likelihood']
    issue_location = request.form['issue_location']
    issue_description = request.form['issue_description']
    issue_remediation = request.form['issue_remediation']
    issue_details = request.form['issue_details']
    issue_notes = request.form['issue_notes']
    issue_ra_date = request.form['issue_ra_date']
    issue_ra_owner = request.form['issue_ra_owner']
    issue_ra_expiry = request.form['issue_ra_expiry']
    issue_ra_notes = request.form['issue_ra_notes']
    issue_due_date = request.form['issue_due_date']
    asset_list = []
    asset_name_list = []
    for asset_id in linked_assets.split(','):
        asset_list.append(asset_id)
        asset_name = docConnection.getDoc(asset_id)['_source']['asset_stuff']['asset_name']
        asset_name_list.append(asset_name)

    issue_details = html.escape(issue_details)

    if issue_ra_date == "" or issue_ra_date == "None":
        issue_ra_date = None
    if issue_ra_expiry == "" or issue_ra_expiry == "None":
        issue_ra_expiry = None

    try:
        issueConnection.updateIssue(asset_list, asset_name_list, issue_id, issue_title, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_location, issue_status, issue_description, issue_remediation, issue_details, issue_notes, issue_ra_date, issue_ra_owner, issue_ra_expiry, issue_ra_notes, issue_due_date)
        return redirect(url_for("viewissues"))
    except:
        return redirect(url_for("error"))
