import pygame,sys
from pygame.locals import *
from random import randint
import time


ancho = 900
alto = 480 
listaEnemigo = []


class personaje(pygame.sprite.Sprite):
	"""clase para las naves"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load('Imagenes/Bear3.png')
		self.ImagenExplosion = pygame.image.load('Imagenes/Bearbaneado.png')

		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = ancho/2
		self.rect.centery = alto - 35
	
		self.listaDisparo = []
		self.Vida = True
		self.speed = 50

		#Sonidos
		#self.sonidoDisparo = pygame.mixer.Sound('Sonidos/Comanpapas.mp3')
		#self.sonidoExplosion =  pygame.mixer.Sound('Sonidos/Baneado.mp3')

	"""Nuevos Cambios(Metodos)"""
	def movimientoDerecha(self):
		self.rect.right += self.speed
		self.__movimiento()

	def movimientoIzquierda(self):
		self.rect.left -= self.speed
		self.__movimiento()

	def __movimiento(self):
		if self.Vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.right > 900:
				self.rect.right = 900

	def disparar(self,x,y):
		miMisil = misil(x,y, "Imagenes/papas.png", True)
		self.listaDisparo.append(miMisil)
		#self.sonidoDisparo.play()

	def destruccion(self):
		#self.sonidoExplosion.play()
		self.Vida = False
		self.speed = 0
		self.ImagenNave = self.ImagenExplosion


	def dibujar(self,superficie):
		superficie.blit(self.ImagenNave, self.rect)

class misil(pygame.sprite.Sprite):
	def __init__(self, posx, posy, ruta, heroe):
		pygame.sprite.Sprite.__init__(self)

		self.imagenMisil = pygame.image.load(ruta)

		self.rect = self.imagenMisil.get_rect()

		self.Misilspeed = 5

		self.rect.top = posy
		self.rect.left = posx

		self.disparoHeroe = heroe

	def trayectoria(self):
		if self.disparoHeroe == True:
			self.rect.top = self.rect.top - self.Misilspeed
		else:
			self.rect.top = self.rect.top + self.Misilspeed

	def dibujar(self, superficie):
		superficie.blit(self.imagenMisil, self.rect)

class Invasor(pygame.sprite.Sprite):
	
	def __init__(self, posx, posy, distancia, ImagenUno, ImagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenEnemigo1 = pygame.image.load(ImagenUno)
		self.imagenEnemigo2 = pygame.image.load(ImagenDos)
		
		self.listaImagenes = [self.imagenEnemigo1, self.imagenEnemigo2]
		self.posImagen = 0
		self.imagenInvasor = self.listaImagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()

		self.listaDisparo = []
		self.speed = 10

		self.rect.top = posy
		self.rect.left = posx
		self.rangoDisparo = 3
		self.tiempoCambio = 1
		self.conquista = False

		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 50

		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx - distancia


	def dibujar(self, superficie):
		self.imagenInvasor = self.listaImagenes[self.posImagen]
		superficie.blit(self.imagenInvasor, self.rect)

	def comportamiento(self, tiempo):
		if self.conquista == False:
			self.__movimientos()
			self.__ataque()

			if self.tiempoCambio == tiempo:
				self.posImagen +=1
				self.tiempoCambio +=1

				if self.posImagen < len(self.listaImagenes) - 1:
					self.posImagen = 0

	def __movimientos(self):
		if self.contador < 1:
			self.__movimientoLateral()
		else:
			self.__descenso()

	def __descenso(self):
		if self.Maxdescenso == self.rect.top:
			self.contador = 0
			self.Maxdescenso = self.rect.top + 8 #Velocidad con la que baja
		else:
			self.rect.top += 1

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.speed
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
				

		else:
			self.rect.left = self.rect.left - self.speed
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

				self.contador +=1

	def __ataque(self):
		if (randint(0,600)<self.rangoDisparo):
			self.__bala()

	def __bala(self):
		x,y = self.rect.center
		miMisil = misil(x,y, "Imagenes/Banned.png", False)
		self.listaDisparo.append(miMisil)

def pause():

    paused = True
    pygame.mixer.music.pause()


    while paused:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    pygame.mixer.music.unpause()

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def detenerTodo():
	for Invasor in listaEnemigo:
		for disparo in Invasor.listaDisparo:
			Invasor.listaDisparo.remove(disparo)

		Invasor.conquista = True

def terminar():
	pygame.quit()
	sys.exit()

def esperarTecla():


	while True:

		for event in pygame.event.get():
			
			if event.type == QUIT:
				terminar()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminar()
				return


def pantallaFinal():
	final = True 
	while True:

		for event in pygame.event.get():
			
			if event.type == QUIT:
				terminar()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminar()
				return

	
def cargarEnemigos():

	posx = 70
	for x in range(1, 5):
		enemigo = Invasor(posx,0,50,'Imagenes/Enemigo2A.png', 'Imagenes/Enemigo2B.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200

	posx = 160
	for x in range (1, 5):
		enemigo = Invasor(posx,-100,50,'Imagenes/Enemigo3A.png','Imagenes/Enemigo3B.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200

	posx = 70
	for x in range (1, 5):
		enemigo = Invasor(posx,-200,50,'Imagenes/Enemigo4A.png','Imagenes/Enemigo4B.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200

	posx = 160
	for x in range (1, 5):
		enemigo = Invasor(posx,-300,50,'Imagenes/Enemigo5A.png','Imagenes/Enemigo5B.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200

	posx = 70
	for x in range (1, 5):
		enemigo = Invasor(posx,-400,50,'Imagenes/Enemigo6A.png','Imagenes/Enemigo6B.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200

	posx = 340
	for x in range (1, 2):
		enemigo = Invasor(posx,-800,50,'Imagenes/Enemigo7A.png','Imagenes/Enemigo7A.png',)
		listaEnemigo.append(enemigo)
		posx = posx + 200



	Inicio = pygame.display.set_mode((ancho,alto))
	ImagenInicio = pygame.image.load('Imagenes/Fondo1.png')
	Inicio.blit(ImagenInicio, (0,0))
	pygame.display.flip()


	esperarTecla()
	pygame.display.update()
	


def mainLoop():

	pygame.init()
	ventana = pygame.display.set_mode((ancho,alto))
	pygame.display.set_caption("Bear, el Oso Tierraplanista")
	ImagenFondo = pygame.image.load('Imagenes/Fondo.jpg')

	#Musica&Sonidos

	
	#Fuentes

	miFuenteSistema = pygame.font.SysFont("Arial",80)
	miFuenteSistema2 = pygame.font.SysFont("Arial",40)
	miFuenteSistema3 = pygame.font.SysFont("Arial",20)
	GameOver = miFuenteSistema.render("Te han baneado",1,(230, 30, 35))
	MenuPause = miFuenteSistema2.render("Pulsa P para reanudar o ESC para salir",1,(250,0,230))
	MenuFinal = miFuenteSistema3.render("Pulsa cualquier tecla para empezar o ESC para salir",1,(250,0,230))
	ImagenVictoria = miFuenteSistema.render("Puedes entrar al Cryptobar",1,(250,0,230))
	
	jugador = personaje()
	cargarEnemigos()

	inGame = True

	#Musica&Sonidos
	pygame.mixer.music.load('Sonidos/Intro.mp3')
	pygame.mixer.music.play(6)
	pygame.mixer.music.set_volume(0.1)

	#Aqui el reloj
	reloj = pygame.time.Clock()



	while True:

		reloj.tick(60)
		tiempo = pygame.time.get_ticks()/1000

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if inGame == True:
				if event.type == pygame.KEYDOWN:
					if event.key == K_LEFT:
						jugador.movimientoIzquierda()

					elif event.key == K_RIGHT:
						jugador.movimientoDerecha()

					elif event.key == K_s:
						x,y = jugador.rect.center
						jugador.disparar(x,y)

					elif event.key == K_p:
						pause()
			
			if inGame == False:
				for event in pygame.event.get():

					if event.type == QUIT:
						terminar()
						if event.type == KEYDOWN:
							if event.key == K_ESCAPE:
								terminar()
								return
					    



		ventana.blit(ImagenFondo, (0,0))	
		jugador.dibujar(ventana)

		if len(jugador.listaDisparo) > 0:
			for x in jugador.listaDisparo:
				x.dibujar(ventana)
				x.trayectoria()
				if x.rect.top <- 10:
					jugador.listaDisparo.remove(x)

				else:
					for enemigo in listaEnemigo:
						if x.rect.colliderect(enemigo.rect):
							listaEnemigo.remove(enemigo)
							jugador.listaDisparo.remove(x)

		if len(listaEnemigo) > 0:
			for enemigo in listaEnemigo:
				enemigo.comportamiento(tiempo)
				enemigo.dibujar(ventana)

				if enemigo.rect.colliderect(jugador.rect):
					jugador.destruccion()
					inGame = False
					detenerTodo()
					 #algo para acabar el juego cuando mueres

				if len(enemigo.listaDisparo) > 0:
					for x in enemigo.listaDisparo:
						x.dibujar(ventana)
						x.trayectoria()
						if x.rect.colliderect(jugador.rect):
							jugador.destruccion()
							inGame = False
							detenerTodo()

						if x.rect.top > 900:
							enemigo.listaDisparo.remove(x)		
						
						else:
							for disparo in jugador.listaDisparo:
								if x.rect.colliderect(disparo.rect):
									jugador.listaDisparo.remove(disparo)
									enemigo.listaDisparo.remove(x)

		if inGame == False:
			
			pygame.mixer.music.fadeout(6000)
			ventana.blit(GameOver,(165,235))
		
			ventana.blit(MenuFinal, (220,320))
			
			esperarTecla()

					
			
		pygame.display.update()
		
mainLoop()
