import markdown
import datetime
from os import path
import os

style = '<style>body {	font-family: Tahoma, Geneva, sans-serif; word-break: break-word;} .body_container { width: 70%; margin-left: 15%;} tr:nth-child(even) {background-color: #f2f2f2;} code { display: inline-block; overflow: visible; padding-left: 10px; padding-bottom: 10px; } .blue_header_top {width: 100%; height: 30px; background-color: #3D5588;} .blue_header_middle {width: 100%; height: 10px; background-color: #779EC2; margin-bottom: 20px;} .blue_header_low {width: 100%; height: 2px; background-color: #779EC2; margin-bottom: 40px; margin-top: 30px;} p.the_header { font-size: 50px; padding-top: 5px;	padding-bottom: 25px; margin: 0; text-align: center; } p.level_two {	font-size: 30px;	padding-top: 5px;	padding-bottom: 5px;	margin: 0;} p.level_three {	font-size: 20px;	padding-top: 10px;	padding-bottom: 5px;	margin: 0;} p.general {	font-size: 14px;	padding-top: 4px; padding-bottom: 4px;	margin: 0;} .tableb {  width: 100%;  margin-top: 30px; margin-bottom: 30px; border: solid 1px #394045;    border-collapse: collapse;    border-spacing: 0;	padding-top: 8px; table-layout: fixed; } .tableb caption {	text-align: center;	font-size: 20px;	padding-bottom: 20px;	padding-top: 20px;} .tableb thead th {  height: 40px; background-color: #3D5588;    border: solid 1px #394045;    color: #fff;    padding: 10px; } .tableb tbody td {    border: solid 1px #394045;    color: #333;    padding: 10px;	font-size: 12px;} .tableb tr { height: 40px; } .left_col { text-align: right; } .other_col { text-align: left; } p.appendix_code { font-size: 14px;	padding: 10px; margin: 0; background-color: #f6f8fa; border-radius: 3px; white-space: pre-wrap; }  .tablec {  width: 50%;  margin: auto; border: solid 1px #394045; border-collapse: collapse;    border-spacing: 0;	padding-top: 8px; table-layout: fixed; } .tablec caption {	text-align: center;	font-size: 20px;	padding-bottom: 20px;	padding-top: 20px;} .tablec thead th {  height: 40px; background-color: #3D5588;    border: solid 1px #394045;    color: #fff;    padding: 10px; } .tablec tbody td {    border: solid 1px #394045;    color: #333;    padding: 10px;	font-size: 12px;} .tablec tr { height: 40px; }</style>'

new_line = "\n"
double_new_line = "\n\n"

def get_date():
    return datetime.datetime.today().strftime('%d-%m-%y')

def masterReportWriter(report_data):

    if report_data['report_type'] == "service":

        return_data = writeServiceReport(report_data)

    elif report_data['report_type'] == "test":

        return_data = writeTestReport(report_data)

    elif report_data['report_type'] == "asset":

        return_data = writeAssetReport(report_data)

    html_data = return_data['html_data']
    report_title = return_data['report_title']

    #htmlpath = "//templates//thereport.html"
    htmlpath = "//templates//" + report_title
    abspath = path.abspath(__file__)
    dirname = path.dirname(abspath)
    html_file = str(dirname) + htmlpath

    with open(html_file, "w") as outfile:
        outfile.write(html_data)

    outfile.close()

    return report_title

