
# testing movie response / data value
test_movie_id = "2baf70d1-42bb-4437-b551-e5fed5a87abe"
test_movie_list = {
"2baf70d1-42bb-4437-b551-e5fed5a87abe":
     {
        "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
        "title": "Castle in the Sky",
        "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of"
                       " Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes"
                       " her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil"
                       " Muska, who plans to use Laputa's science to make himself ruler of the world.",
        "director": "Hayao Miyazaki",
        "producer": "Isao Takahata",
        "release_date": "1986",
        "rt_score": "95",
        "people": [
        ],
        "url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
      }
}

# testing people response / data value
test_people_id = "ba924631-068e-4436-b6de-f3283fa848f0"
test_people_list = {
    "ba924631-068e-4436-b6de-f3283fa848f0": {
        "id": "ba924631-068e-4436-b6de-f3283fa848f0",
        "name": "Ashitaka",
        "gender": "Male",
        "age": "late teens",
        "eye_color": "Brown",
        "hair_color": "Brown",
        "films": [
        ],
        "url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
    }
}

# map movie to people
test_movie_list["2baf70d1-42bb-4437-b551-e5fed5a87abe"]["people"] = \
    [test_people_list["ba924631-068e-4436-b6de-f3283fa848f0"]]
test_people_list["ba924631-068e-4436-b6de-f3283fa848f0"]["films"] = \
    [test_movie_list["2baf70d1-42bb-4437-b551-e5fed5a87abe"]]
