current_movies={ "Hajen": "10:30",
                "The Shining": "13:00",
                "Emil i Lönneberga":"15:00",
                "Gudfadern":"17:00"}

print ("Vi visar följande filmer:")
for key in current_movies:
    print(key)

movie= input("Vad vill du se?\n")
showtime=current_movies.get(movie)

if showtime==None:
    print("Filmen visas inte idag.")
else:
    print ("Filmen spelas ",showtime)
    