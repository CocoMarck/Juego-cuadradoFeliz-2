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


def collision_move(rect, movement, grids):
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