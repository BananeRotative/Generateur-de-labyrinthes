# Créé par alexi, le 21/06/2021 en Python 3.7
# Taille max pour impression A4: 90x64
import pygame, random, sys
#OPTIONS :
#Dimensions
Longueur = 100
Largeur = 100
Dims = (Longueur, Largeur)

#Construction du labyrinthe
LabyParfait = True
Destroying_wall_chance = 10     # si le labyrinthe n'est pas parfait
Show_most_distants_points = True
Optimized = True
Path = "Straight"
Hole_in_Middle = False
Dims_Hole_in_Middle = (3, 3)    # si il y a un espace au milieu
Start_in_Middle = False         # si il y a un espace au milieu
Start_And_End_in_border = True

#Affichage
show_labyrinth="square"
len_paths = 1
len_walls = 1
Save_image = True




# note (01/04/2023) : je connais maintenant la différence entre "maze" et "labyrinth" en anglais
# j'utilise dans ce script le mot "labyrinth" tandis que j'aurais dû utiliser "maze"

def Generate_Labyrinth(Dims, LabyParfait = True, Destroying_wall_chance = 40, Show_most_distants_points = True, show_labyrinth = "basic", Save_image = False, Optimized = True, Path = "Straight"):
    #L'aspect général du labyrinthe change selon l'activation ou non de l'optimisation
    print(Destroying_wall_chance)
    global Walls, CasesNumbers, Hole_in_Middle
    Optimize = Optimized
    Walls = []
    CasesNumbers = []
    for X in range(Dims[0]):
        Walls.append([])
        CasesNumbers.append([])
        for Y in range(Dims[1]):
            Walls[X].append([True, True, True, True])   #haut, bas, gauche, droite
            CasesNumbers[X].append(X*Dims[0] + Y)
    if Optimized:
        CasesLeft = []
        for X in range(Dims[0]):
            for Y in range(Dims[1]):
                CasesLeft.append((X, Y))
        if Path == "Diagonal":
            Lines = []
            for line in range(Dims[0] + Dims[1] -1):
                Lines.append([])
                if line < Dims[0]:
                    for XY in range(Dims[0]):
                        if not XY + line >= Dims[0]:   #problème
                            Lines[-1].append((XY + line, XY))
                else:
                    for XY in range(Dims[1]):
                        if not XY + line - (Dims[0] -1) >= Dims[1]:   #problème
                            Lines[-1].append((XY, XY + line - (Dims[0] -1)))
    if Hole_in_Middle:
        StartingX, StartingY = round((Dims[0] -1)/2) - round((Dims_Hole_in_Middle[0] -1)/2), round((Dims[1] -1)/2) - round((Dims_Hole_in_Middle[1] -1)/2)
        Num_in_Middle = CasesNumbers[StartingX][StartingY]
        for X in range(StartingX, StartingX + Dims_Hole_in_Middle[0]):
            for Y in range(StartingY, StartingY + Dims_Hole_in_Middle[1]):
                CasesNumbers[X][Y] = Num_in_Middle
                if not Y == StartingY:
                    Walls[X][Y][0] = False
                if not Y == StartingY + Dims_Hole_in_Middle[1] -1:
                    Walls[X][Y][1] = False
                if not X == StartingX:
                    Walls[X][Y][2] = False
                if not X == StartingX + Dims_Hole_in_Middle[0] -1:
                    Walls[X][Y][3] = False

    Continuer = True
    CheckPath = False
    while Continuer:
        ForceWallDestruction = False
        if not LabyParfait and random.randint(0, Destroying_wall_chance -1) == 0:
            X = random.randint(0, Dims[0] -1)
            Y = random.randint(0, Dims[1] -1)
            Directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            ValidDirection = False
            while not ValidDirection:
                Direction = random.randint(0, 3)    #haut, bas, gauche, droite
                if not (X + Directions[Direction][0] < 0 or X + Directions[Direction][0] >= Dims[0]):
                    if not (Y + Directions[Direction][1] < 0 or Y + Directions[Direction][1] >= Dims[1]):
                        ValidDirection = True
            ForceWallDestruction = True
        else:
            if Optimize:
                len_CasesLeft = len(CasesLeft)
                if len_CasesLeft%1000 == 0:
                    print(len_CasesLeft)
                num_CasesLeft = random.randint(0, len_CasesLeft -1)
                (X, Y) = CasesLeft[num_CasesLeft]
                del CasesLeft[num_CasesLeft]
            else:
                if Optimized:
                    if Path == "Straight":
                        MustBreak = False
                        for Xcases in range(Dims[0]):
                            for Ycases in range(Dims[1]):
                                if not CasesNumbers[Xcases][Ycases] == 0:
                                    X, Y = Xcases, Ycases
                                    MustBreak = True
                                    break
                            if MustBreak:
                                break
                        else:
                            Continuer = False

                    elif Path == "Diagonal":
                        MustBreak = False
                        for line in Lines:
                            for case in line:
                                if not CasesNumbers[case[0]][case[1]] == 0:
                                    for Xside, Yside in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                                        if case[0] + Xside > -1 and case[0] + Xside < Dims[0]:
                                            if case[1] + Yside > -1 and case[1] + Yside < Dims[1]:
                                                if not CasesNumbers[case[0] + Xside][case[1] + Yside] == CasesNumbers[case[0]][case[1]]:
                                                    (X, Y) = case
                                                    MustBreak = True
                                                    break
                                    if MustBreak:
                                        break
                            if MustBreak:
                                break
                        else:
                            Continuer = False
                else:
                    X = random.randint(0, Dims[0] -1)
                    Y = random.randint(0, Dims[1] -1)
            Direction = random.randint(0, 3)    #haut, bas, gauche, droite
        if Walls[X][Y][Direction]:
            if Direction == 0:
                X2 = X
                Y2 = Y -1
            elif Direction == 1:
                X2 = X
                Y2 = Y +1
            elif Direction == 2:
                X2 = X -1
                Y2 = Y
            elif Direction == 3:
                X2 = X +1
                Y2 = Y
            else:
                print("ERREUR !")
            if X2 >= 0 and Y2 >= 0:
                if X2 <= Dims[0] -1 and Y2 <= Dims[1] -1:
                    NewDirections = [1, 0, 3, 2]
                    Direction2 = NewDirections[Direction]
                    Number1, Number2 = CasesNumbers[X][Y], CasesNumbers[X2][Y2]
                    if Number1 > Number2:
                        OldNumber = Number1
                        NewNumber = Number2
                        SameNumbers = False
                    elif Number2 > Number1:
                        OldNumber = Number2
                        NewNumber = Number1
                        SameNumbers = False
                    else:
                        OldNumber = Number1
                        NewNumber = Number2
                        SameNumbers = True
                    if not SameNumbers:
                        ChangeValues = True
                    elif ForceWallDestruction:
                        ChangeValues = True
                    else:
                        ChangeValues = False
                    if ChangeValues:
                        Walls[X][Y][Direction] = False
                        Walls[X2][Y2][Direction2] = False
                        for X in range(Dims[0]):
                            for Y in range(Dims[1]):
                                if CasesNumbers[X][Y] == OldNumber:
                                    CasesNumbers[X][Y] = NewNumber
                    CheckPath = True

        if Optimize:
            if len_CasesLeft == 1:
                Optimize = False
        else:
            if not Optimized:
                if CheckPath:
                    Continuer = False
                    for X in range(Dims[0]):
                        for Y in range(Dims[1]):
                            if not CasesNumbers[X][Y] == 0:
                                Continuer = True
                                break
                        if Continuer:
                            break
                    CheckPath = False

    #longest path
    if Show_most_distants_points:
        MostDistantsPoints = Get_most_distants_points(Dims)
        if not show_labyrinth == False:
            Show_labyrinth(Dims, Show_most_distants_points, MostDistantsPoints, Save_image, LabyType=show_labyrinth)
    elif not show_labyrinth == False:
        Show_labyrinth(Dims, Show_most_distants_points, Save_image, LabyType=show_labyrinth)

