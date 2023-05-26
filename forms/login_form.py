from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

class LoginForm:
    def __init__(self, request):
        self.request = request
        self.email = None
        self.password = None

    def validate_customer(self):
        self.email = self.request.form.get('email')
        self.password = self.request.form.get('password')

        if not self.email:
            return False
        if not self.password:
            return False

        return True

    def get_errors(self):
        errors = []

        if not self.email:
            errors.append('Email is required.')

        if not self.password:
            errors.append('Password is required.')

        return errors
