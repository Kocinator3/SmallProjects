import pygame
import math
import json
import os
import numpy

pygame.init()
default_width, default_height = 800,600
width, height = default_width, default_height
luncher = True
editing = False
run = True

window = pygame.display.set_mode((default_width, default_height))
pygame.display.set_caption("polygon maker")
textures_name = sorted(os.listdir(f"{os.path.dirname(__file__)}/textures"))
font = pygame.font.Font(f"{os.path.dirname(__file__)}/assets/fonts/press_start.ttf")
choosed = None
page = 0

textures = {
    "previous" : pygame.transform.scale_by(pygame.image.load(f"{os.path.dirname(__file__)}\\assets\\buttons\\previous.png").convert_alpha(), 30*default_width/2560),
    "next" : pygame.transform.scale_by(pygame.image.load(f"{os.path.dirname(__file__)}\\assets\\buttons\\next.png").convert_alpha(), 30*default_width/2560)
}

for i in os.listdir(f"{os.path.dirname(__file__)}/assets/icons"):
    textures[str(i[:-4])] = pygame.transform.scale_by(pygame.image.load(f"{os.path.dirname(__file__)}\\assets\\icons\\{i}").convert_alpha(), 9*default_width/2560)

class FunctionalButton:
    functional_buttons = []
    def __init__(self, index, texture_name:str):
        if wide:
            x = 60 * index + 60
            y = height - 35
        else:
            x = 35
            y = 60 * index + 60
        self.location = (x, y)
        self.index = index
        self.texture_name = texture_name
        self.button_rect = pygame.Rect(0,0,50,50)
        self.button_rect.center = self.location
        FunctionalButton.functional_buttons.append(self)
    def draw(self, display):
        pygame.draw.rect(display, (180,180,180), self.button_rect, width = 0, border_radius = 10)
        display.blit(textures[self.texture_name], textures[self.texture_name].get_rect(center = self.location))
    def collide(self, pointlocation):
        if self.button_rect.collidepoint(pointlocation):
            self.action()
    @classmethod
    def draw_all(cls, display):
        for i in cls.functional_buttons:
            i.draw(display)

class Save(FunctionalButton):
    def __init__(self):
        super().__init__(10, "save")
        if wide:
            x = width - 35
            y = height - 35
        else:
            x = 35
            y = height - 35
        self.location = (x, y)
        self.button_rect.center = self.location


class Text:
    texts = []
    def __init__(self, location:tuple, color:tuple, text:str):
        self.location = location
        self.color = color
        self.text = text
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect(center=self.location)
        Text.texts.append(self)
    def draw(self, display):
        display.blit(self.surface, self.rect)
    @classmethod
    def draw_all(cls, display):
        for i in cls.texts:
            i.draw(display)
class Button(Text):
    buttons = []
    
    def __init__(self, location:tuple, color:tuple, text:str):
        super().__init__(location, color, text)
        self.button_rect = pygame.Rect(0,0,300,40)
        self.button_rect.center = location
        Button.buttons.append(self)
    def draw(self, display):
        pygame.draw.rect(display, (200,10,10), self.button_rect, border_radius= 50)
        super().draw(display)
    def collide(self, pointlocation):
        if self.button_rect.collidepoint(pointlocation):
            self.action()
    def action(self):
        pass
    @classmethod
    def all_actions(cls, pointlocation):
        for i in cls.buttons:
            i.collide(pointlocation)
class ChooseTextureButton(Button):
    texture_bottons = []

    def __init__(self, number, texture_name):
        global page
        y = (number % 9) * 50 + 100
        x = (int(number/9)) * 400 + 200
        location = (x, y)
        super().__init__(location, (200,200,200), texture_name)
        ChooseTextureButton.texture_bottons.append(self)
    def action(self):
        global choosed, luncher, editing,window
        choosed = self.text
        luncher = False
        window = pygame.display.set_mode((default_width, default_height), getattr(pygame, "RESIZABLE"))
        editing = True

