"""Module for generating events by gamer report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from levelupreports.views.helpers import dict_fetch_all

class GamerEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            #write a query to get all events along with gamer full name
            db_cursor.execute("""
            SELECT 
                e.id,
                e.description,
                e.date,
                e.time,
                u.id,
                u.first_name || ' ' || u.last_name as full_name 
            FROM levelupapi_event e
            JOIN auth_user u
            ON e.organizer = u.id
            """)
            
            dataset = dict_fetch_all(db_cursor)
            
            events_by_gamer = [
                {
                    "id":1,
                    "full_name":"Carrie Belk",
                    "events":[
                        {
                            "id":1,
                            "date":"2022-05-25",
                            "time":"12:00:00",
                            "description":"The Classic Game of Sweet Revenge"
                        },
                        {
                            "id":2,
                            "date":"2022-05-27",
                            "time":"11:00:00",
                            "description":"Fantasy Role-Playing"   
                        },
                        {
                            "id":3,
                            "date":"2022-06-04",
                            "time":"09:00:00",
                            "description":"GameNight"
                        },
                        {
                            "id":5,
                            "date":"2022-06-20",
                            "time":"23:11:00",
                            "description":"testing testing"
                        }
                    ]
                }
            ]
            
            for row in dataset:
                event = {
                    row['id'], row['date'],row['time'], row['description']
                }
                
                user_dict = next(
                    (
                        gamer_event for gamer_event in events_by_gamer
                        if gamer_event['id'] == row ['id']
                    ),
                    None
                )
                
                if user_dict:
                    user_dict['events'].append(event)
                else:
                    events_by_gamer.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })
        template = 'users/list_with_events.html'
        
        context = {
            "eventgamer_list": events_by_gamer
        }
        
        return render(request, template, context)