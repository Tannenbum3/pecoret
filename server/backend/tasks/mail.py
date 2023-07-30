from backend import emails


def send_password_reset_mail(context, to):
    email = emails.PasswordResetEmail(context)
    if not isinstance(to, list):
        to = [to]
    email.send(to)
    return True


def send_activation_mail(context, to):
    email = emails.ActivationEmail(context)
    if not isinstance(to, list):
        to = [to]
    email.send(to)
    return True


def send_advisory_shared_mail(context, to):
    email = emails.AdvisorySharedEmail(context)
    if not isinstance(to, list):
        to = [to]
    email.send(to)
    return True


def send_new_critical_finding_mail(context, to):
    email = emails.NewCriticalFindingEmail(context)
    if not isinstance(to, list):
        to = [to]
    email.send(to)
    return True
