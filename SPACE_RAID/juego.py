#CONSTANTES Y FUNCIONES
from CONSTANTES import *

#IMPORTAMOS TODOS LOS OBJETOS
from obj_boton import Button
from obj_player import Player
from obj_enemy import Enemy
from obj_powerup import PowerUp
from obj_star import Star


pygame.init()

def main():
    #TRAIGO LAS VARIABLES PARA EL POWERUP DE VELOCIDAD
    global timer_iniciado,duracion_powerup,tiempo_colision

    #SELECCIONO LA MUSICA DE FONDO
    musica_juego()

    #FUNCION PARA RE-DIBUJAR LA VENTANA
    def redraw_window():
        #TRAIGO LAS VARIABLES PARA EL POWERUP DE VELOCIDAD
        global timer_iniciado,tiempo_colision,duracion_powerup

        #MOSTRAR EL FONDO JUEGO
        VENTANA.blit(BG, (0,0))

        #MOSTRAR EL HUD
        lives_label = main_font.render(f"VIDAS: {player.lives}", 1, ROJO)
        level_label = main_font.render(f"LEVEL: {player.level}", 1, ROSA_AGUA)
        score_label = main_font.render(f"SCORE: {player.score}", 1, AMARILLO)

        VENTANA.blit(lives_label, (10, 10))
        VENTANA.blit(level_label, (ANCHO - level_label.get_width() - 10, 10))
        VENTANA.blit(score_label,(ANCHO/2 - level_label.get_width() - 10, 10))

        #CRONOMETRO PARA PICKUP VELOCIDAD
        for power_up in power_ups:

            power_up.update(power_ups,player,VENTANA)
            power_up.draw(VENTANA)
            if power_up.timer_iniciado:

                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = tiempo_actual - power_up.tiempo_colision
                tiempo_restante = max(power_up.duracion_powerup - tiempo_transcurrido, 0)

                segundos_restantes = tiempo_restante // 1000
                time_powerup_label = main_font.render(f"Tiempo restante: {segundos_restantes:02}", 1, VERDE)
                VENTANA.blit(time_powerup_label, (10, 550))

                if tiempo_restante == 0:
                    #CUANDO TERMINA EL POWER-UP VUELVE A SETEAR LOS VALORES A LO NORMAL
                    player.vel = 5
                    player.laser_vel = 7
                    player.COOLDOWN = 30
                    power_up.timer_iniciado = False
                    #LA BANDERA HACE QUE NO SE PUEDA PICKEAR OTRO SI TENES UNO YA PUESTO.
                    PowerUp.bandera_powerup_azul = 1
                    power_ups.remove(power_up)
                    

        #RE-DIBUJAR ENEMIGO
        for enemy in enemies:
            enemy.update(enemies,player,VENTANA)
            enemy.draw(VENTANA)

        #RE-DIBUJAR ESTRELLAS
        for star in stars:
            star.move()
            star.draw(VENTANA)

        #RE-DIBUJAR PLAYER     
        player.update()
        player.move_lasers()
        player.draw(VENTANA)

        pygame.display.update()

    #CREA LAS ESTRELLAS
    stars = []
    for _ in range(50):  #NUMERO DE ESTRELLAS
        stars.append(Star())


    """JUGADOR"""

    #STEAR (SE RESETEAN LAS STATS PARA CUANDO PIERDA Y VUELVA A JUGAR.)
    player.health = 100
    player.level = 0
    player.score = 0
    player.laser_vel = 4
    player.vel = 7
    player.lives = 3
    PowerUp.bandera_powerup_azul = 1

    """ENEMIGOS"""
    #LISTA ENEMIGOS
    enemies = []
    #WAVE DE ENEMIGOS
    wave_length = 10

    """POWER-UPS"""
    #LISTA POWER_UPS
    power_ups = []
    #WAVE DE POWERUPS
    power_up_length = random.randrange(2, 5)


    run = True
    
    while run:

        #FPS 60
        clock.tick(FPS)
        #RE-DIBUJA LA PANTALLA
        redraw_window()
        #CONTROLES PARA EL VOLUMEN DE LA MUSICA DE FONDO
        musica_controles()

        #SI EL JUGADOR PIERDE TODAS LAS VIDAS O SE QUEDA SIN VIDA Y EXPLOTA, PIERDE.
        if player.lives <= 0 or player.health <= 0:
            #LLAMA A LA PANTALLA DE PERDIDA, QUE DSPS LLAMA A HIGHSCORE SI ES MAYOR A ALGUNO DEL TOP 5
            loss()

        #CREA LA LISTA DE ENEMIGOS
        if len(enemies) == 0:
            #SUBE EL LVL A 1
            player.level += 1
            #INCREMENTA LA WAVE EN 1, POR CADA NIVEL QUE PASE
            wave_length += 1
            #MUESTRA LA PANTALLA DE "LEVEL - "
            show_level_screen()

            for i in range(wave_length):

                #DESDE LVL 1 HASTA LVL 3
                #CREA LAS NAVES ALEATORIAS (RED,BLUE,GREEN)
                if player.level == 0 or player.level <= 3:

                    enemy = Enemy(random.randrange(50, ANCHO-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)

                #DESDE LVL 4 HASTA LVL 6
                if player.level > 3 and player.level <=6:
                    #CREA LAS NAVES ALEATORIAS (RED,BLUE,GREEN,RED_2,BLUE_2,GREEN_2)
                    enemy = Enemy(random.randrange(50, ANCHO-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green","red_2","blue_2","green_2"]))
                    enemies.append(enemy)

                #DESDE LVL 7
                if player.level > 6:
                    #CAMBIO: INCREMENTA EL DOBLE DE NAVES POR CADA NIVEL
                    wave_length += 2
                    enemy = Enemy(random.randrange(50, ANCHO-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green","red_2","blue_2","green_2"]))
                    enemies.append(enemy)
            #AL TERMINAR LA WAVE, LLEGA A 0 Y VUELVE A ENTRAR AL BUCLE.
            #RESET DE LOS VALORES PARA EL SIGUIENTE NIVEL.
            power_ups = []
            player.vel = 5
            player.laser_vel = 7
            player.COOLDOWN = 30
            PowerUp.bandera_powerup_azul = 1
            player.lasers = []
            player.x = 385
            player.y = 500

        #CREA LA LISTA DE POWER_UPS
        if len(power_ups) == 0:

            for i in range(power_up_length):
                #CREA LOS POWER UPS ALEATORIOS (RED,BLUE,GREEN,GREEN_2)
                power_up = PowerUp(random.randrange(50, ANCHO-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green","green_2"]))

                power_ups.append(power_up)

        #EVENTO DEL MAIN, POR SI QUITEA
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausa()

#CREO EL PLAYER.
player = Player(385,500)

def main_menu():
    run = True
    while run:
        #CONTROLES PARA EL VOLUMEN DE LA MUSICA DE FONDO
        musica_controles()
        #MOSTRAR EL FONDO JUEGO
        VENTANA.blit(BG_MENU, (0,0))
        #MUESTRA EL CARTEL DE INICIO MENU DEL JUEGO
        game_label = game_font.render("SPACE RAID", 1, ROSA)
        welcome_label = title_font.render("Bienvenido a ...", 1, BLANCO)

        VENTANA.blit(game_label, (ANCHO/2 - game_label.get_width()/2, 100))
        VENTANA.blit(welcome_label, (250, 50))

        
        #CONSIGO LA POSICION DEL MOUSE
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #LOS BOTONES DEL MENU : SIN IMAGEN,POSICION,TEXTO,FUENTE Y TAMAÑO,COLOR ESTATICO,COLOR CLICK ENCIMA.
        #BOTONES: PLAY, INSTRUCCIONES , HIGHSCORE, QUIT
        PLAY_BUTTON = Button(image=None, pos=(400, 300), 
                            text_input="JUGAR", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)
        
        INSTRUCCIONES_BUTTON = Button(image=None, pos=(400, 350), 
                            text_input="INSTRUCCIONES", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)
        
        HIGHSCORE_BUTTON = Button(image=None, pos=(400, 400), 
                            text_input="HIGH-SCORES", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)
        
        QUIT_BUTTON = Button(image=None, pos=(400, 450), 
                            text_input="SALIR", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)
        
        #PARA CADA BOTON, CAMBIAR EL COLOR CON EL MOUSE ENCIMA Y UPDATEAR
        for button in [PLAY_BUTTON, INSTRUCCIONES_BUTTON, QUIT_BUTTON, HIGHSCORE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(VENTANA)

        #EVENTOS DEL MENU_PRINCIPAL
        for event in pygame.event.get():
            #EVENTO POR SI QUITEA CON LA "X"
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #EVENTO POR SI CLICKEA LOS BOTONES
            if event.type == pygame.MOUSEBUTTONDOWN:
                #BOTON PLAY
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #SONIDO DE BOTON Y DIRIGE AL MAIN
                    boton_sonido()
                    main()
                #BOTON INSTRUCCIONES
                if INSTRUCCIONES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #SONIDO DE BOTON Y DIRIGE A LAS INSTRUCCIONES
                    boton_sonido()
                    instrucciones()
                #BOTON HIGHSCORE
                if HIGHSCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #SONIDO DE BOTON Y DIRIGE A LOS HIGHSCORES
                    boton_sonido()
                    highscores()
                #BOTON QUIT
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #SONIDO DE BOTON Y SALE DEL JUEGO
                    boton_sonido()
                    pygame.quit()

                    quit()
        #ACTUALIZO LA PANTALLA
        pygame.display.update()

def pausa():
    run = True
    pygame.mixer.music.pause()
    while run:
        #CONTROLES PARA EL VOLUMEN DE LA MUSICA DE FONDO
        musica_controles()
        #CONSIGO LA POSICION DEL MOUSE
        INSTRUCCIONES_MOUSE_POS = pygame.mouse.get_pos()
        #MUESTRO EL BOTON VOLVER

        lost_label = get_font(60).render("PAUSA", True, BLANCO)
        lost_rect = lost_label.get_rect(center=(400, 300))
        VENTANA.blit(lost_label, lost_rect)

        CONTINUAR = Button(image=None, pos=(650, 540), 
                            text_input="CONTINUAR", font=get_font(30), base_color=VERDE, hovering_color=BLANCO)
        CONTINUAR.changeColor(INSTRUCCIONES_MOUSE_POS)
        CONTINUAR.update(VENTANA)

        SALIR = Button(image=None, pos=(175, 540), 
                            text_input="SALIR AL MENU", font=get_font(30), base_color=ROJO_ERROR, hovering_color=BLANCO)

        SALIR.changeColor(INSTRUCCIONES_MOUSE_POS)
        SALIR.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUAR.checkForInput(INSTRUCCIONES_MOUSE_POS):

                    boton_sonido()
                    pygame.mixer.music.play(-1)
                    run = False

                if SALIR.checkForInput(INSTRUCCIONES_MOUSE_POS):
                    boton_sonido()
                    musica()
                    main_menu()

        pygame.display.update()

def instrucciones():

    while True:
        #CONTROLES PARA EL VOLUMEN DE LA MUSICA DE FONDO
        musica_controles()
        #CONSIGO LA POSICION DEL MOUSE
        INSTRUCCIONES_MOUSE_POS = pygame.mouse.get_pos()
        #MUESTRO EL BOTON VOLVER
        VENTANA.blit(BG_INSTRUCCIONES, (0,0))
        INSTRUCCIONES_BACK = Button(image=None, pos=(700, 540), 
                            text_input="VOLVER", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)

        INSTRUCCIONES_BACK.changeColor(INSTRUCCIONES_MOUSE_POS)
        INSTRUCCIONES_BACK.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCCIONES_BACK.checkForInput(INSTRUCCIONES_MOUSE_POS):
                    boton_sonido()
                    main_menu()

        pygame.display.update()

def highscores():

    while True:
        musica_controles()
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        VENTANA.blit(BG_HIGHSCORE, (0,0))
        HIGHSCORE_TEXT = get_font(45).render("TOP 5 HIGHSCORES.", True, ROSA)
        HIGHSCORE_RECT = (70, 50)
        VENTANA.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)

        CARTEL = get_font(20).render("Ranking de puntuaciones de SPACE RAID.", True, CELESTE)
        CARTEL_RECT = (70, 125)
        VENTANA.blit(CARTEL, CARTEL_RECT)

        HIGHSCORE_BACK = Button(image=None, pos=(700, 540), 
                            text_input="VOLVER", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)

        HIGHSCORE_BACK.changeColor(PLAY_MOUSE_POS)
        HIGHSCORE_BACK.update(VENTANA)


        conexion = sqlite3.connect(os.path.join(carpeta_juego,"ranking.db"))
        cursor = conexion.cursor()

        #CREAR TABLA SI NO EXISTE
        cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        score INTEGER,
                        level INTEGER)''')

        #OBTIENE LOS REGISTROS ORDENADOS DE FORMA DESCENDIENTE
        cursor.execute("SELECT nombre, score, level FROM jugadores ORDER BY score DESC")

        resultados = cursor.fetchall()

        CARTEL2 = get_font(20).render((f"RANK     -     NOMBRE           -          SCORE    -    LVL"), True, ROSA_AGUA)
        CARTEL2_RECT = (100, 170)
        VENTANA.blit(CARTEL2, CARTEL2_RECT)

        for i, resultado in enumerate(resultados, start=1):
            nombre = resultado[0]
            score = resultado[1]
            level = resultado[2]

            LUGAR = get_font(20).render((f"     {i}."), True, ROJO_ERROR)
            LUGAR_RECT = (100, 170 + i * 55)
            VENTANA.blit(LUGAR, LUGAR_RECT)

            NOMBRE = get_font(20).render((f"{nombre}"), True, BLANCO)
            NOMBRE_RECT = (250, 170 + i * 55)
            VENTANA.blit(NOMBRE, NOMBRE_RECT)

            SCORE = get_font(20).render((f"{score}"), True, AMARILLO)
            SCORE_RECT = (500, 170 + i * 55)
            VENTANA.blit(SCORE, SCORE_RECT)

            LVL = get_font(20).render((f"      {level}"), True, VERDE)
            LVL_RECT = (620, 170 + i * 55)
            VENTANA.blit(LVL, LVL_RECT)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HIGHSCORE_BACK.checkForInput(PLAY_MOUSE_POS):
                    boton_sonido()
                    main_menu()

        pygame.display.update()

def loss():

    bandera_musica = 1
    pygame.mixer.music.stop()
    while True:
        musica_controles()
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        VENTANA.blit(BG_GAME_OVER, (0,0))

        lost_label = get_font(60).render("¡¡GAME OVER!!", True, ROJO_ERROR)
        lost_rect = lost_label.get_rect(center=(400, 300))
        VENTANA.blit(lost_label, lost_rect)

        LOST_CONTINUE = Button(image=None, pos=(670, 540), 
                            text_input="CONTINUAR", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)

        LOST_CONTINUE.changeColor(PLAY_MOUSE_POS)
        LOST_CONTINUE.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if LOST_CONTINUE.checkForInput(PLAY_MOUSE_POS):
                    boton_sonido()
                    ingresar_highscore()

        pygame.display.update()

        if bandera_musica == 1:
            pygame.time.delay(500)
            game_over_sonido()
            bandera_musica = 0


def ingresar_highscore():

    global error

    bandera_musica = 1


    conexion = sqlite3.connect(os.path.join(carpeta_juego,"ranking.db"))
    cursor = conexion.cursor()

    #CREA LA TABLA SI NO EXISTE
    cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    score INTEGER,
                    level INTEGER)''')

    #OBTIENE EL PUNTAJE MAS BAJO DE LOS PRIMEROS 5 DE LA BASE DE DATOS
    cursor.execute("SELECT MIN(score) FROM jugadores LIMIT 5")

    resultado = cursor.fetchone()
    puntaje_minimo = resultado[0] if resultado[0] is not None else 0
    nombre_jugador = ""
    ingresando_nombre = puntaje_minimo < 0 or puntaje_minimo < player.score
    cursor_visible = False
    cursor_tiempo = 0

    while ingresando_nombre:

        if error == 1:
            bandera_musica = 0
        if bandera_musica == 1:

            ingresar_highscore_sonido()
            bandera_musica = 0
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        VENTANA.blit(BG_INGRESAR_HIGHSCORE, (0,0))

        HIGHSCORE1_TEXT = get_font(60).render("Felicitaciones!!", True, ROSA)
        HIGHSCORE1_RECT = (70, 100)
        VENTANA.blit(HIGHSCORE1_TEXT ,HIGHSCORE1_RECT)

        HIGHSCORE2_TEXT = get_font(25).render("Has ingresado en el TOP 5!!", True, ROSA_AGUA)
        HIGHSCORE2_RECT = (150, 250)
        VENTANA.blit(HIGHSCORE2_TEXT,HIGHSCORE2_RECT)


        HIGHSCORE3_TEXT = get_font(25).render("Por favor, Ingrese su nombre.", True,BLANCO)
        HIGHSCORE3_RECT = (150, 300)

        VENTANA.blit(HIGHSCORE3_TEXT, HIGHSCORE3_RECT)

        HIGHSCORE_CONTINUAR = Button(image=None, pos=(670, 540), 
                            text_input="CONTINUAR", font=get_font(30), base_color=CELESTE, hovering_color=BLANCO)

        HIGHSCORE_CONTINUAR.changeColor(PLAY_MOUSE_POS)
        HIGHSCORE_CONTINUAR.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HIGHSCORE_CONTINUAR.checkForInput(PLAY_MOUSE_POS):
                    boton_sonido()
                    if validar_nombre(nombre_jugador) and len(nombre_jugador) <= 10:
                        #GUARDA LOS DATOS DEL JUGADOR EN LA TABLA SI SUS DATOS SON MAYOR QUE EL MINIMO
                        if player.score > puntaje_minimo:
                            #INSERTA LOS DATOS DEL JUGADOR EN LA TABLA
                            cursor.execute("INSERT INTO jugadores (nombre, score, level) VALUES (?, ?, ?)",
                                        (nombre_jugador, player.score, player.level))
                            conexion.commit()

                            #ELIMINA EL REGISTRO CON EL PUNTAJE MINIMO SI HAY MAS DE 5
                            cursor.execute("DELETE FROM jugadores WHERE score = ? AND ID NOT IN (SELECT ID FROM jugadores ORDER BY score DESC LIMIT 5)",
                                        (puntaje_minimo,))
                            conexion.commit()

                        #CIERRA LA CONEXION A LA BASE DE DATOS
                        conexion.close()

                        musica()
                        main_menu()
                    else:
                        error = 1
                        bandera_musica = 0
                        error_sonido()
                        ingresar_highscore()
                    
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_BACKSPACE: #FERIFICA SI PRESIONA LA TECLA PARA BORRAR
                    nombre_jugador = nombre_jugador[:-1] #LE RESTA UNA LETRA AL NOMBRE QUE ESTA ESCRIBIENDO
                else:
                    nombre_jugador += event.unicode

        #MUESTRA EL NOMBRE EN LA PANTALLA
        text = main_font.render(nombre_jugador, True, CELESTE)
        VENTANA.blit(text, (300, 375))

        #MUESTRA EL "." INTERMITENTE AL ESCRIBIR
        if pygame.time.get_ticks() - cursor_tiempo > 500:
            cursor_visible = not cursor_visible
            cursor_tiempo = pygame.time.get_ticks()

        if cursor_visible:
            cursor_surface = main_font.render(".", True, CELESTE)
            VENTANA.blit(cursor_surface, (300 + text.get_width(), 375))

        if error == 1:
            ERROR_TEXT = get_font(25).render("ERROR!. Solo ingresar letras o numeros!", True, ROJO_ERROR)
            ERROR_RECT = (30, 450)
            VENTANA.blit(ERROR_TEXT,ERROR_RECT)

            ERROR2_TEXT = get_font(25).render("10 caracteres como maximo!!", True, ROJO_ERROR)
            ERROR2_RECT = (30, 500)
            VENTANA.blit(ERROR2_TEXT,ERROR2_RECT)


        pygame.display.update()
    
    musica()

    main_menu()

    

        

    
def show_level_screen():

        VENTANA.blit(BG_LEVEL, (0,0))
        level_label = main_font.render(f"LEVEL: {player.level}", 1, ROSA_AGUA)
        VENTANA.blit(level_label, (ANCHO/2 - level_label.get_width()/2, ALTO/2 - level_label.get_height()/2))
        pygame.display.update()
        level_up = pygame.mixer.Sound(os.path.join(carpeta_audio_menu,"LEVEL_UP.mp3"))
        level_up.play(0)

        pygame.time.delay(2000)                       

musica()
main_menu()



