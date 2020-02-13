import argparse
import re

import pandas as pd

offers_columns = ['offer_name', 'link_to_offer', 'price', 'country', 'placed', 'condition']

def get_priority(time_range):
    if time_range.startswith('hour'):
        return 0
    if time_range.startswith('day'):
        return 1
    if time_range.startswith('month'):
        return 2
    if time_range.startswith('year'):
        return 3


def compare_time(placed, relevant_placed):
    if relevant_placed == None:
        return True

    num1, num2 = int(placed.split(' ')[0]), int(relevant_placed.split(' ')[0])
    time_range1, time_range2 = placed.split(' ')[1], relevant_placed.split(' ')[1]

    priority1 = get_priority(time_range1)
    priority2 = get_priority(time_range2)

    if priority1 < priority2:
        return True
    if priority1 == priority2:
        if num1 <= num2:
           return True
        else:
            return False
    if priority1 > priority2:
        return False


def show_offer(row, counter):
    print('Offer %d:\nName: %s\nLink on BGG: %s\nPrice: %s\nCountry: %s\nPlaced: %s\nCondition: %s\n'
          % (counter, row['offer_name'], row['link_to_offer'], row['price'], row['country'], row['placed'], row['condition']))
    input("Press Enter to continue...\n")


def compare_prices(price, relevant_price):
    price = re.findall(r'\d+', price)[0]
    if relevant_price == None:
        return True
    if int(price) <= relevant_price:
        return True
    return False


def show_offers(relevant_offers, relevant_price, relevant_placed):
    counter = 1
    for index, row in relevant_offers.iterrows():
        if compare_prices(row['price'], relevant_price):
            if compare_time(row['placed'], relevant_placed):
                show_offer(row, counter)
                counter += 1




def main(params):
    print('Filtering your offers list...')
    relevant_offers = pd.read_csv('offers_info.csv', usecols=offers_columns)
    print(relevant_offers.shape)


    # filter by country
    if params.countries != None:
        relevant_offers = relevant_offers[relevant_offers['country'].isin(params.countries)]
        print(relevant_offers.shape)

    # for country in params.coutries:
    #     selected_offers = all_offers[all_offers['country' == country]]
    #     relevant_offers = pd.concat([relevant_offers, selected_offers], axis=0, sort=False, ignore_index=True)
    #     del selected_offers

    # filter by condition
    if params.game_condition != None:
        relevant_offers = relevant_offers[relevant_offers['condition'].isin(params.game_condition)]
        print(relevant_offers.shape)

    # for condition in params.game_condition:
    #     selected_offers = relevant_offers[relevant_offers['condition' == condition]]
    #     relevant_offers = pd.concat([relevant_offers, selected_offers], axis=0, sort=False, ignore_index=True)
    #     del selected_offers

    # filter by words in name
    if params.exclude_words != None:
        for word in params.exclude_words:
            relevant_offers = relevant_offers[relevant_offers['offer_name'].str.contains(word) == False]
            print(relevant_offers.shape)

    show_offers(relevant_offers, params.price, params.placed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Parsed Offers')
    parser.add_argument('--exclude_words', type=list, default=None, help='specify which words to avoid (\'like avoid offers of \'Korean\' game edition etc.\')')
    parser.add_argument('--countries', type=list, default=['germany', 'ukraine'], help='specify offers from which countries you are interested in')
    parser.add_argument('--game_condition', type=list, default=['N', 'LN', 'VG', 'G', 'A', 'Through'], help='specify which game condition you accept (N - new, LN - like new, VG - very good, G - good, A - acceptable, Through,  )')
    parser.add_argument('--placed', type=str, default='6 month ago', help='specify from which date placed offers to observe')
    parser.add_argument('--price', type=int, default=45, help='specify which maximum price is acceptable for you')
    opt= parser.parse_args()
    main(opt)