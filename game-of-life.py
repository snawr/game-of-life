import pygame
import numpy as np
import random

### TODO ###


### INIT ###
pygame.font.init()

game_width, game_height = 1200, 800
lower_bar_size = 40
side_bar_size = 200

button_size = (int(0.7*side_bar_size), int(0.4*side_bar_size))

win_width, win_height = game_width+side_bar_size, game_height+lower_bar_size

pixel_size = 10
FPS = 60
generation_time = 1
start_simulation = False

width, height = game_width//pixel_size, game_height//pixel_size

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Game of life")

gui_font = pygame.font.SysFont('Arial', 18)
button_font = pygame.font.SysFont('Arial', 16)

white_color = (255,255,255)
light_gray_color = (201, 201, 199)
dark_gray_color = (110, 110, 110)
black_color = (0, 0, 0)
yellow_color = (243, 250, 35)
light_yellow_color = (255, 255, 102)
blue_color = (10, 60, 209)
light_blue_color = (79, 204, 247)
lighter_blue_color = (165, 228, 250)


# buttons variables
button_posx = game_width + (win_width-game_width)//2 - button_size[0]//2

random_seed_button_posy = int(min(0.05*game_height,15))
random_seed_button_text = 'Random seed'

clear_button_posy = int(random_seed_button_posy + button_size[1] + min(0.05*game_height,15))    #do zmiany - dla wiekszej ilosci przyciskow
clear_button_text = 'Clear'

run_stop_button_posy = int(game_height - button_size[1] - 15)
run_stop_button_text = ('Run', 'Pause')

def randomize_array(main_array, width, height, density=0.3):

    for row in range(width):
        for col in range(height):
        
            main_array[row, col] = int((random.random() + density))
        
def evolve(mask):

    count = 0
    for ind_r, row in enumerate(mask):
        for ind_c, column in enumerate(row):
            if not (ind_r == 1 and ind_c == 1):
                count += mask[ind_r, ind_c]
                
    if mask[1, 1] == 1:
        if count < 2:
            # print('<2')
            return 0

        elif count in (2,3):
            # print('2 3')
            return 1

        elif count >3:
            # print('>3')
            return 0

    else:
        if count == 3:
            # print('zmartywchwstanie')
            return 1
        else:
            return 0


def new_generation(frame): 

    new_frame = np.zeros( (width, height)).astype(np.int64)

    for ind_r, row in enumerate(frame):
        for ind_c, column in enumerate(row):

            mask = np.zeros((3,3))
            
            # if ind_r == 0 or ind_r == width-1 or ind_c == 0 or ind_c == height-1:     #sticky borders
            #     new_frame[ind_r, ind_c] = frame[ind_r, ind_c]

            if ind_r == 0:                                              #find smarter way to handle border pixels
                if ind_c == 0:  #upper left
                    np.copyto(mask[1:3,1:3], frame[ind_r:ind_r+2,ind_c:ind_c+2])
                    new_frame[ind_r, ind_c] = evolve(mask)
                elif ind_c == height-1: #upper right
                    np.copyto(mask[1:3,0:2], frame[ind_r:ind_r+2,ind_c-1:ind_c+1])
                    new_frame[ind_r, ind_c] = evolve(mask)
                else:   #upper
                    np.copyto(mask[1:3,0:3], frame[ind_r:ind_r+2,ind_c-1:ind_c+2])
                    new_frame[ind_r, ind_c] = evolve(mask)

            elif ind_c == 0:    
                if ind_r == width-1:    #lower left
                    np.copyto(mask[0:2,1:3], frame[ind_r-1:ind_r+1,ind_c:ind_c+2])
                    new_frame[ind_r, ind_c] = evolve(mask)
                else:   #left
                    np.copyto(mask[0:3,1:3], frame[ind_r-1:ind_r+2,ind_c:ind_c+2])
                    new_frame[ind_r, ind_c] = evolve(mask)

            elif ind_r == width-1:
                if ind_c == height-1:   #lower right
                    np.copyto(mask[0:2,0:2], frame[ind_r-1:ind_r+1,ind_c-1:ind_c+1])
                    new_frame[ind_r, ind_c] = evolve(mask)
                else:   #lower
                    np.copyto(mask[0:2,0:3], frame[ind_r-1:ind_r+1,ind_c-1:ind_c+2])
                    new_frame[ind_r, ind_c] = evolve(mask)

            elif ind_c == height-1: #right
                np.copyto(mask[0:3,0:2], frame[ind_r-1:ind_r+2,ind_c-1:ind_c+1])
                new_frame[ind_r, ind_c] = evolve(mask)

            else:   
                np.copyto(mask, frame[ind_r-1:ind_r+2,ind_c-1:ind_c+2])
                new_frame[ind_r, ind_c] = evolve(mask)

    return new_frame

