from flask import Flask, render_template, request, redirect, url_for, flash
from elasticstuff import login, logger
import flask_login
import otp

user_instance = login.User()
userConnection = login.Login()
logger_instance = logger.Logger()
one_time_code = otp.OneTimePassword()

def user_loader(username):
    user_check = userConnection.checkUserExists(username)
    if user_check == False:
        return

    else:
        user = user_instance
        user.id = username
        if user.is_authenticated:
            return user

def login():
    return render_template('login.html')

def loginapi():
    username = request.form['username']
    password = request.form['password']
    user_otp = request.form['user_otp']
    try:
        otp_values = userConnection.checkForOtp(username)
        has_otp = otp_values['user_otp']
        user_secret = otp_values['secret']
        password_success_log_in = userConnection.comparePassword(username, password)
        otp_success_log_in = one_time_code.verifyOTP(user_otp, user_secret)
    except:
        password_success_log_in = False
        otp_success_log_in = False

    try:
        if has_otp == False and password_success_log_in:
            user = user_instance
            user.id = username
            logger_instance.createLog({"login_event": "user not registered for otp"}, user.id)
            flash("otp not onboarded")
            return onboardotp()

        elif has_otp == True and password_success_log_in and otp_success_log_in:
            user = user_instance
            user.id = username
            flask_login.login_user(user)
            user_role = userConnection.getPermissions(username)
            user.role = user_role
            logger_instance.createLog({"login_event": "successful login"}, user.id)
            return redirect(url_for('viewassets'))

        else:
            flash("login failed")
            logger_instance.createLog({"login_event": "login failed"}, username)
            return redirect(url_for('login'))

    except:
        flash("login failed")
        logger_instance.createLog({"login_event": "login failed"}, username)
        return redirect(url_for('login'))

def onboardotp():
    otp_values = userConnection.checkForOtp(user_instance.get_id())
    has_otp = otp_values['user_otp']
    user_secret = otp_values['secret']
    if has_otp:
        flash("otp already registered")
        return redirect(url_for('login'))
    else:
        otp_return = one_time_code.onboardUser(user_instance.get_id())
        userConnection.updateOtpSecret(user_instance.get_id(), otp_return['secret'])
        return render_template('onboardotp.html')


def onboardotpapi():
    one_time_code.overwriteOTP()
    user_otp = request.form['user_otp']
    secret_token = userConnection.getUserSecret(user_instance.get_id())
    try:
        otp_success = one_time_code.verifyOTP(user_otp, secret_token)
    except:
        otp_success == False

    if otp_success:
        userConnection.updateOtpStatus(user_instance.get_id())
        flash("success")
        logger_instance.createLog({"registration_event": "user registered for otp"}, user_instance.get_id())
        return redirect(url_for('login'))
    else:
        flash("Something went wrong")
        return redirect(url_for('login'))


def changepassword():
    return render_template('changepassword.html')

def changepasswordapi():

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    new_password_repeat = request.form['new_password_repeat']

    if new_password != new_password_repeat:
        flash("!passwords dont match!")
        logger_instance.createLog({"password_event": "failed password update attempt"}, user_instance.get_id())
        return redirect(url_for('changepassword'))

    else:
        username = user_instance.get_id()
        correct_existing_password = userConnection.comparePassword(username, old_password)

        if not correct_existing_password:
            flash("!incorrect existing password!")
            logger_instance.createLog({"password_event": "failed password update attempt"}, user_instance.get_id())
            return redirect(url_for('changepassword'))

        else:
            userConnection.updateUser(username, new_password)
            flash("success")
            logger_instance.createLog({"password_event": "user updated password"}, user_instance.get_id())
            return render_template('viewassets.html')
