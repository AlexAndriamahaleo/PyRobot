from django.conf import settings


def validate_ai_script(text):
    """
    Verify input AI script. False if the script contains not allowed keywords like "import", "exec"
    :param text: String
    :return: True/False
    """
    if text.strip() == "":
        return False
    for line in text.splitlines():
        if any(kw in line for kw in settings.NOT_ALLOWED_KW):
            return False
    return True
