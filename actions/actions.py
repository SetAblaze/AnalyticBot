# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import sys

class ActionCheckCurrency(Action):

    def name(self)-> Text:
        return "action_get_currency"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mon = tracker.get_slot('monetary')
        mon1 = tracker.get_slot('monetary1')
        mon2 = tracker.get_slot('monetary2')

        key = '7116a9ab2462d1fbd01568bc094eaafa'
        url_auth = 'https://currate.ru/api/?get' 
        url_tran = 'https://currate.ru/api/'

        valute_obs = {
            'рубль': 'RUB',
            'доллар': 'USD',
            'евро': 'EUR'
        }
        rub_valute = valute_obs['рубль']
        usd_valute = valute_obs['доллар']
        eur_valute = valute_obs['евро']

        params1 = {
            'get': 'rates',
            'pairs':  rub_valute + usd_valute,
            'key': key}
        params2 = {
            'get': 'rates',
            'pairs':  rub_valute + eur_valute,
            'key': key}
        params3 = {
            'get': 'rates',
            'pairs':  usd_valute + rub_valute,
            'key': key}
        params4 = {
            'get': 'rates',
            'pairs':  usd_valute + eur_valute,
            'key': key}
        params5 = {
            'get': 'rates',
            'pairs':  eur_valute + rub_valute,
            'key': key}
        params6 = {
            'get': 'rates',
            'pairs':  eur_valute + usd_valute,
            'key': key}
            

        r1 = requests.get(url_auth, params=params1)
        res1 = r1.json()
        r2 = requests.get(url_auth, params=params2)
        res2 = r2.json()
        r3 = requests.get(url_auth, params=params3)
        res3 = r3.json()
        r4 = requests.get(url_auth, params=params4)
        res4 = r4.json()
        r5 = requests.get(url_auth, params=params5)
        res5 = r5.json()
        r6 = requests.get(url_auth, params=params6)
        res6 = r6.json()
        

        sum_all_rub_usd = float(res1['data'][rub_valute + usd_valute])
        sum_all_rub_eur = float(res2['data'][rub_valute + eur_valute])
        sum_all_usd_rub = float(res3['data'][usd_valute + rub_valute])
        sum_all_usd_eur = float(res4['data'][usd_valute + eur_valute])
        #sum_all_eur_usd = float(res5['data'][eur_valute + usd_valute])
        #sum_all_eur_rub = float(res6['data'][eur_valute + rub_valute])


        #entities = tracker.latest_message['entities']
       
        if mon == 'Рубля' or mon == 'Рубль' or mon == 'рубля' or mon == "рубль":
            response = """Текущий курс {} к {}: {}, к {}: {}""".format(mon, "Доллару", sum_all_rub_usd, "Евро", sum_all_rub_eur)
        if mon == 'Доллара' or mon == 'Доллар' or mon == 'доллара' or mon == 'доллар':
            response = """Текущий курс {} к {}: {}, к {}: {}""".format(mon, "Рублю", sum_all_usd_rub, "Евро", sum_all_usd_eur) 
     
        
        if mon1 == 'рубль' or mon1 == 'рубля' and mon2 == 'доллару' or mon2 == 'доллар':
            response = """Текущий курс {} к {}: {}""".format(mon1, mon2, sum_all_rub_usd)
        if mon1 == 'доллар' or mon1 == 'доллара' and mon2 == 'рублю' or mon2 == 'рубль':
            response = """Текущий курс {} к {}: {}""".format(mon1, mon2, sum_all_usd_rub)
        if mon1 == 'доллар' or mon1 == 'доллара' and mon2 == 'евро':
            response = """Текущий курс {} к {}: {}""".format(mon1, mon2, sum_all_usd_eur)

        dispatcher.utter_message(response)
        return [SlotSet('monetary', mon)]

class ActionGetGraph(Action):

    def name(self)-> Text:
        return "action_get_graph"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mon = tracker.get_slot('monetary')

        key = '7116a9ab2462d1fbd01568bc094eaafa'
        url_auth = 'https://currate.ru/api/?get' 
        url_tran = 'https://currate.ru/api/'

        valute_obs = {
            'рубль': 'RUB',
            'доллар': 'USD',
            'евро': 'EUR'
        }
        
        
        if mon == "Рубля" or mon == "Рубль" or mon == "рубля" or mon == "рубль":
            image = "https://charts.profinance.ru/html/charts/image?SID=qP6r7UB1&s=USDRUB&h=368&w=720&pt=2&tt=1&z=7&ba=2&nw=720&T=1671623606113&imd=1"
        if mon == "Доллара" or mon == "Доллар" or mon == "доллара" or mon == "доллар":
            image = "https://charts.profinance.ru/html/charts/image?SID=L4H3d9F0&s=EURUSD&h=368&w=720&pt=2&tt=1&z=7&ba=2&nw=720&T=1671623896006&imd=1"
        if mon == "Евро" or mon == "евро":
            image = "https://charts.profinance.ru/html/charts/image?SID=z8XfOUl7&s=EURRUB&h=368&w=720&pt=2&tt=1&z=7&ba=2&nw=720&T=1671623840908&imd=1"

        dispatcher.utter_message(image)
        return [SlotSet('monetary', mon)]


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
