import sublime
import sublime_plugin
import os
import webbrowser
import subprocess

bCompareLocation = None
isWindows = False

# If we are on mac/unix
if os.name == 'posix':
    bCompareLocation = '/usr/local/bin/bcompare'

# Or we are on windows
else:
    isWindows = True
    if os.path.exists("%s\Beyond Compare 4\BCompare.exe" % os.environ['ProgramFiles(x86)']):
        bCompareLocation = '"%s\Beyond Compare 4\BCompare.exe"' % os.environ['ProgramFiles(x86)']
    else:
        bCompareLocation = "%s\Beyond Compare 4\BCompare.exe" % os.environ['ProgramFiles']

fileA = fileB = None


def recordActiveFile(f):
    global fileA
    global fileB
    fileB = fileA
    fileA = f


def runMacBeyondCompare():
    if fileA is not None and fileB is not None:
        print(
            "BeyondCompare comparing: LEFT [" + fileA + "] | RIGHT [" + fileB + "]")
        subprocess.Popen([str(bCompareLocation), str(fileA), str(fileB)])
        print("Should be open...")
    else:
        print(
            "You must have activated TWO files to compare.\nPlease select two tabs to compare and try again")
        sublime.error_message(
            "You must have activated TWO files to compare.\nPlease select two tabs to compare and try again")


def runWinBeyondCompare():
    if fileA is not None and fileB is not None:
        cmd_line = '%s "%s" "%s"' % (bCompareLocation, fileA, fileB)
        print(
            "BeyondCompare comparing: LEFT [" + fileA + "] | RIGHT [" + fileB + "]")
        subprocess.Popen(cmd_line)


class BeyondCompareCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # For Windows
        if isWindows:
            runWinBeyondCompare()
            return

        # For OSX
        if os.path.exists(bCompareLocation):
            runMacBeyondCompare()

        else:
            commandLinePrompt = sublime.ok_cancel_dialog('Could not find bcompare.\nPlease install the command line tools.', 'Do it now!')
            if commandLinePrompt:
                new = 2  # open in a new tab, if possible
                url = "http://www.scootersoftware.com/support.php?zz=kb_OSXInstallCLT"
                webbrowser.open(url, new=new)
                bCompareInstalled = sublime.ok_cancel_dialog('Once you have installed the command line tools, click the ok button to continue')
                if bCompareInstalled:
                    if os.path.exists("/usr/local/bin/bcompare"):
                        runMacBeyondCompare()

                    else:
                        sublime.error_message('Still could not find bcompare. \nPlease make sure it exists at:\n/usr/local/bin/bcompare\nand try again')

                else:
                    sublime.error_message('Please try again after you have command line tools installed.')
            else:
                sublime.error_message('Please try again after you have command line tools installed.')


class BeyondCompareFileListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.file_name() is not None and view.file_name() != fileA:
            recordActiveFile(view.file_name())
