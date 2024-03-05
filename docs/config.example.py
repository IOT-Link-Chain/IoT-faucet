secret = "Lorem ipsum dor sit amet"
host = "0.0.0.0"
debug = True
port = 4321

proxy_fix = False
x_for = 1

endpoint = "http://rpcuser:rpcpassword@localhost:33440/wallet/faucet"
auth_prefix = "Faucet"
auth_minutes = 2

faucet_token = "TOKEN"
faucet_amount = 1

db = {
    "provider": "sqlite",
    "filename": "../service.db",
    "create_db": True
}
