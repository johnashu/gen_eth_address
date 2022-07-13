from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
import threading
from includes.config import *


def gen_address(
    word: str, thread: threading, start: bool = True, end: bool = True
) -> None:
    found = []
    count = 1
    addresses_count = 1

    log.info(f"Starting New Run in thread {thread}..\n")
    while True:
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[
            1:
        ]
        addr = keccak_256(public_key).digest()[-20:].hex()
        f = False
        if addr.lower().startswith(word) and start and addr not in found:
            f = True
            t = "Start"

        if addr.lower().endswith(word) and end and addr not in found:
            f = True
            t = "End"

        if f:
            found.append(addr)
            log.info(
                f"\nThread:{thread}\nFound number {addresses_count}\nAddresses checked: {count}\nWord found : {word}\nprivate_key: {private_key.hex()}\neth addr: 0x{addr}\nType: {t}"
            )
            addresses_count += 1
        count += 1


def run(words):
    threads = list()
    for i, x in enumerate(words):
        x = threading.Thread(target=gen_address, args=(x, i + 1))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()


# 3 letters will generate instantly..
# 4-5 letters - approx 10-30 seconds
# 6 + - ?????? - Depends on CPU but > 1 hour..
words = "abcdef", "123456", "abcde", "12345"
run(words)
