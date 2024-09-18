import threading
from gen.gen_add import gen_address


def run(words, **kw):
    threads = list()
    for i, x in enumerate(words):
        x = threading.Thread(target=gen_address, args=(x, i + 1), kwargs=kw)
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # 3 letters will generate instantly..
    # 4-5 letters - approx 10-30 seconds
    # 6 + - ?????? - Depends on CPU but > 1 hour..
    words = "C02", 
    run(words, start=False, end=True, save_as_json=True, num_to_find=10)
