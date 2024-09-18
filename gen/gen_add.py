
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
import threading
from includes.config import *
from eth_utils import to_checksum_address

def gen_address(
    word: str,
    thread: int,
    start: bool = True,
    end: bool = True,
    num_to_find: int = 10,
    save_as_json: bool = True,
    fn: str = "found",
) -> None:
    found = {}
    count = 1
    addresses_count = 1

    log.info(f"Starting New Run in thread {thread}..\n")
    while True:
        if num_to_find <= addresses_count:
            if save_as_json:
                save_json(fn, found)
            return found
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]
        addr_hex = addr.hex()
        
        # Convert to checksum address (mixed case)
        checksum_addr = to_checksum_address(addr_hex)
        
        s = False
        e = False
        if checksum_addr[2:].startswith(word) and start and checksum_addr not in found.keys():
            s = True
            t = "Start"

        if checksum_addr[2:].endswith(word) and end and checksum_addr not in found.keys():
            e = True
            t = "End"

        f = False
        if start and end:
            f = s and e
        elif start:
            f = s
        elif end:
            f = e

        if f:
            found[checksum_addr] = f"0x{private_key.hex()}"
            log.info(
                f"\nThread:{thread}\nFound number {addresses_count}\nAddresses checked: {count}\nWord found : {word}\nprivate_key: {private_key.hex()}\neth addr: {checksum_addr}\nType: {t}"
            )
            addresses_count += 1
        
        if count % 10000 == 0:
            print(f"Checked {count} addresses")
        count += 1