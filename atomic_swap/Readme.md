# Atomic swap (with Ethereum)

Atomic Swap is a trade between two users of different cryptocurrencies, wich does not require third party to be involved.
Cross-chain swaps require each party to pay into a contract transaction, one contract for each blockchain.
The contracts contain an output that is spendable by either party, but the rules required for redemption are different for each party involved.

Illustration for the steps each party performs and the transfer of data between each party.

<img src="img/workflow.svg" width="100%" height=650 />

Detailed algorithm description [Decred](https://github.com/decred/atomicswap)

## How to test

1. Install `geth`
For OSX:

`brew tap ethereum/ethereum`

`brew install ethereum`

2. Install [Mist](https://github.com/ethereum/mist/releases)
3. Create directory for new private chain

`mkdir myChain`

`cd myChain`

4. Create genesis config and data directory

`touch myGenesis.json`

Specify chain params in the file. In `alloc` section specify testing accounts you are already have access to.

    {
        "config": {
            "chainId": 1114,
            "homesteadBlock": 0,
            "eip155Block": 0,
            "eip158Block": 0,
            "byzantiumBlock": 0
        },
        "difficulty": "400",
        "gasLimit": "2000000",
        "alloc": {
            "965f548064b53848af13059e553fc1f39ffea766": { 
                "balance": "100000000000000000000000" 
            },
            "15c096476dafa698862f39c009aa0d5cf6d91cba": { 
                "balance": "120000000000000000000000" 
            }
        }
    }
    
`mkdir dataDir`

5. Init new chain

`geth --datadir ./dataDir init ./privateGenesis.json`

6. Run local ethereum node

`geth --ws  --wsaddr "0.0.0.0" --wsapi "eth,net,web3,admin,shh" --wsorigins "*" --mine --minerthreads=1 --datadir ./dataDir/ --networkid 1114`

7. Run Mist pointing it to the local network

`open '/Applications/Ethereum Wallet.app' --args --node-networkid 1114 --rpc http://127.0.0.1:8545`

8. Deploy solidity contract from `./eth/AtomicSwap.sol` from mist

Initiator (on Ethereum side):

- Run `python3 ./utils/secret_gen.py`.

The output should looks as follows:

    Secret: 
    a3e1653c5816f03129483f18a39fd411c38c97c1aed64a2064035382d91a6131
    Hashed secret: 
    98a4616057d0c56d680195014231975e4b992c74c1cf6d23c97af350458894e2

- When the contract is deployed, call its `initiate()` method passing hashed secret and redemption delay (In miliseconds) to it.

Initiator (on Encry side):

- Run `python3 ./utils/secret_gen.py`.

The output should looks as follows:

    Secret: 
    a3e1653c5816f03129483f18a39fd411c38c97c1aed64a2064035382d91a6131
    Hashed secret: 
    98a4616057d0c56d680195014231975e4b992c74c1cf6d23c97af350458894e2

- Run `python3 ./utils/atomic_swap_contract.py <hashed_secret> <participant_addr_p2sh> <amount> <redemption_deadline> <token_id_hex>[OPTIONAL]`.

Example: `python3 ./atomic_swap_contract.py 98a4616057d0c56d680195014231975e4b992c74c1cf6d23c97af350458894e2 ABoqbCE7zuLMxd7nTej7xyP2x23xrKcKDopnVW59b1NNXdrnRqX 10 1546169038`

- Create scripted transaction from EncryWallet pasting the output of the pevious command to the `contract` field.

Participant (on Ethereum side)

- When the contract is deployed, call its `participate()` method passing hashed secret, redemption delay (In miliseconds) and initiator's address to it.

Participant (on Encry side):

- Run `python3 ./utils/atomic_swap_contract.py <hashed_secret> <participant_addr_p2sh> <amount> <redemption_deadline> <token_id_hex>[OPTIONAL]`.

Example: `python3 ./atomic_swap_contract.py 98a4616057d0c56d680195014231975e4b992c74c1cf6d23c97af350458894e2 ABoqbCE7zuLMxd7nTej7xyP2x23xrKcKDopnVW59b1NNXdrnRqX 10 1546169038`

- Create scripted transaction from EncryWallet pasting the output of the pevious command to the `contract` field.

Done! Contracts are deployed, now you are to simply stick to the atomic swap protocol described above.

#### Troublesooting

Geth may fail to start mining if etherbase account not specified. To specify it attach to running geth node `geth attach ./dataDir/geth.ipc`, check whether you have active accounts `eth.accounts` and run `miner.setEtherbase(web3.eth.accounts[0])`.
