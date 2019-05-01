# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz
from datetime import datetime, timedelta
from app.interpreter.dExtenso import dExtenso
from app.interpreter.response_code import ResponseCode
from app.database.repository.repository import Repository
import time


class Interpreter(object):
    def __init__(self):
        self.__repo = Repository()
        self.bdStates = pd.DataFrame(
            {'state_code': ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
                            'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'],
             'state': ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal',
                       'Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais',
                       'Pará',
                       'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte',
                       'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe',
                       'Tocantins']},
            columns=['state_code', 'state'])

        self.date_now = ['hoje', 'amanhã', 'depois de amanhã', 'hoje de manhã', 'hoje de tarde', 'hoje a tarde',
                         'hoje de noite', 'hoje a noite', 'amanhã de manhã', 'amanhã de tarde', 'amanhã a tarde',
                         'amanhã de noite', 'amanhã a noite', 'depois de amanhã de manhã', 'depois de amanhã de tarde',
                         'depois de amanhã a tarde', 'depois de amanhã de noite', 'depois de amanhã a noite']

        self.date_next = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo',
                          'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira',
                          'próxima segunda', 'próxima terça', 'próxima quarta', 'próxima quinta',
                          'próxima sexta', 'próximo sábado', 'próximo domingo', 'próxima segunda-feira',
                          'próxima terça-feira', 'próxima quarta-feira', 'próxima quinta-feira',
                          'próxima sexta-feira', 'segunda que vem', 'terça que vem', 'quarta que vem',
                          'quinta  que vem', 'sexta que vem', 'sábado que vem', 'domingo que vem',
                          'segunda-feira que vem', 'terça-feira que vem', 'quarta-feira que vem',
                          'quinta-feira que vem', 'sexta-feira que vem']

    def user_city(self, user_input):
        city = self.__repo.get_bus_station_to_pandas_()

        len_id = []
        match1 = []

        for index, row in city.iterrows():
            match1.append(fuzz.token_sort_ratio(row['city_name'], user_input))
            len_id.append(len(row['associated_ids']))

        city['match1'] = match1
        city['lenID'] = len_id
        city = city[city.match1 >= max(city.match1) - 4].reset_index(drop=True)

        # Verify if match string has less that 70%
        if max(city.match1) < 70:
            return ResponseCode.ASK_AGAIN, 0

        # Check if was found one more city in matched
        if len(list(city.state_code.unique())) > 1:
            city['state'] = city['state_code'].apply(
                lambda x: self.bdStates[self.bdStates['state_code'] == x]['state'].reset_index().loc[0]['state'])
            return ResponseCode.ASK_STATE, list(city.state.unique())

        # Check if was found unique city, then return it
        if len(list(city.state_code.unique())) == 1 and len(city) > 1:
            city = city[city.lenID == max(city.lenID)].reset_index(drop=True)
            return ResponseCode.NEXT, city.id_bus_station[0]

        if len(list(city.state_code.unique())) == 1 and len(city) == 1:
            return ResponseCode.NEXT, city.id_bus_station[0]

    def user_state(self, user_input):
        city = self.__repo.get_bus_station_to_pandas_()
        city = pd.merge(city, self.bdStates, how='outer', on=['state_code'])

        userInput = pd.DataFrame(user_input)

        match1 = []
        match2 = []
        match3 = []

        for index, row in city.iterrows():
            match1.append(fuzz.token_sort_ratio(row['city_name'], userInput['station_name'][0]))
            match2.append(fuzz.token_sort_ratio(row['state_code'], userInput['state_name'][0]))
            match3.append(fuzz.token_sort_ratio(row['state'], userInput['state_name'][0]))

        city['match1'] = match1
        city['match2'] = match2
        city['match3'] = match3

        city = city[city.match1 >= max(city.match1) - 4].reset_index(drop=True)

        if (max(city.match2) > 50) or (max(city.match3) > 50):
            if max(city.match3) > max(city.match2):
                city = city[city.match3 == max(city.match3)].reset_index(drop=True)
            else:
                city = city[city.match2 == max(city.match2)].reset_index(drop=True)
            city.sort_values(by='population')
            return ResponseCode.NEXT, city.id_bus_station[0]

        return ResponseCode.ASK_AGAIN, 0

    def user_travel_date(self, user_input_):
        user_input = str(user_input_).lower()
        # Dataframe date_request
        travel_date = pd.read_csv('./app/interpreter/date_request.csv')

        # Transformar numero em seu extenso
        n_exten = dExtenso()
        number = re.findall('^([A-Z]*\s?[0-9]*)[\s_-]*([1-9][1-9]*$)?', user_input)[0][0]
        if number is not '':
            try:
                user_input = re.sub('^([A-Z]*\s?[0-9]*)[\s_-]*([1-9][1-9]*$)?', n_exten.getExtenso(number) + ' ',
                                    user_input)
            except IndexError:
                pass

        match1 = []
        for index, row in travel_date.iterrows():
            match1.append(fuzz.token_sort_ratio(row['request'], user_input))

        travel_date['match1'] = match1
        travel_date = travel_date[travel_date.match1 == max(travel_date.match1)].reset_index(drop=True)

        _day = travel_date.day[0]
        # Check request exist on date_now or date_next
        if travel_date.request[0] in self.date_now:
            travel_date.day[0] = (datetime.now() + timedelta(int(_day))).day
            travel_date.month[0] = (datetime.now() + timedelta(int(_day))).month

        elif travel_date.request[0] in self.date_next:
            # Se o dia ainda contém nessa semana
            if travel_date.day[0] >= (((datetime.now().weekday() + 1) % 7) + 1):
                travel_date.day[0] = (datetime.now() + timedelta(int(_day) - (datetime.now().weekday() + 1))).day
                travel_date.month[0] = (datetime.now() + timedelta(int(_day) - (datetime.now().weekday() + 1))).month
            else:
                # Se o dia passado for menor que o atual, significa que será na próxima semana
                travel_date.day[0] = (
                        datetime.now() + timedelta(7 - (((datetime.now().weekday() + 1) % 7) + 1)) + timedelta(
                    int(travel_date.day[0])) + timedelta(1)).day
                travel_date.month[0] = (datetime.now() + timedelta(7 - (((datetime.now().weekday() + 1) % 7) + 1))
                                        + timedelta(int(_day)) + timedelta(1)).month

        # Getting year
        now = datetime.now()
        travel_year = now.year + 1 if now.month > travel_date.month[0] else now.year

        travel_date_str = str(travel_year) + '-' + str(travel_date.month[0]) + '-' + str(travel_date.day[0])

        return ResponseCode.NEXT, travel_date_str
