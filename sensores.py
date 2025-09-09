def sensores(mundo, pos):
    x, y = pos
    mensagens = {
        "brisa": "Você sente uma brisa...",
        "fedor": "Você sente um fedor terrível...",
        "brilho": "Você vê um objeto brilhante..."
    }
    percepcoes = set()
    vizinhos = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    
    for i, j in vizinhos:
        if 0 <= i < len(mundo) and 0 <= j < len(mundo):
            if mundo[i][j] == "P":
                percepcoes.add("brisa")
            elif mundo[i][j] == "W":
                percepcoes.add("fedor")
            elif mundo[i][j] == "O":
                percepcoes.add("brilho")
    
    for percepcao in percepcoes:
        print(mensagens.get(percepcao, ""))
