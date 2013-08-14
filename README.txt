SyncedPlay
==

This program was developed for people who need to play back certain sound files at certain times, with no delay.
My particular use-case was during drama preformances, when sound effects had to be played, and other solutions had too long of a loading period.

Run
==

1) Convert audio files to "OGG" and place them in the sounds directory.
2) Create a Sounds.txt file, linking sounds to keyboard commands.
3) Optionally, create a cues.txt file, creating a list of cues, so you can step through them with the space bar.

In both sounds.txt and cues.txt, blank lines and lines starting with # are ignored

sounds.txt format:
  [Path To Sound File relative to the sounds directory]
  _attribute = value
  ^commandtoregister = effect

example sounds.txt:
  [Phone-Ring.ogg]
  _name = Intercom-Buzz
  ^playbuzz = play
  ^cancelbuzz = fade 1

NOTE: name is the only required attribute

possible effects are:
  play = begin playback
  fade value = fade to silence in "value" seconds

cues.txt format:
  #Comment
  [Cue Title]
  Command to run
  Command to run 

example cues.txt:
  #This is the beginning of the preformance
  [Opening Sounds]
  Trumpets
  Flutes
  Curtain_Opening_Sound
  [First Act]
  Forest_Ambiance
  [End]
  Ending_Music