class NextButton(Button):
    buttons = []
    def __init__(self, next_previous:bool, pages:int):
        self.next_previous = next_previous
        if next_previous:
            location = (default_width//2 + 40, default_height - 40)
        else:
            location = (default_width//2 - 40, default_height - 40)
        super().__init__(location, (200,200,200), str(pages))
        if next_previous:
            self.button_rect = textures["next"].get_rect(center = location)
        else:
            self.button_rect = textures["previous"].get_rect(center = location)
        NextButton.buttons.append(self)
    def draw(self, display):
        global textures, page
        if self.next_previous:
            next_rect = textures["next"].get_rect(center = self.location)
            display.blit(textures["next"], next_rect)
            page_surface = font.render(self.text, True, self.color)
            page_rect = page_surface.get_rect(midright = next_rect.center + pygame.math.Vector2(3,0))
            display.blit(page_surface, page_rect)
        else:
            next_rect = textures["previous"].get_rect(center = self.location)
            display.blit(textures["previous"], next_rect)
            page_surface = font.render(self.text, True, self.color)
            page_rect = page_surface.get_rect(midleft = next_rect.center + pygame.math.Vector2(-3,0))
            display.blit(page_surface, page_rect)
        page_surface =font.render(str(page + 1), True, self.color)
        page_rect = page_surface.get_rect(center = (default_width // 2, self.location[1]))
        display.blit(page_surface, page_rect)
    def action(self):
        global page
        if self.next_previous:
            page += 1
        else:
            page -= 1
        refresh()

def refresh():
    global luncher, editing, textures_name, window, choosed_scaled, textures, one_pixel, default_chess_surface, chess_surface, panel_rect, height, width, wide
    if luncher:
        Text.texts.clear()
        Button.buttons.clear()
        ChooseTextureButton.texture_bottons.clear()
        NextButton.buttons.clear()

        Text((default_width//2,40),(200,200,200),"choose your texture")

        start_id =  page * 18
        end_id = start_id + 18
        actual_textures = textures_name[start_id:end_id]

        for i, texture in enumerate(actual_textures):
            ChooseTextureButton(i,texture)

        if end_id < len(textures_name):
            NextButton(True, page + 2)
        if page > 0:
            NextButton(False, page)
    elif editing:
        Text.texts.clear()
        Button.buttons.clear()
        ChooseTextureButton.texture_bottons.clear()
        NextButton.buttons.clear()
        FunctionalButton.functional_buttons.clear()

        
        window = pygame.display.set_mode((width, height), getattr(pygame, "RESIZABLE"))


        if textures["choosed"].get_width() < textures["choosed"].get_height():
            choosed_scaled = pygame.transform.scale_by(textures["choosed"],height/textures["choosed"].get_height())
            one_pixel = height/textures["choosed"].get_height()
            panel_rect = pygame.Rect(0,0,70,height)
            wide = False          
        else:
            choosed_scaled = pygame.transform.scale_by(textures["choosed"],width/textures["choosed"].get_width())
            one_pixel = width/textures["choosed"].get_width()
            panel_rect = pygame.Rect(0,height-70,width,70)
            wide = True       
        if choosed_scaled.get_width() > width:
            choosed_scaled = pygame.transform.scale_by(textures["choosed"],width/textures["choosed"].get_width())
            one_pixel = width/textures["choosed"].get_width()
            panel_rect = pygame.Rect(0,height-70,width,70)            
            wide = True
        if choosed_scaled.get_height() > height:
            choosed_scaled = pygame.transform.scale_by(textures["choosed"],height/textures["choosed"].get_height())
            one_pixel= height/textures["choosed"].get_height()
            panel_rect = pygame.Rect(0,0,70,height)     
            wide = False          

        chess_surface = pygame.transform.scale_by(default_chess_surface, one_pixel/2)
        Save()

refresh()
while run:
    while luncher and run:

        actual_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Button.all_actions(event.pos)

        window.fill((20,20,20))

        Text.draw_all(window)
        
        pygame.display.flip()
        pygame.time.Clock().tick(50)

    textures["choosed"] = pygame.image.load(f"{os.path.dirname(__file__)}\\textures\\{choosed}")

    color1 = (80,80,80)
    color2 = (60,60,60)

    default_chess_surface = pygame.Surface((textures["choosed"].get_width()*2,textures["choosed"].get_height()*2))

    for x in range(0, textures["choosed"].get_width() * 2):
        for y in range(0, textures["choosed"].get_height() * 2):
            color = color1 if (x + y) % 2 == 0 else color2
            pygame.draw.rect(default_chess_surface, color, (x, y, 1, 1))

    refresh()

    while editing and run:

        actual_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Button.all_actions(event.pos)
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                refresh()                 

        window.fill((40,40,40))
        window.blit(chess_surface, choosed_scaled.get_rect(center = (width//2,height//2)))
        window.blit(choosed_scaled, choosed_scaled.get_rect(center = (width//2,height//2)))
        pygame.draw.rect(window, (20,20,20), panel_rect)
        FunctionalButton.draw_all(window)

        Text.draw_all(window)
        
        pygame.display.flip()
        pygame.time.Clock().tick(50)