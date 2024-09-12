
import re

def sanitize_mail(email_field):
    # Use regular expression to split on common separators (slash, comma, semicolon, whitespace)
    emails = re.split(r'[;/,\s]\s*', email_field)
    # Filter out empty strings in case of multiple separators and strip spaces, then convert to lower case
    cleaned_emails = [email.strip().lower() for email in emails if email.strip()]
    # Return the first email if there are any, otherwise return an empty string
    return cleaned_emails[0] if cleaned_emails else ''