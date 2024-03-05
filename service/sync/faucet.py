from requests import request
from ..clients import Bitcoin
from ..models import Request
from pony import orm
from . import utils
import config

@orm.db_session
def process_faucet():
    utils.log_message("Processing faucet requests")

    client = Bitcoin(config.endpoint)
    processed = []
    outputs = {}

    # Withdrawals are locked for update
    requests = Request.select(
        lambda w: w.txid is None
    ).for_update().limit(100)

    for faucet_request in requests:
        # Add address to outputs list if missing
        if faucet_request.address not in outputs:
            outputs[faucet_request.address] = 0

        outputs[faucet_request.address] += faucet_request.amount
        processed.append(faucet_request)

    # There is no withdrawals to process
    if len(processed) == 0:
        return

    # Convert Decimal to float before sending request to rpc
    for address in outputs:
        outputs[address] = float(round(outputs[address], 8))

    # Make transfer request via rpc
    data = client.make_request("transfermany", [
        config.faucet_token, outputs
    ])

    # Make sure to rollback if rpc call failed
    if data["error"]:
        orm.rollback()
        return

    txid = data["result"]
    total = 0

    # Set txid for withdrawals
    for faucet_request in processed:
        faucet_request.txid = txid
        total += faucet_request.amount

        utils.log_message(
            f"Sent {float(faucet_request.amount)} to {faucet_request.address}"
        )

    utils.log_message(f"Sent {total} in total in {txid}")