def writeAssetReport(report_data):

    report_title = report_data['asset_data']['_source']['asset_stuff']['asset_name'] + "_Asset-Security-Report_" + get_date() + ".html"

    summary = "This report details the tests conducted for the asset named " + report_data['asset_data']['_source']['asset_stuff']['asset_name'] + ", along with associated findings arising from those tests. Issues may be raised as a result of a number of security assessments over time, whether a complete risk assessment, or a partial review of a minor change to the service."

    html_data = writeHeader(report_data['asset_data']['_source']['asset_stuff']['asset_name'] + "_Asset-Security-Report_" + get_date(), summary)

    if report_data['test_data']:

        html_data += """
        <p class="level_two">Summary of Completed Testing</p>
        <table class="tableb"><thead><tr>
        <th width="50%" scope="col" class="other_col">Test Type</th>
        <th width="50%" scope="col" class="other_col">Test Date</th>
        </tr></thead><tbody>
        """

        for test in report_data['test_data']:
            html_data += writeTestTable(test)

        html_data += """
        </tbody></table>
        <div class="blue_header_low"></div>
        """

    else:
        html_data += """
        <p class="level_two">There have been no tests conducted for """ + report_data['asset_data']['_source']['asset_stuff']['asset_name'] + """
        </p>
        <div class="blue_header_low"></div>
        """


    if report_data['issue_data']: #[0]['_source']['issue_stuff']:

        html_data += """
        <p class="level_two">Issue Summary
        </p>
        <table class="tableb"><thead><tr>
        <th width="20%" scope="col" class="other_col">Issue Reference</th>
        <th width="40%" scope="col" class="other_col">Issue Title</th>
        <th width="20%" scope="col" class="other_col">Risk Rating</th>
        <th width="20%" scope="col" class="other_col">Status</th>
        </tr></thead><tbody>
        """

        for issue in report_data['issue_data']:
            html_data += writeIssueTable(issue)

        html_data += """
        </tbody></table>
        <div class="blue_header_low"></div>
        """

    else:
        html_data += """
        <p class="level_two">There are no issues to report for """ + report_data['asset_data']['_source']['asset_stuff']['asset_name'] + """
        </p>
        <div class="blue_header_low"></div>
        """

    if report_data['issue_data']:

        html_data += """
        <p class="level_two">Technical Findings</p>
        """

        for issue in report_data['issue_data']:
            html_data += writeTechnicalTable(issue)

        html_data += """
        <div class="blue_header_low"></div>
        """

    html_data += """
    <p class="level_two">Appendix</p>
    """

    html_data += writeReportFooter()

    return {"html_data": html_data, "report_title": report_title}

def writeTestReport(report_data):

    report_title = report_data['asset_data']['_source']['asset_stuff']['asset_name'] + "_" + report_data['test_data']['_source']['test_stuff']['test_type'] + "_" + get_date() + ".html"

    html_data = writeHeader(report_data['asset_data']['_source']['asset_stuff']['asset_name'] + "_" + report_data['test_data']['_source']['test_stuff']['test_type'] + "_" + report_data['test_data']['_source']['test_stuff']['test_date'], report_data['test_data']['_source']['test_stuff']['test_exec_summary'])

    if report_data['issue_data']: #[0]['_source']['issue_stuff']:

        html_data += """
        <p class="level_two">Issue Summary
        </p>
        <table class="tableb"><thead><tr>
        <th width="20%" scope="col" class="other_col">Issue Reference</th>
        <th width="40%" scope="col" class="other_col">Issue Title</th>
        <th width="20%" scope="col" class="other_col">Risk Rating</th>
        <th width="20%" scope="col" class="other_col">Status</th>
        </tr></thead><tbody>
        """

        for issue in report_data['issue_data']:
            html_data += writeIssueTable(issue)

        html_data += """
        </tbody></table>
        <div class="blue_header_low"></div>
        """

    else:
        html_data += """
        <p class="level_two">There are no issues to report for """ + report_data['asset_data']['_source']['asset_stuff']['asset_name'] + """
        </p>
        <div class="blue_header_low"></div>
        """

    if report_data['issue_data']:

        html_data += """
        <p class="level_two">Technical Findings</p>
        """

        for issue in report_data['issue_data']:
            html_data += writeTechnicalTable(issue)

        html_data += """
        <div class="blue_header_low"></div>
        """

    html_data += """
    <p class="level_two">Appendix</p>
    """

    for issue in report_data['issue_data']:

        html_data += writeIssueDetails(issue)

    html_data += """
    <div class="blue_header_low"></div>
    """

    html_data += writeReportFooter()

    return {"html_data": html_data, "report_title": report_title}


