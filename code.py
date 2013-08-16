import sys, pygame
import commands
import re

re_startsection = re.compile(r"\[(.*)\]")
re_data = re.compile(r"\_(.*)=(.*)")
re_generickeyvalue = re.compile(r"(.*)=(.*)")
re_command = re.compile(r"\^(.*)=(.*)")
re_comment = re.compile(r"#.*$")

pygame.init()
settings = {};

#READ GENERIC CONFIGURATION FILE settings.txt
f = open('./Settings/settings.txt', 'r').read()
for line in f.splitlines():
  key = re_generickeyvalue.match(line).group(1).strip()
  value = re_generickeyvalue.match(line).group(2).strip()
  settings[key] = value;


#PREPARE the mixer so we can create sound objects
pygame.mixer.init()
pygame.mixer.set_num_channels(int(settings["num_channels"]))

class SoundDataObject:
  soundobj = "";
  data = {};
  def __init__(self, soundobj, data):
    self.soundobj = soundobj;
    self.data = data;

#READ CONFIGURATION FILE FOR SOUNDS
sounds = [];

f = open("./Settings/" + settings["soundfile"], 'r').read()

sectionsanddata = re_startsection.split(f)[1:]

while sectionsanddata:
  data = {}
  section = sectionsanddata[0].strip()
  soundobj = pygame.mixer.Sound("./Sounds/" + section)
  data_raw = sectionsanddata[1].strip()
  for line in data_raw.splitlines():
    print line;
    key = re_generickeyvalue.match(line).group(1).strip()
    value = re_generickeyvalue.match(line).group(2).strip()
    data[key] = value;
  sectionsanddata = sectionsanddata[2:]

  
  a = SoundDataObject(soundobj, data);
  sounds.append(a);


#READ CONFIGURATION FILE FOR LAYOUT
layout = {};
f = open("./Settings/" + settings["layoutfile"], 'r').read()

sectionsanddata = re_startsection.split(f)[1:]

while sectionsanddata:
  title = sectionsanddata[0].strip()
  sectiondata = {}
  data_raw = sectionsanddata[1].strip()
  for line in data_raw.splitlines():
    key = re_generickeyvalue.match(line).group(1).strip()
    value = re_generickeyvalue.match(line).group(2).strip()
    sectiondata[key] = value;
  sectionsanddata = sectionsanddata[2:]

  layout[title] = sectiondata
  
#END CONFIGURATION FILE FOR LAYOUT



class CueObject:
  comment = ""
  commands = []
  def __init__(self, comment, commands):
    self.comment = comment
    self.commands = commands

#READ CONFIGURATION FILE FOR CUES

cues = [];

f = open("./Settings/" + settings["cuesfile"], 'r').read()

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
  buffer = buffer.strip().lower()
  if buffer:
    buffer = buffer.split(" ")
    if buffer[0] == "close" or buffer[0] == "exit":
      sys.exit();
    if buffer[0] == "goto":
      global curcue
      curcue = int(buffer[1])
      return "Next cue is now cue "+ str(curcue);
    if buffer[0] == "fade":
      if buffer[2] == "all":
        for asound in sounds:
          asound.soundobj.fadeout(int(buffer[1])*1000);
        return "Faded all sounds"
      else:
        for asound in sounds:
          if asound.data["keyword"] == buffer[2]:
            asound.soundobj.fadeout(int(buffer[1])*1000);
        return "Faded requested sound"
    if buffer[0] == "silence":
      if buffer[1] == "all":
        for asound in sounds:
          asound.soundobj.stop();
        return "Silenced all sounds"
      else:
        for asound in sounds:
          if asound.data["keyword"] == buffer[1]:
            asound.soundobj.stop();
        return "Silenced requested sound"
    if buffer[0] == "play":
      for asound in sounds:
        if asound.data["keyword"] == buffer[1]:
          asound.soundobj.play();
      return "Playing requested sound"
    if buffer[0] == "loop":
      for asound in sounds:
        if asound.data["keyword"] == buffer[1]:
          asound.soundobj.play(loops = -1);
      return "Playing requested sound"
    return "That command was not found"
  else:
    return "You did not enter a command"
    
def runCue(cue):
  for command in cues[cue].commands:
    runCommand(command);

curcue = 0;
buffer = "";
lastcommand = "";
lastresponse = "";

def keyeventhandle(event):
  global curcue;
  global buffer;
  global lastcommand;
  global lastresponse;
  if event.unicode == '\r':
    lastcommand = (buffer);
    lastresponse = runCommand(buffer);
    buffer = "";
  elif event.unicode == '\t':
    if curcue >= len(cues):
      curcue = -1;
    runCue(curcue)
    curcue = curcue + 1
  elif event.unicode == '\b':
    buffer = buffer[:-1]
  else:
    buffer = buffer + event.unicode;
    
