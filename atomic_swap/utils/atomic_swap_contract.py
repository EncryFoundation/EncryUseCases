import sys
from string import Template


DEFAULT_TOKEN_ID_HEX = "487291c237b68dd2ab213be6b5d1174666074a5afab772b600ea14e8285affab"


CONTRACT = Template("""
    contract (state: State, tx: Transaction, secret: Array[Byte]) = {
        let secretHash         = hex"$secret_hash_hex"
        let participantAddress = base58"$participant_address"
        let tokenId            = hex"$token_id_hex"
        let amount             = $amount
        let redemptionDeadline = $redemption_deadline // Timestamp
        sha256(secret) == secretHash && tx.outputs.exists(lamb (bx: Box) = if (let assetBx: AssetBox = bx) {
            assetBx.tokenId == tokenId &&
            assetBx.contractHash == participantAddress &&
            assetBx.amount >= amount
        } else false) || (sha256(secret) == secretHash && state.lastBlockTimestamp > redemptionDeadline)
    }
    """)


if __name__ == '__main__':
    args = sys.argv[1:]
    if (len(args) >= 4):
        secret_hash_hex = args[0]
        participant_address_hex = args[1]
        amount = args[2]
        redemption_deadline = args[3]
        
        try:
            token_id_hex = args[4]
        except IndexError:
            token_id_hex = DEFAULT_TOKEN_ID_HEX
        
        print(CONTRACT.substitute({
            "secret_hash_hex" : secret_hash_hex,
            "participant_address" : participant_address,
            "amount" : amount,
            "redemption_deadline" : redemption_deadline,
            "token_id_hex" : token_id_hex
        }))
    else:
        print("Usage: atomic_swap_contract.py <secret_hash_hex> <participant_address> <amount> <redemption_deadline> <token_id_hex>[OPTIONAL]")
        sys.exit()


