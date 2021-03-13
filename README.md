# Minimal DUCO Miner for Android

This miner is built with Kivy and Buildozer to produce an easy to use android app.
It's very minimal, the user gets no feed back at the moment but it works. 

The miner class is based on revox's minimal pc miner.

I could not for the life of me figure out checkbuttons, so you will have to write yes or no in the
application interface. I know typing is cringe for mobile UX.



## Usage:

-  Allow unknown sources in settings. 
-  Install the apk as usual, and run it.
-  Type in your DUCO Username.
-  Type in yes or no for the difficulty setting.
-  Press the big button.

## For Developers:

The code is kind of a mess, I normally dont work with Kivy, I mostly use Tkinter and or its derivatives.
This means this app has no style, no good design and it's just a proof of concept that can mine. 

When I get good enough, I will port the algorithm to Dart and use Flutter to make a proper mobile Miner, and maybe even a wallet.

Install `libffi-dev` if you encounter a buildozer error about `_ctypes`, you may need to delete your `.buildozer` folder.


- Set up Kivy and Buildozer. (The setup is kinda complex, there are better guides online, sorry)
- To build the apk, run `buildozer android release`

## Upcoming features:

- Some sort of user feedback, like a scrolling text of transactions or just a color change in the app.

### License:

MIT License, like most of the Duino-Coin project.

