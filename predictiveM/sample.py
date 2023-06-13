import datetime

from .predict import predict_on_test
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from .production import *
from django.http import HttpResponse
from .models import Allocate
import csv
import datetime
import holidays
from dateutil.parser import parse

labels = ["Machine 1", "Machine 2", "Machine 3", "Machine 4", "Machine 5", "Machine 6",
          "Machine 7", "Machine 8", "Machine 9", "Machine 10"]
days_data = predict_on_test('test_FD001.txt')
machine_0 = [68, 91, 34, 29, 16, 43, 31, 35, 68, 38, 81, 62, 54, 77, 85, 21, 62, 81, 48, 80, 65, 85, 55, 40, 62,
             46,
             70,
             77,
             74, 35, 90, 93, 47, 16, 86, 83, 79, 94, 90, 72, 62, 52, 71, 83, 33, 95, 82, 13, 90, 39, 56, 51, 28,
             18,
             26,
             69,
             54, 47, 44, 65, 53, 72, 45, 85, 55, 60, 71, 73, 38, 55, 86, 51, 81, 57, 30, 63, 95, 40, 21, 41, 38,
             90,
             75,
             71,
             36, 71, 13, 47, 71, 91]

from datetime import timedelta

print(days_data[:10])
sorted_days_data = sorted(days_data[:10])
print(sorted_days_data, '22222222222222222222')


def home(request):
    if request.method == 'POST':
        range_day = request.POST.get('day_range')
        holidays_list = ['2023-01-01', '2023-01-14', '2023-01-26', '2023-03-29', '2023-04-01', '2023-04-14',
                         '2023-05-01',
                         '2023-08-15', '2023-10-02', '2023-10-19', '2023-12-25']
        # Convert the holiday strings to datetime objects
        holiday = [datetime.datetime.strptime(holiday, '%Y-%m-%d').date() for holiday in holidays_list]

        # Get today's date
        today = datetime.date.today()

        # Calculate the range of dates
        date_range = [today + timedelta(days=x) for x in range(int(range_day))]

        # Exclude weekends and holidays
        filtered_dates = []
        for date in date_range:
            if date.weekday() < 5 and date not in holiday:
                filtered_dates.append(date.strftime('%Y-%m-%d'))

        # Print the list of filtered dates
        print(filtered_dates)

        # print(range_dates, '^^^^^^^^^^^^^^^^^^^^^^^^^^')
        machine_id_list = []
        allocated_day = []
        planned_date = []
        maintenance_team = []
        maintenance_on_list = []

        us_holidays = holidays.US()  # Create an instance of US holidays

        for day in sorted_days_data:
            if day < int(range_day):
                subset = machine_0[int(day) - 7:int(day)]

                lowest_value = float('inf')

                for element in subset:
                    if element < lowest_value:
                        lowest_value = element

                lowest_index = machine_0.index(lowest_value)

                today = datetime.date.today()
                total_date = today + datetime.timedelta(days=int(day))
                print(total_date, 'ssssssssssssssssssssssssssssssss')
                next_90_days = total_date - datetime.timedelta(days=7)
                today1 = datetime.date.today()
                maintenance_on = today1 + datetime.timedelta(days=int(day))
                index_of_machine = sorted_days_data.index(day)
                print(index_of_machine, '888888888888888888888888888')

                machine_id_list.append(labels.index(labels[index_of_machine - 1]) + 1)

                for le in range(0, 10):
                    if len(allocated_day) != 0:
                        while True:
                            if next_90_days.weekday() >= 5 or next_90_days in us_holidays:
                                next_90_days += datetime.timedelta(days=1)
                            elif next_90_days.weekday() in [5, 6]:
                                next_90_days += datetime.timedelta(days=1)
                            else:
                                break

                        if next_90_days in allocated_day:
                            one_day = datetime.timedelta(days=1)
                            new_date = next_90_days - one_day
                            while new_date.weekday() in [5, 6] or new_date in us_holidays:
                                new_date -= datetime.timedelta(days=1)
                            if new_date not in allocated_day:
                                allocated_day.append(new_date)
                        else:
                            allocated_day.append(next_90_days)
                    else:
                        while True:
                            if next_90_days.weekday() >= 5 or next_90_days in us_holidays:
                                next_90_days += datetime.timedelta(days=1)
                            else:
                                break
                        allocated_day.append(next_90_days)

                planned_date.append(today)
                maintenance_team.append('Crew_1')
                maintenance_on_list.append(maintenance_on)

        a_list = []
        p_list = []
        m_list = []

        for a in allocated_day:
            b = a.strftime('%B %d, %Y')
            a_list.append(b)

        for p in planned_date:
            c = p.strftime('%B %d, %Y')
            p_list.append(c)

        for m in maintenance_on_list:
            d = m.strftime('%B %d, %Y')
            m_list.append(d)

        sorted_dates = sorted(a_list, key=lambda x: parse(x), reverse=True)

        print(sorted_dates)

        return render(request, 'splitscreen.html',
                      context={"data": zip(machine_id_list, a_list, p_list, m_list, maintenance_team),
                               'filtered_dates': filtered_dates})
    return render(request, 'splitscreen.html')