def writeServiceReport(report_data):

    summary = "This report details the security findings related to the Service above. Services can be made of many components including mutiple individual applications and services provided by third party vendors. The report will include a summary and detailed findings for each of the application or third party components listed as comprising the service in ICS's systems. Should any of these be incorrect, please inform ICS."

    report_title = report_data['service_name'] + "_Service-Security-Report_" +  get_date() + ".html"

    html_data = writeHeader(report_data['service_name'] + "_Service-Security-Report_" +  get_date(), summary)

    for asset in report_data['components']:
        if asset['issue_data']:

            html_data += """
            <p class="level_two">Issue Summary for """ + asset['asset_name'] + """
            </p>
            <table class="tableb"><thead><tr>
            <th width="20%" scope="col" class="other_col">Issue Reference</th>
            <th width="40%" scope="col" class="other_col">Issue Title</th>
            <th width="20%" scope="col" class="other_col">Risk Rating</th>
            <th width="20%" scope="col" class="other_col">Status</th>
            </tr></thead><tbody>
            """

            for issue in asset['issue_data']:
                html_data += writeIssueTable(issue)

            html_data += """
            </tbody></table>
            <div class="blue_header_low"></div>
            """

        else:
            html_data += """
            <p class="level_two">There are no issues to report for """ + asset['asset_name'] + """
            </p>
            <div class="blue_header_low"></div>
            """

    for asset in report_data['components']:
        if asset['issue_data']:

            html_data += """
            <p class="level_two">Technical Findings for """ + asset['asset_name'] + """
            </p>
            """

            for issue in asset['issue_data']:
                html_data += writeTechnicalTable(issue)


            html_data += """
            <div class="blue_header_low"></div>
            """

    html_data += """
    <p class="level_two">Appendix</p>
    """

    html_data += writeReportFooter()

    return {"html_data": html_data, "report_title": report_title}

def writeHeader(report_title, report_summary):

    return """
    <!DOCTYPE html><html lang="en"<head><title>AppSec Report</title>""" + style + """
    <div class="blue_header_top"></div>
    <div class="blue_header_middle"></div>
    <p class="the_header">""" + report_title + """</p>
    </head><body><div class="body_container">
    <p class="general">""" + report_summary + """</p>
    <div class="blue_header_low"></div>
    """

def writeTestTable(test):

    html_data = ""

    test_type = test['_source']['test_stuff']['test_type']
    test_date = test['_source']['test_stuff']['test_date']

    html_data += """
    <tr>
    <td>""" + test_type + """</td>
    <td>""" + test_date + """</td>
    </tr>
    """

    return html_data

def writeHeaderTable(report_subject, base_location, test_limitations):

    return """
    <table class="tablec"><thead><tr>
    <th width="50%" scope="col" class="left_col">Value</th>
    <th width="50%" scope="col" class="other_col">Detail</th>
    </tr></thead><tbody>
    <tr>
    <td class="left_col">Report Subject</td>
    <td class="other_col">""" + report_subject + """
    </td>
    </tr>
    <tr>
    <td class="left_col">Location</td>
    <td class="other_col">""" + base_location + """
    </td>
    </tr>
    <tr>
    <td class="left_col">Limitations</td>
    <td class="other_col">""" + test_limitations + """
    </td>
    </tr>
    </tbody></table>
    <div class="blue_header_low"></div>
    """

