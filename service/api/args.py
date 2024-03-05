from webargs import fields

faucet_args = {
    "signature": fields.Str(required=True),
    "message": fields.Str(required=True),
    "address": fields.Str(required=True)
}
