TAXONOMY = {
    "ios_update": [
        "ios", "update", "upgrade", "downgrade",
        "install ios", "ios update", "software update"
    ],

    "device_hardware": [
        "screen", "display", "battery", "charging",
        "charger", "speaker", "camera", "broken",
        "damage", "repair", "keyboard"
    ],

    "connectivity": [
        "wifi", "wi-fi", "bluetooth", "cellular",
        "network", "internet", "signal", "connection"
    ],

    "account_access": [
        "apple id", "appleid", "icloud", "password",
        "login", "log in", "sign in", "locked account"
    ],

    "billing_subscription": [
        "charged", "charge", "billing", "refund",
        "payment", "subscription", "subscribed",
        "purchase", "money"
    ],

    "app_service": [
        "app", "facetime", "safari", "apple music",
        "itunes", "notification", "crash", "game",
        "apple tv"
    ],

    "device_performance": [
        "slow", "freezes", "freezing", "freeze",
        "boot loop", "glitch", "lag", "hang", "stuck"
    ],

    "other": []
}


def weak_label(text):
    """Assign a simple weak label using keyword matches."""
    text = str(text).lower()

    scores = {}

    for intent, keywords in TAXONOMY.items():
        scores[intent] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "other"

    return best_intent