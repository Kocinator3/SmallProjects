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
choosed_point = None
one_pixel = 1
lock_lower_grid = False
x, y = 100, 0

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
    if str(i[:-4]) == "save":
        textures[str(i[:-4])] = pygame.transform.scale_by(pygame.image.load(f"{os.path.dirname(__file__)}\\assets\\icons\\{i}").convert_alpha(), 7*default_width/2560)

class Point:
    exportable = []
    points = []
    points_to_remove = []
    def __init__(self, location, lock_lower_grid = False, insert = False):
        global choosed_point
        self.location = pygame.Vector2(location) - shift
        if lock_lower_grid:
            rel_x = round((self.location.x / one_pixel)*2)/2
            rel_y = round((self.location.y / one_pixel)*2)/2
        else:
            rel_x = round(self.location.x / one_pixel)
            rel_y = round(self.location.y / one_pixel)            
        self.relative_location = pygame.Vector2(rel_x, rel_y)
        self.location = self.relative_location * one_pixel + shift
        self.relative_location = self.relative_location - Core.relative_location
        if self.relative_location in Point.exportable:
            Point.points[Point.exportable.index(self.relative_location)].choosed()
        elif choosed_point != None:
            if insert == True:
                Point.points.insert(choosed_point.index + 1, self)
                Point.exportable.insert(choosed_point.index + 1, self.relative_location)
                self.index = Point.points.index(self)
                choosed_point = self
                Point.refresh_all()
            else:
                choosed_point.relative_location = self.relative_location
                Point.exportable[choosed_point.index] = self.relative_location
                Point.refresh_all()
        else:
            Point.points.append(self)
            Point.exportable.append(self.relative_location)
            self.index = Point.points.index(self)
            if self.index == 0:
                choosed_point = self
    def draw(self, display):
        index = Point.points.index(self)
        pygame.draw.line(display, (0,0,255), self.location, Point.points[index - 1].location, width = 5)
        if choosed_point != None:
            if choosed_point.index + 1 == self.index:
                pygame.draw.line(display, (60, 60,255), self.location, Point.points[index - 1].location, width = 5)
        if choosed_point == self:
            pygame.draw.circle(display, (70, 70, 255), self.location, one_pixel/3)
        else:
            if index == 0:
                if Point.points[-1] == choosed_point:
                    pygame.draw.line(display, (60, 60,255), self.location, Point.points[index - 1].location, width = 5) 
                pygame.draw.circle(display, (0,0,200), self.location, one_pixel/4)
            else:
                pygame.draw.circle(display, (0,0,200), self.location, one_pixel/4)
    def refresh(self):
        self.location = (self.relative_location + Core.relative_location) * one_pixel + shift
        self.index = Point.points.index(self)
    def choosed(self):
        global choosed_point
        choosed_point = self
    def remove(self):
        global choosed_point
        Point.exportable.remove(self.relative_location)
        Point.points_to_remove.append(self)
        if len(Point.points) > 1:
            choosed_point = Point.points[self.index - 1]
        else:
            choosed_point = None
        Point.refresh_all()
    @classmethod
    def draw_all(cls, display):
        for i in cls.points:
            i.draw(display)
    @classmethod
    def refresh_all(cls,):
        for i in Point.points_to_remove:
            Point.points.remove(i)
        Point.points_to_remove.clear()
        for i in cls.points:
            i.refresh()

class Core:
    relative_location = None
    core = None
    def __init__(self, location = None, lock_lower_grid = True):
        if location == None:
            location = (width/2, height/2)
        Core.core = self
        self.location = pygame.Vector2(location) - shift
        if lock_lower_grid:
            rel_x = round((self.location.x / one_pixel)*2)/2
            rel_y = round((self.location.y / one_pixel)*2)/2            
        else:
            rel_x = round(self.location.x / one_pixel)
            rel_y = round(self.location.y / one_pixel)
        Core.relative_location = pygame.Vector2(rel_x, rel_y)
        self.location = self.relative_location * one_pixel + shift
    @classmethod
    def draw(cls, display):
        pygame.draw.circle(display, (0,200,0), cls.core.location, one_pixel/4)
    def refresh(self):
        self.location = self.relative_location * one_pixel + shift


