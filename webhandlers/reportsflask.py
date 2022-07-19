from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import reports
import reportcreator

reportConnection = reports.Reports()

def showReport(report_title):
    return render_template(report_title)

def testReport():

    test_id = request.args.get('test_id')

    test_data = reportConnection.getTestData(test_id)

    if test_data:
        issue_data = reportConnection.getIssueData(test_id)
        asset_data = reportConnection.getAssetData(test_data['_source']['test_stuff']['test_has_assets'][0])

    else:
        issue_data = None
        asset_data = None

    report_data = {"report_type": "test", "asset_data": asset_data, "test_data": test_data, "issue_data": issue_data}

    report_title = reportcreator.masterReportWriter(report_data)

    return showReport(report_title)

def serviceReport():

    service_id = request.args.get('service_id')

    service_data = reportConnection.getServiceData(service_id)
    component_list = []

    for asset_id in service_data['_source']['service_stuff']['service_has_assets']:
        issue_data = reportConnection.getIssuesForAsset(asset_id)
        asset_data = reportConnection.getAssetData(asset_id)
        component_list.append({"asset_name": asset_data['_source']['asset_stuff']['asset_name'], "issue_data": issue_data})

    report_data = {"service_name": service_data['_source']['service_stuff']['service_name'], "components": component_list}
    report_data.update({"report_type": "service"})

    report_title = reportcreator.masterReportWriter(report_data)

    return showReport(report_title)

def assetReport():

    asset_id = request.args.get('asset_id')

    asset_data = reportConnection.getAssetData(asset_id)
    test_data = reportConnection.getTestsForAsset(asset_id)
    issue_data = reportConnection.getIssuesForAsset(asset_id)

    report_data = {"report_type": "asset", "asset_data": asset_data, "test_data": test_data, "issue_data": issue_data}

    report_title = reportcreator.masterReportWriter(report_data)

    return showReport(report_title)