def writeReportFooter():

    return """
    <p class="level_three">Remediation Guidelines</p>
    <p class="general">The table below indicates the timelines agreed by the Board of Directors for the remediation of security issues. Any issues that cannot be resolved within the timeframe below must be risk accepted by the Business Owner of the service. Please confer with ICS on the most appropriate action for any issues listed and where any fixes are applied, please discuss these with ICS to ensure they are suitable for addressing the risk identified. Should you feel this report contains any inaccuracies, please do not hesitate to contact ICS to discuss the contents.</p>
    <div class="blue_header_low"></div>
    <table class="tablec"><thead><tr>
    <th width="50%" scope="col" class="left_col">Issue Rating</th>
    <th width="50%" scope="col" class="other_col">Remediation Time</th>
    </tr></thead><tbody>
    <tr>
    <td class="left_col">Critical</td>
    <td class="other_col">7 Days</td>
    </tr>
    <tr>
    <td class="left_col">High</td>
    <td class="other_col">30 Days</td>
    </tr>
    <tr>
    <td class="left_col">Medium</td>
    <td class="other_col">60 Days</td>
    </tr>
    <tr>
    <td class="left_col">Low</td>
    <td class="other_col">180 Days</td>
    </tr>
    </tbody></table>
    <div class="blue_header_low"></div>
    </div>
    <div class="blue_header_top"></div>
    <div class="blue_header_middle"></div>
    </body></html>
    """

def writeIssueTable(issue):

    html_data = ""

    issueTitle = issue['_source']['issue_stuff']['issue_title']
    issueLocation = issue['_source']['issue_stuff']['issue_location']
    issueDescription = issue['_source']['issue_stuff']['issue_description']
    issueRemediation = issue['_source']['issue_stuff']['issue_remediation']
    issueRisk = issue['_source']['issue_stuff']['issue_risk_rating']
    issueImpact = issue['_source']['issue_stuff']['issue_risk_impact']
    issueLikelihood = issue['_source']['issue_stuff']['issue_risk_likelihood']
    issueStatus = issue['_source']['issue_stuff']['issue_status']
    issueDetails = issue['_source']['issue_stuff']['issue_details']
    issueID = issue['_id']

    html_data += """
    <tr>
    <td>""" + issueID + """</td>
    <td>""" + issueTitle + """</td>
    <td>""" + issueRisk + """</td>
    <td>""" + issueStatus + """</td>
    </tr>
    """

    return html_data

def writeTechnicalTable(issue):

    html_data = ""

    issueTitle = issue['_source']['issue_stuff']['issue_title']
    issueLocation = issue['_source']['issue_stuff']['issue_location']
    issueDescription = issue['_source']['issue_stuff']['issue_description']
    issueRemediation = issue['_source']['issue_stuff']['issue_remediation']
    issueRisk = issue['_source']['issue_stuff']['issue_risk_rating']
    issueImpact = issue['_source']['issue_stuff']['issue_risk_impact']
    issueLikelihood = issue['_source']['issue_stuff']['issue_risk_likelihood']
    issueStatus = issue['_source']['issue_stuff']['issue_status']
    issueDetails = issue['_source']['issue_stuff']['issue_details']
    issueID = issue['_id']

    html_data += """
    <table class="tableb"><thead><tr>
    <th width="15%" scope="col" class="left_col"></th>
    <th width="85%" scope="col" class="other_col">""" + issueTitle + """</th>
    </tr></thead><tbody>
    <tr>
    <td class="left_col">Reference</td>
    <td class="other_col">""" + issueID + """</td>
    </tr>
    <tr>
    <td class="left_col">Status</td>
    <td class="other_col">""" + issueStatus + """</td>
    </tr>
    <tr>
    <td class="left_col">Issue Title</td>
    <td class="other_col">""" + issueTitle + """</td>
    </tr>
    <tr>
    <td class="left_col">Risk Rating</td>
    <td class="other_col">""" + issueRisk + """</td>
    </tr>
    <tr>
    <td class="left_col">Description</td>
    <td class="other_col">""" + issueDescription + """</td>
    </tr>
    <tr>
    <td class="left_col">Remediation</td>
    <td class="other_col">""" + issueRemediation + """</td>
    </tr>
    </tbody></table>
    """

    return html_data

def writeIssueDetails(issue):

    html_data = ""

    if issue['_source']['issue_stuff']['issue_details']:

        html_data += """
        <p class="level_three">""" + issue['_source']['issue_stuff']['issue_title'] + """ - """ + str(issue['_id']) + """</p>
        <p class="appendix_code">""" + issue['_source']['issue_stuff']['issue_details'] + """</p>
        """

    return html_data
