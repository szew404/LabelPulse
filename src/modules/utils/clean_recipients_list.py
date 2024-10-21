def clean_recipients(recipients: str) -> list[str]:

    # Split each recipient email address
    re_splitted = recipients.split("\n")
    return [recipient.strip() for recipient in re_splitted]
