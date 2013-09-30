
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
        self.slpath = path+"L#"+str(row)

        self.d = sublime.load_settings("ggu.sublime-settings")
        URL = MakeURL().geturl(self.slpath, self.d)

        if URL:
            sublime.set_clipboard(URL)

    def get_user(self, username):

        
        user = username.split(":")[0]
        pw = username.split(":")[1]
        self.d["user"] = user
        self.d["pw"] = pw
        URL = MakeURL().geturl(self.slpath, self.d)
        return URL

    def get_path(self,edit):

	    (row,col) = self.view.rowcol(self.view.sel()[0].begin())
	    return (self.view.file_name(),row + 1 )

class MakeURL(object):

    def __init__(self):
        
        self.dicpath = None
        self.path =  None

    def getrepo(self, path, d):
        """
            get the git repositories
        """

        self.path = path.strip('') 
        self.dicpath = path.split('/')[1:]

        repoin = self.dicpath[0]

        p2 = subprocess.Popen('echo ' + d.get("pw") +' |sudo -S locate -r \'\.git$\'| xargs -n 1 dirname ',shell=True, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = p2.communicate()
        output = output[0].strip()
        dirs = output.split("\n")

        print dirs
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

    def geturl (self, path, d):
        """
            generate the url
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

        branch = self.get_branch(maxlength)


        URL = ["http:/","github.com",d.get("username"),lleng[len(lleng)-1],"blob",branch]  

        for i in b:
             URL.append(i)

        URL = "/".join(URL)
        
        return URL

    def get_branch(self,ml):
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
    
        status = ["what the fuck are you waiting for, check your clipboard!!", "You are free to Paste the URL!!", "Guess What? you can now paste the url",
                  "Why dont you paste the URL??", "your work is done", "URL copied to clipboard!!" ]
        s = random.randint(0,5)
        print status[s]
 