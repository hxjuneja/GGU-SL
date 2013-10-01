import sublime, sublime_plugin
import itertools
import os
import subprocess
import random, sys
import shelve

class GguCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Generate file path and position
        path, row = self.get_path(edit)
        if path:
            slpath = path+"#L"+str(row)

        # Generate URL
        self.d = sublime.load_settings("ggu.sublime-settings")
        URL = MakeURL().geturl(slpath, self.d)

        # Paste URL
        if URL:
            sublime.set_clipboard(URL)

    def get_path(self,edit):
        """
            Get current filename and position
        """
	    (row,col) = self.view.rowcol(self.view.sel()[0].begin())
	    return (self.view.file_name(),row + 1 )

class GgurCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        self.items = []
        self.fremotes = []

        # Generate file path and position
        path, row = self.get_path(edit)
        if path:
            slpath = path + "#L" + str(row)

        # Get remotes
        self.d = sublime.load_settings("ggu.sublime-settings")
        (remotes,b) = MakeURL().geturl(slpath,self.d, remote = True)
        self.b = b

        for r in remotes:
            self.items.append(r[0])
            self.fremotes.append(r[1])

        # show quick panel
        self.view.window().show_quick_panel(self.items, self.on_done)

    def on_done(self, index):
        """
            called when the remote is selected
        """

        URL = self.fremotes[index]
        URL = URL + "/blob/master"
        for bb in self.b:
            URL = URL + "/" + bb
        self.paste_url(URL)

    def paste_url(self, URL):
        """
            Paste URL to clipboard
        """

        if URL:
            sublime.set_clipboard(URL)

    def get_path(self, edit):
        """
            Generate current file path and position
        """

        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        return (self.view.file_name(),row + 1 )              

class MakeURL(object):

    def __init__(self):
        
        self.dicpath = None
        self.path =  None

    def getrepo(self, path, d):
        """
            Get all git repositories
        """

        self.path = path.strip('') 
        self.dicpath = path.split('/')[1:]

        repoin = self.dicpath[0]
        pw = d.get("pw")

        if pw == "":
            sublime.error_message("Pleaes edit your ggu.sublime-settings file")

        p2 = subprocess.Popen('echo ' + pw +' |sudo -S locate -r \'\.git$\'| xargs -n 1 dirname ',shell=True, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = p2.communicate()
        output = output[0].strip()
        dirs = output.split("\n")
        sorted_dict = []
        for i in dirs:
            for m,n in zip(i.split("/")[1:],self.dicpath):
                if m != n:
                    i = []
            if type(i) is not list:
                sorted_dict.append(i)


        def IsEmpty(inList):
            if isinstance(inList, list):
                return all( map(IsEmpty, inList) )
            return False 

        if IsEmpty(sorted_dict):
            sublime.error_message("This file is not in a git repo")  
            return None

        else:
            return sorted_dict

    def geturl (self, path, d, remote = None):
        """
            Generate the url
        """
        dirs = self.getrepo(path, d)
        if dirs is None:
            return None

        maxlength = max(s for s in dirs)

        b = []

        lleng = maxlength.split('/')[1:]

        self.pstatus()

        for i,j in itertools.izip_longest(self.dicpath,lleng):
            if j is not None:
                continue
            else:
                b.append(i)

        username = ""
        if remote is True:
            r = self.get_remote_branch(maxlength)
            return (r,b)

        else:    
            username = d.get("username")
            if username == "":
                sublime.error_message("Pleaes edit your ggu.sublime-settings file")

        branch = self.get_branch(maxlength)
        URL = ["https:/", "github.com", username, lleng[len(lleng)-1], "blob",branch]  
        for i in b:
             URL.append(i)

        URL = "/".join(URL)
        
        return URL

    def get_remote_branch(self, ml):
        """
            Get remote branches
        """

        remotes = []   
        os.chdir(ml)
        p1 = subprocess.Popen(["git", "remote", "-v"], stdout = subprocess.PIPE)
        output = p1.communicate()
        for o in output[0].split("\n")[::2]:
            if o != "":
                o = o.split(" ")[0].split("\t")
                o[1] = o[1].split(".git")[0]
                remotes.append(o)
        return remotes 

    def get_branch(self, ml):
        """
            get current branch of the required repo
        """
        os.chdir(ml)
        p1 = subprocess.Popen(["git","branch"], stdout=subprocess.PIPE)
        output = p1.communicate()
        branch = None

        output = output[0].split("\n")
        for i in output:
            b = i.strip().split(" ")
            for j in b:
                if j == "*":
                    branch = max(b)
                    break

        return branch
 
    def pstatus(self):

        status = ["what the fuck are you waiting for, check your clipboard!!", 
                  "You are free to Paste the URL!!", 
                  "Guess What? you can now paste the url",
                  "Why dont you paste the URL??", 
                  "your work is done", 
                  "URL copied to clipboard!!" ]
        s = random.randint(0,5)
        print status[s]
 