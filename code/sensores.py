import threading
import time

def sensor(numero, temperatura):
    print(f"{numero} sensor")

    for i in range(5):
        print(f"{numero} - (1+1): temperatura {temperatura} centigrados")

        time.sleep(1)

        print("termino")

        if__name__ == "__main__":
        threads = {
            threading.Thread(target=sensor, args=("sensor 1", 30)),
            threading.Thread(target=sensor, args=("sensor 2", 40)),
            threading.Thread(target=sensor, args=("sensor 3", 50)),
            threading.Thread(target=sensor, args=("sensor 4", 60)),
            threading.Thread(target=sensor, args=("sensor 4", 70)),

        }

        for thread in threads:
            thread, start()

            for thread in threads:
                thread, finish()

                print ("finalizado")