def tocolortuple(hexstring):
  r = int(hexstring[0:2], 16)
  g = int(hexstring[2:4], 16)
  b = int(hexstring[4:6], 16)
  return r,g,b
  
  
def run():
  size = width, height = int(settings["windowwidth"]),int(settings["windowheight"])
  background = tocolortuple(settings["undefinedcolor"])
  if settings["fullscreen"] == "True":
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
  else:
    screen = pygame.display.set_mode(size)

  size = width, height = screen.get_size()
  settings["screenwidth"] = width;
  settings["screenheight"] = height;

  myfont = pygame.font.SysFont(settings["font"], int(settings["fontsize"]))
  while 1:
      #EventHandle
      for event in pygame.event.get():
          if event.type == pygame.QUIT: sys.exit();
          if event.type == pygame.KEYDOWN: keyeventhandle(event);
      
      #--Draw--
      #Clear The Screen
      screen.fill(background)
      
      for section in layout:
        actual_width = (int(layout[section]["width"]) * settings["screenwidth"]) / 100
        actual_height = (int(layout[section]["height"]) * settings["screenheight"]) / 100
        surf = pygame.Surface((actual_width,actual_height))
        pygame.draw.rect(surf, tocolortuple(layout[section]["bordercolor"]), pygame.Rect(0, 0, actual_width, actual_height), 0)
        bordersize = int(layout[section]["bordersize"])
        pygame.draw.rect(surf, tocolortuple(layout[section]["backgroundcolor"]), pygame.Rect(0+bordersize, 0+bordersize, actual_width-(bordersize*2), actual_height-(bordersize*2)), 0)
        if section == "Response":
          #Draw the response of the last command
          label = myfont.render("Ran: "+lastcommand, 1, tocolortuple(layout[section]["commandcolor"]))
          surf.blit(label, (int(layout[section]["padding"]) + bordersize, int(layout[section]["padding"]) + bordersize))
          t = 1
          for line in lastresponse.splitlines():
            label = myfont.render(line, 1, tocolortuple(layout[section]["responsecolor"]))
            surf.blit(label, 
                             (
                               int(layout[section]["padding"]) + bordersize,
                               int(layout[section]["padding"]) + bordersize + (int(settings["fontsize"])*t)
                             )
                      )
            t += 1
        if section == "Prompt":
          #Draw The Contents of the Text Buffer
          label = myfont.render(buffer, 1, tocolortuple(layout[section]["color"]))
          surf.blit(label, (int(layout[section]["padding"]) + bordersize, int(layout[section]["padding"]) + bordersize))
        if section == "Cues":
          #figure out how many cues can fit in the window
          numcues = (actual_height-(int(layout[section]["padding"]) + bordersize)) / (int(settings["fontsize"]) + int(layout[section]["linespacing"])); 
          for i in range(0, numcues):
            io = curcue + (i - numcues/2)
            if io < 0 or io >= len(cues):
              curcueobj = CueObject("","");
            else:
              curcueobj = cues[io]
            if i == numcues/2:
              label = myfont.render(str(io).rjust(3) + " Next: " + curcueobj.comment, 1, tocolortuple(layout[section]["color"]))
            else:
              label = myfont.render(str(io).rjust(3) + "       " + curcueobj.comment, 1, tocolortuple(layout[section]["color"]))
            labelloc = (
                          int(layout[section]["padding"]) + bordersize,
                          int(layout[section]["padding"]) + bordersize + ((int(layout[section]["linespacing"]) + int(settings["fontsize"])  )*i)
                       )
            surf.blit(label, labelloc)        
        screen.blit(surf, ((int(layout[section]["x"]) * settings["screenwidth"]) / 100, (int(layout[section]["y"]) * settings["screenheight"]) / 100))          

#          surf = pygame.Surface((200,50))
#          pygame.draw.rect(surf, (100,100,100), pygame.Rect(3, 3, 194, 44), 0)
#          label = myfont.render("Cue up next:", 1, (0,0,0))
#          surf.blit(label, (3, 3))
#          screen.blit(surf, (0, 150))
      
    #  cuesurf = pygame.Surface((50,50))
    #  pygame.draw.rect(cuesurf, (200,200,200), pygame.Rect(3, 3, 74, 44), 0)
    #  label = myfont.render(str(curcue), 1, (0,0,0))
    #  cuesurf.blit(label, (3, 3))
    #  screen.blit(cuesurf, (0,55))

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
      
run()
