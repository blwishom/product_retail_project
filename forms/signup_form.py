
class SignUpForm:
    def __init__(self, data):
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.email = data.get('email', '')
        self.password = data.get('password', '')
        self.confirm_password = data.get('confirm_password', '')

    def validate(self):
        errors = []

        if not self.first_name:
            errors.append('Please enter first name.')

        if not self.last_name:
            errors.append('Please enter last name.')

        if not self.email:
            errors.append('Please enter an email.')
        elif not self.is_valid_email(self.email):
            errors.append('Invalid email.')

        if not self.password:
            errors.append('Password is required.')
        elif len(self.password) < 5:
            errors.append('Please make password 5 characters or longer.')

        if self.password != self.confirm_password:
            errors.append('Passwords do not match!')

        return errors

    def is_valid_email(self, email):
        if '@' not in email or '.' not in email:
            return False

        email_split = email.split('@')
        if len(parts) != 2:
            return False

        return True
