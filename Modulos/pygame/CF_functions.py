# Funciones de colisiones
def collision_detect(rect, grids):
    '''
    Si rect colisiona con uno o mas coliders/grids, estas se agregaran a la lista de hits "hit_list"
    Devuelve una lista
    '''
    hit_list = []
    for grid in grids:
        if rect.colliderect(grid):
            hit_list.append(grid)
    return hit_list


def collision_move_original(rect, movement, grids):
    ''''
    Cuando "rect" colisione con algun "grid", dependiendo de la dirección de su colision, el "rect" se posicionara de forma inversa a la dirección de colisión.
    - Si rect colisiona del lado derecho del tile, este se movera a su lado izquierdo.
    - Si rect colisiona del lado izquiedo del tile, este se movera a su lado derecho.
    - Si rect colisiona del lado inferior del tile, este se movera a su lado superior.
    - Si rect colisiona del lado superior del tile, este se movera a su lado inferior.
    '''
    collision_types = {'top':False, 'bottom':False, 'right':False, 'left': False}

    # Movimiento dimención x
    rect.x += movement[0]
    hit_list = collision_detect(rect, grids)
    for grid in hit_list:
        if movement[0] > 0:
            rect.right = grid.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = grid.right
            collision_types['left'] = True
    
    # Movimiento dimención y
    rect.y += movement[1]
    hit_list = collision_detect(rect, grids)
    for grid in hit_list:
        if movement[1] > 0:
            rect.bottom = grid.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = grid.bottom
            collision_types['top'] = True
    
    return rect, collision_types




def collide_and_move( obj=None, obj_movement=[0,0], solid_objects=None):
    '''
    Esta función collisiona y mueve un objeto tipo "pygame.sprite.Sprite()"
    
    Para esta función se necesita del siguiente objeto, con estos atributos:
    Objeto tipo "pygame.sprite.Sprite"
    self.rect
    Este objeto lo utilizaremos para el parametro:
    obj=objeto

    Tambien se necesita una lista de dos valores, que haran la función de movimiento del jugador.
    obj_movement = [0, 0]
    El primer valor de la lista seria el movimiento "x" y el segundo valor de la lista el movimiento "y"
    
    solid_objects, es una lista de objetos que teinen los siguientes atributos:
    Objetos tipo pygame.sprite.Sprite()
    self.rect
    solid_objects = lista_de_objetos
    


    Cuando "obj" colisione con algun "solid_objects", dependiendo de la dirección de su colision, el "obj" se posicionara de forma inversa a la dirección de colisión.
    Primero obj se mueve en dirección "x" si obj_movement[0] es menor o meyor a cero.
    Y se determina lo siguiente:
    - Si obj colisiona del lado derecho del solid_object, este se movera a su lado izquierdo.
    - Si obj colisiona del lado izquiedo del solid_object, este se movera a su lado derecho.
    
    Despues obj se mueve en dirección "y" si obj_movement[1] es menor o meyor a cero, y se determina lo siguiente:
    Y se determina lo siguiente:
    - Si obj colisiona del lado inferior del solid_object, este se movera a su lado superior.
    - Si obj colisiona del lado superior del solid_object, este se movera a su lado inferior.
    '''
    collided_side = None

    obj.rect.x += obj_movement[0]
    for solid in solid_objects:
        if obj.rect.colliderect( solid.rect ):
            if obj_movement[0] > 0:
                obj.rect.right = solid.rect.left
                collided_side = 'right'
            elif obj_movement[0] < 0:
                obj.rect.left = solid.rect.right
                collided_side = 'left'
        
    obj.rect.y += obj_movement[1]
    for solid in solid_objects:
        if obj.rect.colliderect( solid.rect ):
            if obj_movement[1] > 0:
                obj.rect.bottom = solid.rect.top
                collided_side = 'bottom'
            elif obj_movement[1] < 0:
                obj.rect.top = solid.rect.bottom
                collided_side = 'top'
    
    return collided_side