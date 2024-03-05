errors = {
    "faucet": {
        "invalid-signature": "Invalid signature",
        "invalid-timestamp": "Invalid timestamp",
        "invalid-message": "Invalid message",
        "invalid-prefix": "Invalid prefix",
        "try-later": "Please try later",
    }
}

# Return error message
def abort(scope, message):
    code = scope.replace("-", "_") + "_" + message.replace("-", "_")

    try:
        error_message = errors[scope][message]
    except Exception:
        error_message = "Unknown error"

    return {
        "error": {
            "message": error_message,
            "code": code
        },
        "data": {}
    }