def update_grid(resolution, main_array, position, value):

    pos_x = int(((game_width)//resolution)*(position[0]/(game_width)))
    pos_y = int(((game_height)//resolution)*(position[1]/(game_height)))
    main_array[pos_x, pos_y] = value
    return main_array

def gui():
    
    text_pause = gui_font.render('SPACE to run/pause', 1, white_color)
    window.blit(text_pause, (4, win_height - text_pause.get_height()))
    text_left_mouse = gui_font.render('Left mouse button to draw', 1, white_color)
    window.blit(text_left_mouse, (text_pause.get_width() + 30, win_height - text_left_mouse.get_height()))
    text_right_mouse = gui_font.render('Right mouse button to erase', 1, white_color)
    window.blit(text_right_mouse, (text_pause.get_width() + text_left_mouse.get_width() + 60, win_height - text_right_mouse.get_height()))
    text_generation_count = gui_font.render('GENERATION: '+ str(generation_count), 1, white_color)
    window.blit(text_generation_count, (game_width - text_generation_count.get_width(), win_height - text_generation_count.get_height()))

def render_button(posx, posy, width, height, text, runcolor = light_gray_color):

    button_rect = pygame.Rect(posx, posy, width, height)
    if start_simulation:
        pygame.draw.rect(window, runcolor, button_rect)

    else:
        pygame.draw.rect(window, lighter_blue_color, button_rect)

    text_button = button_font.render(text, 1, black_color)
    window.blit(text_button, (posx + (width//2) - (text_button.get_width()//2), posy + (height//2) - (text_button.get_height()//2)))

def button_pressed(button, pos):

    if button=='RANDOM':
        if pos[0] in range (button_posx, button_posx + button_size[0]) and pos[1] in range (random_seed_button_posy, random_seed_button_posy + button_size[1]):
            return True
    if button=='CLEAR':
        if pos[0] in range (button_posx, button_posx + button_size[0]) and pos[1] in range (clear_button_posy, clear_button_posy + button_size[1]):
            return True
    
    if button=='RUN/STOP':
        if pos[0] in range (button_posx, button_posx + button_size[0]) and pos[1] in range (run_stop_button_posy, run_stop_button_posy + button_size[1]):
            return True

def draw_outline(offset=4):

    outline_rect = pygame.Rect(0, 0, game_width+2*offset, game_height+2*offset)
    if start_simulation:
        pygame.draw.rect(window, yellow_color, outline_rect, offset)
    else:
        pygame.draw.rect(window, light_blue_color, outline_rect, offset)

def draw_grid(resolution, main_array, offset=4):

    for x_ind, row in enumerate(main_array):
        for y_ind, cell in enumerate(row):
            if cell == 1:
                cell_rect = pygame.Rect(x_ind*resolution+1+offset, y_ind*resolution+1+offset, resolution-1, resolution-1)
                pygame.draw.rect(window, white_color, cell_rect)

def draw_window(resolution, main_array):

    offset = 4
    window.fill(black_color)
    draw_grid(resolution, main_array, offset)
    draw_outline(offset)
    gui()
    render_button(button_posx, random_seed_button_posy, button_size[0], button_size[1], random_seed_button_text)
    render_button(button_posx, clear_button_posy, button_size[0], button_size[1], clear_button_text)
    if start_simulation==True:
        render_button(button_posx, run_stop_button_posy, button_size[0], button_size[1], run_stop_button_text[1], light_yellow_color)
    else:
        render_button(button_posx, run_stop_button_posy, button_size[0], button_size[1], run_stop_button_text[0])

    pygame.display.update()


def main():

    global main_array
    global start_simulation
    global generation_count

    main_array = np.zeros((width, height)).astype(np.int64)
    generation_count = 0

    clock = pygame.time.Clock()
    run = True
    tick = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        draw_window(pixel_size, main_array)
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if not start_simulation:

            if click[0] == True:    #left button pressed - continous
                if pos[0]<game_width and pos[1]<game_height:
                    main_array = update_grid(pixel_size, main_array, pos, 1)
                    generation_count=0
                    
            
            if click[1] == True:    #right button pressed
                if pos[0]<game_width and pos[1]<game_height:
                    main_array = update_grid(pixel_size, main_array, pos, 0)
                    generation_count=0

                draw_window(pixel_size, main_array)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and main_array.any():    #if space was pressed and array has any elements
                    start_simulation = not start_simulation

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                
                if not start_simulation:

                    if event.button == 1:    #left button pressed - single

                        if button_pressed('RANDOM', pos):
                            randomize_array(main_array, width, height)
                            generation_count = 0

                        elif button_pressed('CLEAR', pos):
                            main_array = np.zeros((width, height)).astype(np.int64)
                            generation_count = 0
                        
                        elif button_pressed('RUN/STOP', pos) and main_array.any():
                            start_simulation = True
                            

                        draw_window(pixel_size, main_array)

            
                elif event.button == 1:    #left button pressed
                    if button_pressed('RUN/STOP', pos):
                        start_simulation = False
                            


        if (pygame.time.get_ticks() - tick) >= generation_time and start_simulation:
            
            if not main_array.any():
                start_simulation = False
            else:
                draw_window(pixel_size, main_array)
                main_array = new_generation(main_array)
                generation_count += 1
                tick = pygame.time.get_ticks()
            

    pygame.quit()



if __name__ == "__main__":
    main()
