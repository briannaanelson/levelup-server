"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT
                g.id,
                g.title,
                g.maker,
                g.skill_level,
                g.number_of_players,
                g.game_type_id,
                u.id,
                u.first_name || ' ' || u.last_name as full_name 
            FROM levelupapi_game g
            JOIN auth_user u
            ON g.gamer_id = u.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            games_by_user = [
                {
                    "id": 1,
                    "full_name": "Carrie Belk",
                    "games":[
                        {
                            "id": 1,
                            "title": "Sorry",
                            "maker": "Hasbro",
                            "skill_level": 1,
                            "number_of_players": 4,
                            "game_type_id": 1
                        },
                         {
                            "id": 2,
                            "title": "Codenames 2 Player",
                            "maker": "CGE",
                            "skill_level": 3,
                            "number_of_players": 2,
                            "game_type_id": 2
                        },
                        {
                            "id":3,
                            "title": "Codenames",
                            "maker": "CGE",
                            "skill_level": 3,
                            "number_of_players": 6,
                            "game_type_id": 2
                        },
                        {
                            "id": 4,
                            "title": "CodeWARS",
                            "maker": "BBB",
                            "skill_level": 3,
                            "number_of_players": 2,
                            "game_type_id": 2
                        },
                        {
                            "id": 5,
                            "title": "Uno",
                            "maker": "Mattel",
                            "skill_level": 1,
                            "number_of_players": 4,
                            "game_type_id": 2
                        },
                        {
                            "id": 6,
                            "title": "Uno",
                            "maker": "Mattel",
                            "skill_level": 1,
                            "number_of_players": 4,
                            "game_type_id": 1
                        },
                        
                    ]
                },
            ]

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                game =  {
                    row['title'], row['number_of_players'],
                    row['maker'], row['game_type_id'], row['skill_level'], row ["id"]
                    }
                    
                
                
                # This is using a generator comprehension to find the user_dict in the games_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                
                user_dict = next(
                    (
                        user_game for user_game in games_by_user
                        if user_game['id'] == row['id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    games_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "usergame_list": games_by_user
        }

        return render(request, template, context)
