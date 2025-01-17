def get_tab(lang: str):
    if lang == 'fr':
        return i18n_FR
    if lang == 'nl':
        return i18n_NL
    return i18n_EN

def get_i18n(lang: str, key: str):
    tab = get_tab(lang)
    text = key
    try:
        text = tab[key]
    except KeyError:
        pass
    return text

i18n_FR = {
    "WRONG_CREDENTIALS": "Le mot de passe ou le nom d'utilisateur est incorrect.",
    "MISSING_CREDENTIAL": "Merci de renseigner le nom d'utilisateur et le mot de passe.",
    "EMAIL_SENT": "L'email a bien été envoyé."
}

i18n_NL = {
    "WRONG_CREDENTIALS": "Het wachtwoord of de gebruikersnaam is onjuist.",
    "MISSING_CREDENTIAL": "Gelieve de gebruikersnaam en het wachtwoord in te vullen.",
    "EMAIL_SENT": "De e-mail is succesvol verzonden.",

}

i18n_EN = {
    "WRONG_CREDENTIALS": "The username or password is incorrect.",
    "MISSING_CREDENTIAL": "Please enter the username and password.",
    "EMAIL_SENT": "The email has been sent successfully.",

}