
import sublime, sublime_plugin
import itertools
import os
import subprocess
import random, sys
sys.path.append('~/.config/sublime-text-2/GGU-SL/config.py')
from config import Config


class GguCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		path, row = self.get_path(edit)
		slpath = path+'L#'+str(row)
		URL = MakeURL().geturl(slpath)
		sublime.set_clipboard(URL)

	def get_path(self,edit):

	    (row,col) = self.view.rowcol(self.view.sel()[0].begin())
	    return (self.view.file_name(),row + 1 )

class MakeURL(object):
    """
        This class generate the URL and copy it to clipboard
    """
    def __init__(self):

        self.dicpath = None
        self.path =  None

    def getrepo(self, path):
        """
            get the git repositories
        """

        self.path = path 
        self.dicpath = path.split('/')[1:]

        repoin = self.dicpath[0]

        pw = Config().get_pw()
 
        p2 = subprocess.Popen('echo ' + pw +' |sudo -S find /'+ repoin+ ' -type d -name .git | xargs -n 1 dirname ',shell=True, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output = p2.communicate()
    
        dirs = output[0].split("\n")

        sorted_dict = []

        for i in dirs:
            for m,n in zip(i.split("/")[1:],self.dicpath):
                if m != n:
                    i = []
            sorted_dict.append(i)

        def IsEmpty(inList):
            if isinstance(inList, list): # Is a list
                return all( map(IsEmpty, inList) )
            return False 

        if IsEmpty(sorted_dict):
            print "I only work on git repo!!"
            sys.exit()
        else:
            return sorted_dict

    def geturl (self, path):
        """
            generate the url
        """
        dirs = self.getrepo(path)
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
        user = Config().get_username()

        URL = ["http:/","github.com",user,lleng[len(lleng)-1],"blob",branch]  

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
 