def population_chart(request):
    my_int_list = [int(x) for x in days_data[0:15]]
    # print(my_int_list)

    data = my_int_list

    return JsonResponse(data={
        'labels': labels,
        'data': data,

    })


def update_bar_index(request):
    if request.method == 'POST':
        index = request.POST.get('index')
        print(index, '*' * 100)
        request.session['index'] = index
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def index(request):
    return render(request, 'splitscreen.html')


# def ExpMaintainGrph(request):
#     idx = request.session['index']
#     predicted_life = [70, 85, 28, 40, 64, 83, 54, 46, 89, 51]
#     remains_days = predicted_life[int(idx)]
#     print(type(idx), '+++++++++++++++++++++')
#     name = 'machine_' + str(idx)
#     single_machine_production = getDataOfsingileMation(name)
#     print(name, '-----------------')
#
#     today = datetime.date.today()
#     next_90_days = today + datetime.timedelta(days=100)
#
#     dates_list = []
#
#     for i in range(1, 90):
#         date = today + datetime.timedelta(days=i)
#         if date < next_90_days:
#             dates_list.append(date)
#     dates_list = [dates.strftime('%Y-%m-%d') for dates in dates_list]
#
#     # _________________________________________Data for graph______________________________________
#
#     labels = dates_list
#     data = single_machine_production
#     print(data)
#     print(labels)
#
#     # print(labels, '************************************')
#     team1 = 'maintanenceTeam1'
#     Saturday_list = []
#     sunday_list = []
#     today = datetime.date.today()
#     num_days = 100
#     for i in range(num_days):
#         date = today + datetime.timedelta(days=i)
#         if date.weekday() == 5:
#             # print("Saturday:", date)
#             Saturday_list.append(date)
#             # print('Sundayyyyyyyyyyyyyy', Saturday_list)
#         elif date.weekday() == 6:
#             sunday_list.append(date)
#             # print("Sunday:", date)
#             # print('aturrrrr', sunday_list)
#
#     return JsonResponse(data={
#         'Labels': labels,
#         'data': data,
#         'remains_days': remains_days,
#         'team': team1,
#         'Saturday': Saturday_list,
#         'sunday': sunday_list,
#     })

def ExpMaintainGrph(request):
    # idx = request.session['index']
    predicted_life = [70, 85, 28, 40, 64, 83, 54, 46, 89, 51]
    # remains_days = predicted_life[int(0)]
    name = 'machine_' + str(0)
    single_machine_production = getDataOfsingileMation(name)
    print(name)
    today = datetime.date.today()
    next_90_days = today + datetime.timedelta(days=100)

    events = []
    for i, value in enumerate(single_machine_production):
        date = today + datetime.timedelta(days=i)
        if date < next_90_days:
            event = {
                'title': str(value),
                'start': date.isoformat(),
                'allDay': True,
                'className': 'success'
            }
            events.append(event)

    return JsonResponse(events, safe=False)


def allocate_maintenance(request):
    machine_names = ["machine_0", "machine_1", "machine_2", "machine_3", "machine_4", "machine_5", "machine_6",
                     "machine_7", "machine_8", "machine_9"]
    if request.method == 'POST':
        idx = request.session['index']
        label = request.POST.get('label')
        data = request.POST.get('data')
        is_urgent = request.POST.get('is_urgent')
        # print(label, '-------------', data, '-----------------', is_urgent, 'dataaaaaaaaaa')
        # print(machine_names[int(idx)], '.' * 50)
        machine_name = machine_names[int(idx)]
        Allocate.objects.create(date_of_maintenance=label, machine_name=machine_name, is_allocate_or_not=is_urgent)

        return JsonResponse({'status': 'success'})


sunday_list = []
Saturday_list = []


def get_date_and_day():
    import datetime
    today = datetime.date.today()
    num_days = 100
    for i in range(num_days):
        date = today + datetime.timedelta(days=i)
        if date.weekday() == 5:
            print("Saturday:", date)
            Saturday_list = date
            print('Sundayyyyyyyyyyyyyy', Saturday_list)
        elif date.weekday() == 6:
            sunday_list = date
            print("Sunday:", date)
            print('aturrrrr', sunday_list)

            return JsonResponse(data={
                'Saturday': Saturday_list,
                'sunday': sunday_list,
            })
