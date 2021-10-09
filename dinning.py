# Lab 1 40 % work

import queue
import random
import time
from flask import Flask, request
import threading
import requests

time_unit = 1

menu = [{
    "id": 1,
    "name": "pizza",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 2,
    "name": "salad",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": None
}, {
    "id": 4,
    "name": "Scallop Sashimi with Meyer Lemon Confit",
    "preparation-time": 32,
    "complexity": 3,
    "cooking-apparatus": None
}, {
    "id": 5,
    "name": "Island Duck with Mulberry Mustard",
    "preparation-time": 35,
    "complexity": 3,
    "cooking-apparatus": "oven"
}, {
    "id": 6,
    "name": "Waffles",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 7,
    "name": "Aubergine",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": None
}, {
    "id": 8,
    "name": "Lasagna",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 9,
    "name": "Burger",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": "oven"
}, {
    "id": 10,
    "name": "Gyros",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}]

table_state0 = 'being free'
table_state1 = 'waiting to make a order'
table_state2 = 'waiting for the order to be served'

tables_list = [{
    "id": 1,
    "state": table_state0,
    "order_id": None
}, {
    "id": 2,
    "state": table_state0,
    "order_id": None
}, {
    "id": 3,
    "state": table_state0,
    "order_id": None
}, {
    "id": 4,
    "state": table_state0,
    "order_id": None
}, {
    "id": 5,
    "state": table_state0,
    "order_id": None
}]

waiters = [{
    'id': 1,
    'name': 'Iura'
}, {
    'id': 2,
    'name': 'Irina'
}, {
    'id': 3,
    'name': 'Alexandra'
}, {
    'id': 4,
    'name': 'Alexei'
}]

orders = queue.Queue()
orders.join()
orders_bundle = []

app = Flask(__name__)
threads = []


@app.route('/distribution', methods=['POST'])
def distribution():
    order = request.get_json()
    print(f'Received order from kitchen. Order ID: {order["order_id"]}')
    return {'isSuccess': True}


class Waiter(threading.Thread):
    def __init__(self, data, *args, **kwargs):
        super(Waiter, self).__init__(*args, **kwargs)
        self.id = data['id']
        self.name = data['name']
        self.daemon = True

    def run(self):
        while True:
            self.search_order()

    def search_order(self):
        try:
            order = orders.get()
            orders.task_done()
            table_id = next((i for i, table in enumerate(tables_list) if table['id'] == order['table_id']), None)
            print(
                f'Taking the order with Id: {order["id"]} and items: {order["items"]}')
            tables_list[table_id]['state'] = table_state2
            payload = dict({
                'order_id': order['id'],
                'table_id': order['table_id'],
                'waiter_id': self.id,
                'items': order['items'],
            })

            time.sleep(random.randint(2, 4) * time_unit)
            # send order to kitchen
            requests.post('http://localhost:3030/order', json=payload, timeout=0.0000000001)

        except (queue.Empty, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            pass



class Costumers(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Costumers, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            time.sleep(1)
            self.create_order()

    @staticmethod
    def create_order():
        (table_id, table) = next(
            ((idx, table) for idx, table in enumerate(tables_list)), (None, None))
        if table_id is not None:
            food_choices = []
            for i in range(random.randint(1, 5)):
                choice = random.choice(menu)
                food_choices.append(choice['id'])
            neworder_id = int(random.randint(1, 10000) * random.randint(1, 10000))
            neworder = {
                'table_id': table['id'],
                'id': neworder_id,
                'items': food_choices,

            }
            orders.put(neworder)



def run_dinninghall_server():
    main_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False),daemon=True)
    threads.append(main_thread)
    costumer_thread = Costumers()
    threads.append(costumer_thread)
    for _, w in enumerate(waiters):
        waiter_thread = Waiter(w)
        threads.append(waiter_thread)
    for th in threads:
        th.start()
    for th in threads:
        th.join()


if __name__ == '__main__':
    run_dinninghall_server()
