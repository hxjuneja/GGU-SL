import sublime, sublime_plugin
import itertools
import os
import re
import random, sys


class GguCommand(sublime_plugin.TextCommand):

    def run(self, edit):


        # Generate file path and position
        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        row = row + 1
        path = os.path.realpath(self.view.file_name()) 
        path = path + "#L" + str(row)

        # Get remotes
        settings = sublime.load_settings("ggu.sublime-settings")
        URL = MakeURL().getremotes(path, settings, remote = False)

        if URL:
            sublime.set_clipboard(URL)
            sublime.status_message('Copied %s to clipboard.' % URL)
            print('Copied %s to clipboard.' % URL)

class GgurCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        self.items = []
        self.fremotes = []

        # Generate file path and position
        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        row = row + 1
        path = os.path.realpath(self.view.file_name()) 
        path = path + "#L" + str(row)

        # Get remotes
        settings = sublime.load_settings("ggu.sublime-settings")
        remotes_stuff = MakeURL().getremotes(path, settings, remote = True)

        if remotes_stuff is None:
            return

        remotes = remotes_stuff[0]
        alises = remotes_stuff[1]
        self.b = remotes_stuff[2]

        for a in alises:
            self.items.append(a)
        for r in remotes:
            self.fremotes.append("https://github.com/"+r[0]+"/"+r[1])

        # show quick panel
        self.view.window().show_quick_panel(self.items, self.on_done)

    def on_done(self, index):
        """
            called when the remote is selected
        """

        URL = self.fremotes[index]
        URL = URL + "/blob/master"
        URL = URL + self.b
        self.paste_url(URL)

    def paste_url(self, URL):
        """
            Paste URL to clipboard
        """

        if URL:
            sublime.set_clipboard(URL)
            sublime.status_message('Copied %s to clipboard.' % URL)
            print('Copied %s to clipboard.' % URL)

class MakeURL(object):

    def find_dir(self, path, folder):
        items = os.listdir(path)
        if folder in items and os.path.isdir(os.path.join(path, folder)):
            return path
        dirname = os.path.dirname(path)
        if dirname == path:
            return None
        return self.find_dir(dirname, folder)

    def getremotes (self, path, settings, remote = None):
        """
            Generate the url
        """

        folder_name, file_name = os.path.split(path)
        git_path = self.find_dir(folder_name, '.git')

        if not git_path:
            sublime.error_message('Could not find .git directory.')
            print('Could not find .git directory.')
            return

        new_path = folder_name[len(git_path):]

        username = ""
        username = settings.get("username")
        if username == "":
            sublime.error_message("Pleaes edit your ggu.sublime-settings file")

        URL_path = new_path+"/"+file_name
        branch = self.get_branch( git_path)
        
        if remote is True:
            remote_alias, remotes = self.get_remote_branch(git_path, folder_name)
            return (remotes, remote_alias, URL_path)

        repo = path[:len(path)-len(URL_path)].split("/")
        repo = repo[len(repo)-1:][0]

        URL = "https://github.com/%s/%s/blob/%s%s"%(username, repo,branch,URL_path)
        return URL

    def get_remote_branch(self, git_path, folder_name):
        """
            Get remote branches
        """

        gitc_path = os.path.join(git_path, '.git', 'config')

        with open(gitc_path, "r") as git_config_file:
            config = git_config_file.read()

        r1 = r'(?:remote\s\")(.*?)\"\]'
        raliases = re.findall(r1,config)

        r2 = r'url\s=\s(?:https://%s/|%s:|git://%s)(.*)/(.*?)(?:\.git)'%('github.com', 'github.com', 'github.com')
        remotes = re.findall(r2,config)

        return  raliases, remotes
        
    def get_branch(self, git_path):
        """
            get current branch of the required repo
        """

        ref = open(os.path.join(git_path, '.git', 'HEAD'), "r").read().replace('ref: ', '')[:-1]
        branch = ref.replace('refs/heads/','')

        return branch
 
 