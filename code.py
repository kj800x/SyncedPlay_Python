import sys, pygame
import commands
import re

re_startsection = re.compile(r"\[(.*)\]")
re_data = re.compile(r"\_(.*)=(.*)")
re_command = re.compile(r"\^(.*)=(.*)")
re_comment = re.compile(r"#.*$")

pygame.init()

SONG_END = pygame.USEREVENT + 10

pygame.mixer.init()
pygame.mixer.set_num_channels(30)

class CueObject:
  comment = ""
  commands = []
  def __init__(self, comment, commands):
    self.comment = comment
    self.commands = commands

class SoundDataObject:
  soundobj = "";
  data = {};
  commands = {};
  def __init__(self, soundobj, data, commands):
    self.soundobj = soundobj;
    self.data = data;
    self.commands = commands;





sounds = [];

f = open('./sounds.txt', 'r').read()

sectionsanddata = re_startsection.split(f)[1:]

while sectionsanddata:
  data = {}
  commands = {}
  section = sectionsanddata[0].strip()
  soundobj = pygame.mixer.Sound("./Sounds/" + section)
  data_raw = sectionsanddata[1].strip()
  for line in data_raw.splitlines():
    print line;
    if re_command.match(line):
      key = re_command.match(line).group(1).strip()
      value = re_command.match(line).group(2).strip()
      commands[key] = value;
      
    if re_data.match(line):
      key = re_data.match(line).group(1).strip()
      value = re_data.match(line).group(2).strip()
      data[key] = value;
  sectionsanddata = sectionsanddata[2:]

  
  a = SoundDataObject(soundobj, data, commands);
  sounds.append(a);



#BEGIN CUE

cues = [];

f = open('./cues.txt', 'r').read()

sectionsanddata = re_startsection.split(f)[1:]

while sectionsanddata:
  commands = []
  comment = sectionsanddata[0].strip()
  
  data_raw = sectionsanddata[1].strip()
  for line in data_raw.splitlines():
    commands.append(line.strip())

  a = CueObject(comment, commands);
  cues.append(a);
  
  sectionsanddata = sectionsanddata[2:]

#END CUE





  

def runCommand(buffer):
  if buffer:
    global curcue;
    if buffer[0] == "^":
      if buffer[1] == "k":
        for asound in sounds:
          asound.soundobj.fadeout(500);
      if buffer[1] == "g":
        curcue = int(buffer[2:])
    else:
      for asound in sounds:
        if buffer in asound.commands:
          if asound.commands[buffer] == "play":
            asound.soundobj.play();
          if asound.commands[buffer][0:4] == "fade":
            asound.soundobj.fadeout(int(asound.commands[buffer][5:]) * 1000)

def runCue(cue):
  for command in cues[cue].commands:
    runCommand(command);

curcue = 0;
buffer = "";

def keyeventhandle(event):
  global curcue;
  global buffer;
  if event.unicode == '\r':
    runCommand(buffer);
    buffer = "";
  elif event.unicode == ' ':
    if curcue >= len(cues):
      curcue = -1;
    runCue(curcue)
    curcue = curcue + 1
  elif event.unicode == '\b':
    buffer = buffer[:-1]
  else:
    buffer = buffer + event.unicode;
    
    
    ###NOT YET CLEANED UP###
  
size = width, height = 500,500
speed = [2, 2]
background = 150, 196, 242

screen = pygame.display.set_mode(size)

size = width, height = screen.get_size() 

myfont = pygame.font.SysFont("Courier New", 15)

while 1:
    #EventHandle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit();
        if event.type == pygame.KEYDOWN: keyeventhandle(event);
        if event.type >= SONG_END: sm.handleSignal(event);
    
    #Process

    #--Draw--
    #Clear The Screen
    screen.fill(background)
    
    
    #Draw The Contents of the Text Buffer
    
    surf = pygame.Surface((400,50))
    pygame.draw.rect(surf, (200,200,200), pygame.Rect(3, 3, 394, 44), 0)
    label = myfont.render(buffer, 1, (0,0,0))
    surf.blit(label, (3, 3))
    screen.blit(surf, (0, 0))

    surf = pygame.Surface((200,50))
    pygame.draw.rect(surf, (100,100,100), pygame.Rect(3, 3, 194, 44), 0)
    label = myfont.render("Cue up next:", 1, (0,0,0))
    surf.blit(label, (3, 3))
    screen.blit(surf, (0, 150))
    
  #  cuesurf = pygame.Surface((50,50))
  #  pygame.draw.rect(cuesurf, (200,200,200), pygame.Rect(3, 3, 74, 44), 0)
  #  label = myfont.render(str(curcue), 1, (0,0,0))
  #  cuesurf.blit(label, (3, 3))
  #  screen.blit(cuesurf, (0,55))

    cuelogssurf = pygame.Surface((500,100))
    for i in range(0, 5):
      io = curcue + (i - 2)
      if io < 0 or io >= len(cues):
        curcueobj = CueObject("","");
      else:
        curcueobj = cues[io]
      if i == 2:
        label = myfont.render(str(io) + "> " + curcueobj.comment, 1, (255,255,255))
      else:
        label = myfont.render(str(io) + "  " + curcueobj.comment, 1, (255,255,255))
      cuelogssurf.blit(label, (3, 3+(20*i)))
    screen.blit(cuelogssurf, (0,200))
    
    #i = 0;
    #for sound in sounds:
      #surf = pygame.Surface((100,100))
      #pygame.draw.rect(surf, (200,200,200), pygame.Rect(3, 3, 96, 96), 0)
      
      # pick a font you have and set its size
      
      #textcolor = (255,255,0)
      #if sound.isplaying:
      #  textcolor = (255,0,255)
      
      # apply it to text on a label
      #label = myfont.render(sound.name, 1, textcolor)
      #surf.blit(label, (10, 10))
        
      #screen.blit(surf, (2 + (102*i), 52))
      #i=i+1
      
    pygame.display.flip()
