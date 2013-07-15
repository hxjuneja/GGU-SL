## About

Get Git Url (GGU) is a [Sublime-Text 2] plugin that generate a GitHub repo URL for you from your editor itself.

## Usage


GGU helps you share the code in your remote repo (GitHub) from your local repo,
So there's no need to search for your code and the line no in GitHub and then paste the URL to share it
You can do all this very easily from your editor.

Here's how

1. Go to the file and line no using Vim.

2. press `ctrl + alt + g`

3. Boom! you are free to paste the URL.


##  Quick Start

1. Setup GGU:

  dowload the source code from [[here]]

  ```
  cd ~/.config/sublime-text 2/Installed Packages
  ```

2. Configure GGU:

  Before you can start you need to edit config.py.

  ```
  cd ~/.config/sublime-text 2/Installed Packages/

  ```
  Open the GGU-SL.sublime.package and open a file config.py

  In this file add the following
  
  ```
   def __init__(self):
   
        " Your Github Username
        self.username = "hardikj"
        
        " Your Shell(sudo) Password
        self.pw = ""  
        
  ```

Thats It!! Enjoy.



