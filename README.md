## About

[Get Git Url](https://sublime.wbond.net/packages/Ggu) (GGU) is a Sublime-Text plugin that generate Github URL of the file you are on, from your editor and paste it to clipboard.

## Usage

I want my editor to quickly generate the Github URL for me without jumping to the browser to yank the URL of file.

So I made this.

## Install

### Package Control

The easiest way to install this is with [Package Control](https://sublime.wbond.net/packages/Ggu).

 * If you just went and installed [Package Control](http://wbond.net/sublime\_packages/package\_control), you probably need to restart Sublime Text 2 before doing this next bit.
 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Select GGU when the list appears.

### Other Methods

#### OSX

```
$ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
$ git clone git://github.com/kemayo/GGU-SL.git 
```

#### Linux

```
$ cd ~/.config/sublime-text-2/Packages/
$ git clone git://github.com/kemayo/sublime-text-2-git.git Git
```

## Get Started

1. Configure GGU:

  Before you can start you need to edit ggu.sublime-setting.py.


2.  Generate remote repo URL

  1. Go to the file in a git repo.

  2. press `ctrl + alt + r`

  3. Choose your remote repo.

  4. Boom! you are free to paste the URL.
  
  ![remote](http://s13.postimg.org/oudt9sk07/choose_remote.png)


3.  Quickly Generate URL  -  

  1. Go to the file in a git repo.

  2. press `ctrl + alt + g`

  3. Boom! you are free to paste the URL.
  
  Note - This automatically detect your current branch you are working on


4.  You are free to change the key bindings.


Thats It!! Enjoy.



