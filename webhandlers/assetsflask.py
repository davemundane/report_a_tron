from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import assets, singledocs, thirdparty, issues

assetConnection = assets.Assets()
docConnection = singledocs.Docs()
tpConnection = thirdparty.Thirdparty()
issueConnection = issues.Issues()

def createasset():
    return render_template('createasset.html')

def viewassets():
    data = assetConnection.getAssets()
    return render_template('viewassets.html', data=data)

def createassetapi():
    asset_name = request.form['asset_name']
    asset_type = request.form['asset_type']
    asset_owner = request.form['asset_owner']
    asset_notes = request.form['asset_notes']
    asset_internet_facing = request.form['asset_internet_facing']

    if asset_internet_facing == "No":
        asset_internet_facing = 0
    elif asset_internet_facing == "Yes":
        asset_internet_facing = 1
    else:
        asset_internet_facing = ""

    try:
        timenow = datetime.datetime.now().isoformat().split(".")[0]
        asset_id = assetConnection.createAsset(asset_name, asset_type, asset_owner, timenow, asset_notes, asset_internet_facing)

        if asset_type == "Third Party":
            tpConnection.createThirdParty(asset_id, asset_name, asset_owner)

        return redirect(url_for("viewassets"))

    except:
        return redirect(url_for("error"))

def updateasset():
    asset_id = request.args.get('asset_id')
    data = docConnection.getDoc(asset_id)
    return render_template('updateasset.html', data=data)

def updateassetapi():
    asset_id = request.form['asset_id']
    asset_name = request.form['asset_name']
    asset_type = request.form['asset_type']
    asset_owner = request.form['asset_owner']
    asset_notes = request.form['asset_notes']
    related_components = request.form['related_components']
    asset_internet_facing = request.form['asset_internet_facing']
    asset_active = request.form['asset_active']

    related_components_list = []
    for component in related_components.split(','):
        related_components_list.append(component)

    if asset_internet_facing == "No":
        asset_internet_facing = 0
    elif asset_internet_facing == "Yes":
        asset_internet_facing = 1
    else:
        asset_internet_facing = ""

    if asset_active == "No":
        issue_data = issueConnection.getIssuesFilter({"asset_id": asset_id})
        if issue_data:
            for issue in issue_data:
                issue_id = issue['_id']
                issueConnection.closeSingleIssue(issue_id)

    try:
        assetConnection.updateAsset(asset_id, asset_name, asset_type, asset_owner, asset_notes, related_components_list, asset_internet_facing, asset_active)

        return redirect(url_for("viewassets"))

    except:
        return redirect(url_for("error"))
