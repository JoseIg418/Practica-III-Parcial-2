from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

#Importar imagenes 
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')

#Importar audio
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)

#Eliminar subrayado de la ventana
window.fps_counter.enabled = False
#Agregar la x para salir del juego
window.exit_button.visible = True

block_pick = 1
#Funcion para elegir el tipo de bloque
def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.activate()
    else:
        hand.pasive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2 
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4     

#La clase voxel del juego
class Voxel(Button):
    def __init__(self, position= (0,0,0), texture= stone_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block' ,
            origin_y = 0.5,
            texture = texture,
            color = color.hsv(0,0, random.uniform(0.9,1)),
            scale = 1)

    def input(self, key):
        #Establecer el hovered para trabajar con teclado
        if self.hovered:
            #Click izquierdo se crea cubo
            if key == 'left mouse down':
                #Click izquierdo reproduce sonido
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

           # click derecho, se destruye bloque
            if key == 'right mouse down':
                 #Click derecho reproduce sonido
                punch_sound.play()
                destroy(self)

#crear clase para el cielo
class Sky(Entity):
    def __init__(self):
            super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 250,
            #se fija que el cielo sea exterior
            double_sided = True
        )   
                      
#Se crea clase para la mano del personaje
class Hand(Entity):
    def __init__(self):
        super().__init__(
            #Se establece la clase de la cual se hereda, en este caso la vista 3D
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            #Se establece la posicion tanto 3D como 2D
            rotation = Vec3(150, -10,0),
            position = Vec2(0.4, -0.6)

        )        

 #Se crea una nueva posición de la mano cuando hace click(movimiento)
    def activate(self):
        self.position = Vec2(0.3, -0.5)
#Se crea una nueva posición de la mano cuando no hace click(movimiento al origen)
    def pasive(self):
        self.position = Vec2(0.4, -0.6)

#Se crea el escenario para el juego por medio de dos bucles que iteran uno dentro del otro
for z in range(120):
    for x in range(120):
        #Se va cambiando la posicion de cda voxel para la plataforma
        voxel = Voxel(position= (x,0,z))

#Se crea el jugador desde vista primera persona
player = FirstPersonController()
player.scale = 2

#Se inicia cielo y mano
sky = Sky()
hand = Hand()



app.run()