def Get_most_distants_points(Dims):
    Actual_pos = [0, 0]
    Previous_direction = 1      #0:haut ; 1:bas ; 2:gauche ; 3:droite
    distance_from_staring_point = 0
    Directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    Opposite_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    EndPaths = []       #for each endpath : [previous direction, distance from starting point, (X, Y)]
    DeadEnds = []       #for each Dead end : [distance from starting point, (X, Y)]
    Most_distants_points = []
    Explorated = [[False for Y in range(Dims[1])] for X in range(Dims[0])]
    for loop in range(2):
        EveryCaseExplored = False
        while not EveryCaseExplored:
            Is_a_DeadEnd = True
            for direction, wall in enumerate(Walls[Actual_pos[0]][Actual_pos[1]]):
                if not Directions[direction] == Opposite_directions[Previous_direction] and not wall:
                    if not Explorated[Actual_pos[0] + Directions[direction][0]][Actual_pos[1] + Directions[direction][1]]:
                        EndPaths.append([direction, distance_from_staring_point +1, (Actual_pos[0] + Directions[direction][0], Actual_pos[1] + Directions[direction][1])])
                        Explorated[Actual_pos[0] + Directions[direction][0]][Actual_pos[1] + Directions[direction][1]] = True
                        Is_a_DeadEnd = False
            if Is_a_DeadEnd:
                DeadEnds.append([distance_from_staring_point +1, (Actual_pos[0], Actual_pos[1])])

            if len(EndPaths) == 0:
                EveryCaseExplored = True
            else:
                last_EndPath = len(EndPaths) -1
                Previous_direction = EndPaths[last_EndPath][0]
                distance_from_staring_point = EndPaths[last_EndPath][1]
                Actual_pos = [EndPaths[last_EndPath][2][0], EndPaths[last_EndPath][2][1]]
                del EndPaths[last_EndPath]
        if Start_And_End_in_border:
            Finish_Loop = False
            while not Finish_Loop:
                if DeadEnds[0][1][0] == 0 or DeadEnds[0][1][0] == Dims[0] -1 or DeadEnds[0][1][1] == 0 or DeadEnds[0][1][1] == Dims[1] -1:
                    Finish_Loop = True
                else:
                    del DeadEnds[0]
            while len(DeadEnds) > 1:
                if DeadEnds[1][1][0] == 0 or DeadEnds[1][1][0] == Dims[0] -1 or DeadEnds[1][1][1] == 0 or DeadEnds[1][1][1] == Dims[1] -1:
                    if DeadEnds[0][0] > DeadEnds[1][0]:
                        del DeadEnds[1]
                    else:
                        del DeadEnds[0]
                else:
                    del DeadEnds[1]
        else:
            while len(DeadEnds) > 1:
                if DeadEnds[0][0] > DeadEnds[1][0]:
                    del DeadEnds[1]
                else:
                    del DeadEnds[0]
        if Start_in_Middle and loop == 0:
            Most_distants_points.append((round((Dims[0] -1)/2), round((Dims[1] -1)/2)))
            Actual_pos = [round((Dims[0] -1)/2), round((Dims[1] -1)/2)]
        else:
            print("Distance des deux points :", DeadEnds[0][0])
            Most_distants_points.append(DeadEnds[0][1])
            Actual_pos = [DeadEnds[0][1][0], DeadEnds[0][1][1]]
        for direction, wall in enumerate(Walls[Actual_pos[0]][Actual_pos[1]]):
            if not wall:
                Previous_direction = direction
                break
        distance_from_staring_point = 0
        EndPaths = []
        DeadEnds = []
        Explorated = [[False for Y in range(Dims[1])] for X in range(Dims[0])]
    print(Most_distants_points)
    return Most_distants_points