class FunctionalButton:
    functional_buttons = []
    def __init__(self, index, texture_name:str, key):
        if wide:
            x = 60 * index + 60
            y = height - 35
        else:
            x = 35
            y = 60 * index + 60
        self.location = (x, y)
        self.key = key
        self.index = index
        self.texture_name = texture_name
        self.button_rect = pygame.Rect(0,0,50,50)
        self.button_rect.center = self.location
        FunctionalButton.functional_buttons.append(self)
    def draw(self, display):
        pygame.draw.rect(display, (180,180,180), self.button_rect, width = 0, border_radius = 10)
        display.blit(textures[self.texture_name], textures[self.texture_name].get_rect(center = self.location))
        if pygame.key.get_pressed()[pygame.K_LALT]:
            key = font.render(str(self.key).upper(), True, (0,0,0))
            display.blit(key, key.get_rect(center = (self.location[0] - 15, self.location[1] + 15)))

    def collide(self, pointlocation):
        if self.button_rect.collidepoint(pointlocation):
            self.action()
    @classmethod
    def draw_all(cls, display):
        for i in cls.functional_buttons:
            i.draw(display)
    @classmethod
    def alt_all(cls, key):
        for i in cls.functional_buttons:
            if key == i.key:
                i.action()
    @classmethod
    def collide_all(cls, pointlocation):
        for i in cls.functional_buttons:
            i.collide(pointlocation)

class SaveBtn(FunctionalButton):
    def __init__(self):
        super().__init__(10, "save", "s")
        if wide:
            x = width - 35
            y = height - 35
        else:
            x = 35
            y = height - 35
        self.location = (x, y)
        self.button_rect.center = self.location
    def action(self):
        global choosed

        refresh()

        raw_data = []
        for i in Point.exportable:
            raw_data.append([i.x, i.y])

        path_to_the_file = f"{os.path.dirname(__file__)}\\polygons.json"

        try:
            with open(path_to_the_file, "r", encoding="utf-8") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = {}

        all_data[choosed.split('.')[0]] = raw_data

        with open(path_to_the_file, "w", encoding="utf-8") as file:
            json.dump(all_data, file, indent=4)
class RemoveBtn(FunctionalButton):
    def __init__(self):
        super().__init__(2, "remove", "t")
    def action(self):
        if choosed_point != None:
            choosed_point.remove()
class CoreBtn(FunctionalButton):
    def __init__(self):
        super().__init__(0, "core_off", "c")
    def action(self):
        if "on" in self.texture_name:
            self.texture_name = "core_off"
            self.button_rect = pygame.Rect(0,0,50,50)
            self.button_rect.center = self.location
        else:
            self.texture_name = "core_on"
            self.button_rect = pygame.Rect(0,0,55,55)
            self.button_rect.center = self.location
class LockBtn(FunctionalButton):
    def __init__(self):
        super().__init__(1, "lock(1x1)", "l")
    def action(self):
        global lock_lower_grid
        if "1" in self.texture_name:
            self.texture_name = "lock(2x2)"
            lock_lower_grid = True
        else:
            self.texture_name = "lock(1x1)"
            lock_lower_grid = False


def load(path_to_the_file, choosed_texture):
    try:
        with open(path_to_the_file, "r", encoding="utf-8") as file:
            all_data = json.load(file)
            if choosed_texture.split(".")[0] in all_data:
                raw_data = all_data[choosed_texture.split(".")[0]]

                for i in raw_data:
                    Point((pygame.math.Vector2(i) * one_pixel) + Core.core.location, lock_lower_grid=True, insert=True)
            else:
                raw_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        print(FileNotFoundError)


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
        self.color = (200,10,10)
    def draw(self, display):
        pygame.draw.rect(display, self.color, self.button_rect, border_radius= 50)
        super().draw(display)
    def collide(self, pointlocation):
        if self.button_rect.collidepoint(pointlocation):
            self.action()
    def action(self):
        pass
    @classmethod
    def collide_all(cls, pointlocation):
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
        if texture_name[:-4] in all_data:
            self.color = (10,10,200)
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

json_file = f"{os.path.dirname(__file__)}\\polygons.json"

try:
    with open(json_file, "r", encoding="utf-8") as file:
        all_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print(FileNotFoundError) 

