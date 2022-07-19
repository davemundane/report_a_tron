import pyotp
import qrcode
import config
import secrets


class OneTimePassword:

    def __init__(self):
        pass

    def onboardUser(self, username):

        secret_token = pyotp.random_base32()
        uri = pyotp.totp.TOTP(secret_token).provisioning_uri(name=username, issuer_name="Report-a-Tron")
        img = qrcode.make(uri)
        img.save("static/qr.png")

        return {"success": True, "secret": secret_token}

    def verifyOTP(self, user_otp, user_secret):

        try:
            value = pyotp.TOTP(user_secret).verify(user_otp)
            return value

        except:
            return False


    def overwriteOTP(self):

        uri = "https://haveibeenpwnd.com"
        img = qrcode.make(uri)
        img.save("static/qr.png")