def Show_labyrinth(Dims, Show_most_distants_points, MostDistantsPoints = None, Save_image = True, LabyType = "basic"):
    #pygame.init()
    #screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1366, 768))
    screen.fill((128, 128, 128))
    if LabyType == "basic":
        CaseImg = pygame.image.load("images/case.png").convert()
        Mur_vertical = pygame.image.load("images/mur vertical.png").convert()
        Mur_horizontal = pygame.image.load("images/mur horizontal.png").convert()
        Point = pygame.image.load("images/point.png").convert()
        Laby = pygame.Surface((12*Dims[0], 12*Dims[1]))
        for X in range(Dims[0]):
            for Y in range(Dims[1]):
                Laby.blit(CaseImg, [X*12, Y*12, 12, 12], [0, 0, 12, 12])
        for X in range(Dims[0]):
            for Y in range(Dims[1]):
                if Walls[X][Y][0]:
                    Laby.blit(Mur_horizontal, [X*12, Y*12 -1, 12, 2], [0, 0, 12, 2])
                if Walls[X][Y][1]:
                    Laby.blit(Mur_horizontal, [X*12, Y*12 +11, 12, 2], [0, 0, 12, 2])
                if Walls[X][Y][2]:
                    Laby.blit(Mur_vertical, [X*12 -1, Y*12, 2, 12], [0, 0, 2, 12])
                if Walls[X][Y][3]:
                    Laby.blit(Mur_vertical, [X*12 +11, Y*12, 2, 12], [0, 0, 2, 12])

        for X in range(Dims[0]):
            Laby.blit(Mur_horizontal, [X*12, 0, 12, 2], [0, 0, 12, 2])
            Laby.blit(Mur_horizontal, [X*12, Dims[1]*12 -2, 12, 2], [0, 0, 12, 2])
        for Y in range(Dims[1]):
            Laby.blit(Mur_vertical, [0, Y*12, 2, 12], [0, 0, 2, 12])
            Laby.blit(Mur_vertical, [Dims[0]*12 -2, Y*12, 2, 12], [0, 0, 2, 12])

        if Show_most_distants_points:
            Laby.blit(Point, [MostDistantsPoints[0][0]*12 +4, MostDistantsPoints[0][1]*12 +4, 4, 4], [0, 0, 4, 4])
            Laby.blit(Point, [MostDistantsPoints[1][0]*12 +4, MostDistantsPoints[1][1]*12 +4, 4, 4], [0, 0, 4, 4])

    elif LabyType == "square":
        global len_paths, len_walls
        if len_paths > 3:
            len_paths = 3
        elif len_paths < 1:
            len_paths = 1
        if len_walls < 1:
            len_walls = 1
        elif len_walls > 3:
            len_walls = 3
        if len_paths == 1:
            Cases_width = 2
            RelativePos = [[(-1, -1), (0, -1), (1, -1)], [(-1, 1), (0, 1), (1, 1)], [(-1, -1), (-1, 0), (-1, 1)], [(1, -1), (1, 0), (1, 1)]]
        elif len_paths == 2:
            Cases_width = 3
            RelativePos = [[(-1, -1), (0, -1), (1, -1), (2, -1)], [(-1, 2), (0, 2), (1, 2), (2, 2)], [(-1, -1), (-1, 0), (-1, 1), (-1, 2)], [(2, -1), (2, 0), (2, 1), (2, 2)]]
        else:
            Cases_width = 4
            RelativePos = [[(-1, -1), (0, -1), (1, -1), (2, -1), (3, -1)], [(-1, 3), (0, 3), (1, 3), (2, 3), (3, 3)], [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3)], [(3, -1), (3, 0), (3, 1), (3, 2), (3, 3)]]
        if len_walls > 1:
            NumberToReplace = Cases_width -1
            if len_walls == 2:
                Cases_to_add = [[(-2, -2), (NumberToReplace +1, -2)], [(-2, NumberToReplace +1), (NumberToReplace +1, NumberToReplace +1)],
                [(-2, -2), (-2, NumberToReplace +1)], [(NumberToReplace +1, -2), (NumberToReplace +1, NumberToReplace +1)]]
            elif len_walls == 3:
                Cases_to_add = [[(-3, -3), (-3, -2), (-2, -3), (-2, -2), (NumberToReplace +1, -2), (NumberToReplace +2, -2), (NumberToReplace +1, -3), (NumberToReplace +2, -3)],
                [(-3, NumberToReplace +1), (-3, NumberToReplace +2), (-2, NumberToReplace +1), (-2, NumberToReplace +2), (NumberToReplace +1, NumberToReplace +1), (NumberToReplace +1, NumberToReplace +2), (NumberToReplace +2, NumberToReplace +1), (NumberToReplace +2, NumberToReplace +2)],
                [(-3, -3), (-3, -2), (-2, -3), (-2, -2), (-3, NumberToReplace +1), (-3, NumberToReplace +2), (-2, NumberToReplace +1), (-2, NumberToReplace +2)],
                [(NumberToReplace +1, -2), (NumberToReplace +2, -2), (NumberToReplace +1, -3), (NumberToReplace +2, -3), (NumberToReplace +1, NumberToReplace +1), (NumberToReplace +1, NumberToReplace +2), (NumberToReplace +2, NumberToReplace +1), (NumberToReplace +2, NumberToReplace +2)]]
            for direction, walls in enumerate(RelativePos):
                List_to_add = []
                if walls[1][0] == -1 or walls[1][0] == NumberToReplace:
                    FixAxis = 0
                else:
                    FixAxis = 1
                for pos in walls:
                    for repeat in range(len_walls -1):
                        new_posX, new_posY = pos
                        if FixAxis == 0:
                            if new_posX == -1:
                                new_posX = -(repeat +2)
                            elif new_posX == NumberToReplace:
                                new_posX = NumberToReplace + repeat +1
                        elif FixAxis == 1:
                            if new_posY == -1:
                                new_posY = -(repeat +2)
                            elif new_posY == NumberToReplace:
                                new_posY = NumberToReplace + repeat +1
                        List_to_add.append((new_posX, new_posY))
                List_to_add = List_to_add + Cases_to_add[direction]
                RelativePos[direction] = RelativePos[direction] + List_to_add[:]
            Cases_width = Cases_width + len_walls -1

        Laby = pygame.Surface((Dims[0]*Cases_width +1, Dims[1]*Cases_width +1))
        Laby.fill((255, 255, 255))
        for X in range(Dims[0]):
            for Y in range(Dims[1]):
                for num_side, side in enumerate(Walls[X][Y]):
                    if side:
                        for relative_pos in RelativePos[num_side]:
                            Laby.set_at((X*Cases_width +1 + relative_pos[0], Y*Cases_width +1 + relative_pos[1]), (0, 0, 0))
        if len_walls == 3:
            Laby_extern_wall = (Dims[0]*Cases_width -2, Dims[1]*Cases_width -2)
            for X in range(Laby_extern_wall[0]):
                Laby.set_at((X, 0), (0, 0, 0))
                Laby.set_at((X, Laby_extern_wall[1]), (0, 0, 0))
            for Y in range(Laby_extern_wall[1]):
                Laby.set_at((0, Y), (0, 0, 0))
                Laby.set_at((Laby_extern_wall[0], Y), (0, 0, 0))
        if Show_most_distants_points:
            if len_paths == 1:
                Laby.set_at((MostDistantsPoints[0][0]*Cases_width +1, MostDistantsPoints[0][1]*Cases_width +1), (255, 0, 0))
                Laby.set_at((MostDistantsPoints[1][0]*Cases_width +1, MostDistantsPoints[1][1]*Cases_width +1), (255, 0, 0))
            else:
                Laby.fill((255, 0, 0), (MostDistantsPoints[0][0]*Cases_width +1, MostDistantsPoints[0][1]*Cases_width +1, len_paths, len_paths))
                Laby.fill((255, 0, 0), (MostDistantsPoints[1][0]*Cases_width +1, MostDistantsPoints[1][1]*Cases_width +1, len_paths, len_paths))
    Laby_to_blit = pygame.Surface((Laby.get_width() -(len_walls -1), Laby.get_height() -(len_walls -1)))
    Laby_to_blit.blit(Laby, [0, 0, Laby.get_width(), Laby.get_height()], [0, 0, Laby.get_width(), Laby.get_height()])

    screen.blit(Laby_to_blit, [round(screen.get_width()/2 - Laby_to_blit.get_width()/2), round(screen.get_height()/2 - Laby_to_blit.get_height()/2), Laby_to_blit.get_width(), Laby_to_blit.get_height()], [0, 0, Laby_to_blit.get_width(), Laby_to_blit.get_height()])
    print(pygame.time.get_ticks())
    
    Mainloop = True
    while Mainloop:
        pygame.display.update()
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Mainloop = False

    if Save_image:
        try:
            Save_name = input("Sauvegarder l'image sous :\n")
            Save_name = "C:/Users/alexi/Documents/Fichiers python/fichiers/Personnel/Pratique/Générateur de labyrinthes/saves/" + Save_name + ".png"
            pygame.image.save(Laby_to_blit, Save_name, "PNG")
        except KeyboardInterrupt as err:
            print(err)


pygame.init()
Generate_Labyrinth(Dims, LabyParfait, Destroying_wall_chance, Show_most_distants_points, show_labyrinth, Save_image, Optimized, Path)