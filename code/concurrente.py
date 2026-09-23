import multiprocessing,time


def print_numbers():
    for i in range(1, 6):
        print(f"numero: {i}")
        time.sleep(1)


def print_letters():
    for letter in "ABCDE":
        print(f"letter: {letter}")
        time.sleep(1)


if __name__ == "__main__":
    p1 = multiprocessing.process(target=print_numbers)
    p2 = multiprocessing.process(target=print_letters)

    p1.start()
    p2.start()

    p1.join()
    p2.join()