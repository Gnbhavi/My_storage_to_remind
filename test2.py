import itertools
import random
from collections import defaultdict

import numpy

input_table = {
    "DAVD": 8,
    "EAF": 28,
    "ETF": 18,
    "EWI": 15,
    "FOI": 10,
    "PF": 20,
    "PL": 1,
    "PPF": 16,
    "SCIA": 14,
    "SR": 10,
    "TI": 7,
    "TL": 3,
}

max_allowed = {
    "EAF": 10,
    "PPF": 10,
    "ETF": 10,
    "FOI": 7,
    "SSF": 7,
    "PF": 7,
    "TI": 7,
    "EWI": 6,
    "TL": 6,
    "PL": 6,
    "SR": 5,
    "DAVD": 8,
    "SCIA": 8,
}


def valid_insertion(day, slot):
    if slot in day:
        return False
    if slot == "PL" and "TL" in day:
        return False
    if slot == "TL" and "PL" in day:
        return False
    if slot == "PF" and ("TI" in day or "SSF" in day):
        return False
    if slot == "TI" and ("PF" in day or "SSF" in day):
        return False
    if slot == "SSF" and ("PF" in day or "TI" in day):
        return False
    return True


def split_lst_into_max(input_slots):
    lst = []
    for slot, req_count in input_slots:
        mx_val = max_allowed[slot]
        n_days, r_days = divmod(req_count, mx_val)
        req_ = [mx_val] * n_days + ([r_days] if r_days != 0 else [])
        for k in req_:
            lst.append((slot, k))
    lst = sorted(lst, key=lambda x: x[1], reverse=True)
    return lst


def split_min_max(work_slots):
    min_lst = list(filter(lambda x: x[1] <= 6, work_slots))
    max_lst = list(filter(lambda x: x[1] > 6, work_slots))

    return min_lst, max_lst


days_ = {
    1: dict(),
    2: dict(),
    3: dict(),
    4: dict(),
    5: dict(),
    6: dict(),
}

if __name__ == '__main__':
    lst_ = [tuple((slot, input_table[slot])) for slot in input_table]
    work_slots = split_lst_into_max(lst_)
    less_than_7, greater_than_6 = split_min_max(work_slots)
    # print(less_than_6)
    # print(greater_than_6)
    used = 0

    for day in days_.keys():
        if less_than_7:
            slot, load = less_than_7.pop(-1)
            k = list(days_[day].keys())
            if valid_insertion(k, slot):
                days_[day][slot] = load
                used += 1
            else:
                less_than_7.insert(-1, (slot, load))
    print(used, len(less_than_7), len(greater_than_6))
    for i in range(2):
        for day in days_.keys():
            if greater_than_6:
                slot, load = greater_than_6.pop(0)
                k = list(days_[day].keys())
                if valid_insertion(k, slot):
                    days_[day][slot] = load
                else:
                    greater_than_6.insert(0, (slot, load))

    available_slots = less_than_7 + greater_than_6
    for e, avail_slot in enumerate(available_slots):
        slot, val = avail_slot
        for day in days_.keys():
            if valid_insertion(days_[day], slot):
                req_ = sum(days_[day].values())
                if val == 25 - req_ or len(days_[day]) <= 2 and val < 25 - req_:
                    days_[day][slot] = val
                    available_slots.pop(e)
                    break

    for e, avail_slot in enumerate(available_slots):
        slot, val = avail_slot
        for day in days_.keys():
            if len(days_[day].keys()) < 4 and valid_insertion(days_[day], slot):
                days_[day][slot] = val
                available_slots.pop(e)
                break

    print(available_slots)
    for day_ in days_:
        cur_val = sum(days_[day_].values())
        print(day_, days_[day_], cur_val, 25 - cur_val)