def refresh():
    global luncher, editing, textures_name, window, choosed_scaled, textures, one_pixel, default_chess_surface, chess_surface, panel_rect, height, width, wide, shift
    if luncher:
        pygame.display.set_caption("polygon maker")
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
        pygame.display.set_caption(choosed)
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
            one_pixel = height/textures["choosed"].get_height()
            panel_rect = pygame.Rect(0,0,70,height)     
            wide = False          

        chess_surface = pygame.transform.scale_by(default_chess_surface, one_pixel/2)
        SaveBtn()
        RemoveBtn()
        CoreBtn()
        LockBtn()

        shift = pygame.math.Vector2((width - choosed_scaled.get_width()) / 2, (height - choosed_scaled.get_height()) / 2)

        Core.core.refresh()
        Point.refresh_all()
refresh()
while run:
    window = pygame.display.set_mode((default_width, default_height))
    refresh()
    
    if choosed != None:
        editing = True
        luncher = False

    json_file = f"{os.path.dirname(__file__)}\\polygons.json"

    while luncher and run:

        txts = sorted(os.listdir(f"{os.path.dirname(__file__)}/textures"))
        if txts != textures_name:
            textures_name = txts
            refresh()

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(FileNotFoundError)        

        actual_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Button.collide_all(event.pos)

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
            one_pixel = height/textures["choosed"].get_height()
            panel_rect = pygame.Rect(0,0,70,height)     
            wide = False 
            
    shift = pygame.math.Vector2((width - choosed_scaled.get_width()) / 2, (height - choosed_scaled.get_height()) / 2)

    Core()

    load(f"{os.path.dirname(__file__)}\\polygons.json", choosed)

    refresh()

    while editing and run:

        actual_time = pygame.time.get_ticks()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    FunctionalButton.collide_all(event.pos)
                    if choosed_scaled.get_rect(center = (width//2,height//2)).collidepoint(event.pos) and not panel_rect.collidepoint(event.pos):
                        Point(event.pos, lock_lower_grid=lock_lower_grid)
                if event.button == 1:
                    FunctionalButton.collide_all(event.pos)
                    if choosed_scaled.get_rect(center = (width//2,height//2)).collidepoint(event.pos) and not panel_rect.collidepoint(event.pos):
                        Point(event.pos, insert=True, lock_lower_grid=lock_lower_grid)
                index = textures_name.index(choosed)
                txts = sorted(os.listdir(f"{os.path.dirname(__file__)}/textures"))
                if txts != textures_name:
                    textures_name = txts
                    refresh()                
                if event.button == 4 and index != 0:
                    choosed = textures_name[index - 1]
                    raw_data = []
                    Point.points.clear()
                    Point.exportable.clear()
                    choosed_point = None
                    editing = False
                if event.button == 5 and index != len(textures_name) - 1:
                    choosed = textures_name[index + 1]
                    raw_data = []
                    Point.points.clear()
                    Point.exportable.clear()
                    choosed_point = None
                    editing = False

            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                refresh()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LALT] and event.key != pygame.K_LALT:
                    FunctionalButton.alt_all(pygame.key.name(event.key))
                if event.key == pygame.K_ESCAPE:
                    luncher = True
                    choosed = None
                    editing = False
                if event.key == pygame.K_DELETE:
                    choosed_point.remove()


        window.fill((40,40,40))
        window.blit(chess_surface, choosed_scaled.get_rect(center = (width//2,height//2)))
        window.blit(choosed_scaled, choosed_scaled.get_rect(center = (width//2,height//2)))

        #Points and lines
        Core.draw(window)
        Point.draw_all(window)
        if choosed_point != None:
            choosed_point.draw(window)
        if Point.points.__len__() > 0:
            Point.points[0].draw(window)
            if Point.points.__len__() > 2:
                Point.points[-1].draw(window)
                        

        #GUI
        pygame.draw.rect(window, (20,20,20), panel_rect)
        FunctionalButton.draw_all(window)

        Text.draw_all(window)
        
        pygame.display.flip()
        pygame.time.Clock().tick(50)

    raw_data = []
    Point.points.clear()
    Point.exportable.clear()
    Core.core = None
    Core.relative_location = None
    choosed_point = None