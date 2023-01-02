import tkinter
from tkinter import *
from tkinter.filedialog import *
import os
import subprocess
import psutil

master = Tk()
master.overrideredirect(True)
master.configure(bg="#FFFFFF")
master.resizable(False,False)
master.geometry("400x600+200+200")
master.title("Fortnite Settings Manager")

profile = 1

try:
    mainfont = "Fortnite 15 bold"
    bigfont = "Fortnite 20 bold"
    smallfont = "Arial 10"
except:
    mainfont = "Arial 12 bold"
    bigfont = "Arial 20 bold"
    smallfont = "Arial 10"

settingsdir = os.path.expanduser('~') + "\AppData\Local\FortniteGame\Saved\Config\WindowsClient"
pgmdir = settingsdir + "\FNsettingsmanager"
mainfnsettings = settingsdir + "\GameUserSettings.ini"
settingsfile = pgmdir + "\pgmconfig.txt"

if not os.path.exists(pgmdir):
    os.makedirs(pgmdir)

if not os.path.isfile(settingsfile):
    createfile = open(settingsfile, "w")
    createfile.write("[Fortnite Settings Manager Configuration File]")
    createfile.write("\nSyncedSettings=[bMotionBlur, bShowFPS, LatencyTweak2, FortAntiAliasingMethod, TemporalSuperResolutionQuality, bRayTracing, RayTracingShadowsQuality, RayTracingReflectionsQuality, RayTracingAmbientOcclusionQuality, RayTracingAOQuality, RayTracingGIQuality, FrontendFrameRateLimit, DisplayGamma, UserInterfaceContrast, bUseHeadphoneMode, bDisableMouseAcceleration, bUseVSync, bUseDynamicResolution, ResolutionSizeX, ResolutionSizeY, AudioQualityLevel, FrameRateLimit, bUseNanite, DesiredGlobalIlluminationQuality, DesiredReflectionQuality, sg.ResolutionQuality, sg.ViewDistanceQuality, sg.AntiAliasingQuality, sg.ShadowQuality, sg.PostProcessQuality, sg.TextureQuality, sg.EffectsQuality, sg.FoliageQuality, sg.ShadingQuality, PreferredFeatureLevel, PreferredRHI, MeshQuality]")
    createfile.close()

def readconfig(location):
    config = {}
    configfile = open(location, "r")
    i = 0
    lastkeys = []
    for line in configfile:
        tempkey = "Line" + str(i)
        if ("=" in line):
            key = line[0:line.index("=")]
            value = line[line.index("=")+1:len(line)].strip("\n")
            if value != "":
                if value[0] == "[":
                    value = value.strip('][').split(', ')
            if key not in lastkeys:
                config[key] = value
            else:
                config[tempkey] = key + "=" + value
            lastkeys.append(key)
        else:
            value = line.strip("\n")
            config[tempkey] = value
        i += 1
    configfile.close()
    return config

def writeconfig(location, config):
    open(location, "w").close()
    configfile = open(location, "a")
    for i in range (0,len(config)):
        if list(config.keys())[i] == "Line%d"%(i):
            configfile.write(list(config.values())[i] + "\n")
        else:
            configfile.write(list(config.keys())[i] + "=" + list(config.values())[i] + "\n")
    configfile.close()

def move_window(event):
    master.geometry('+{0}+{1}'.format((event.x_root - 200), (event.y_root - 25)))

def togglegrass():
    global grasstoggle
    if grasstoggle == 0:
        grasstoggle = 3
        bodycanvas.itemconfig(grasslabel, text="On")
    elif grasstoggle == 3:
        grasstoggle = 0
        bodycanvas.itemconfig(grasslabel, text="Off")

def inclobfpscap(amount):
    global lobbyfpscap
    temp = lobbyfpscap + amount
    if temp > 0:
        lobbyfpscap = temp
        bodycanvas.itemconfig(lobbyfpslabel, text=lobbyfpscap)
    elif temp == 0:
        lobbyfpscap = temp
        bodycanvas.itemconfig(lobbyfpslabel, text="Uncapped")

def switchprofile(direction):
    global profile
    global lobbyfpscap
    global grasstoggle
    if direction == 1:
        if profile < 5:
            profile += 1
    elif direction == 0:
        if profile > 1:
            profile -= 1
    profilertext.delete(0, END)
    profilertext.insert(0, (readconfig(pgmdir + "\Profile%d.txt"%(profile))["Line0"]).strip("[]"))
    lobbyfpscap = int(readconfig(pgmdir + "\Profile%d.txt"%(profile))["FrontendFrameRateLimit"])
    grasstoggle = int(readconfig(pgmdir + "\Profile%d.txt"%(profile))["sg.FoliageQuality"])
    if grasstoggle == 3:
        bodycanvas.itemconfig(grasslabel, text="On")
    elif grasstoggle == 0:
        bodycanvas.itemconfig(grasslabel, text="Off")
    inclobfpscap(0)

def savetoprofile(profile, profilename):
    global grasstoggle
    global lobbyfpscap
    currentconfig = open(pgmdir + "\Profile%d.txt" % (profile), "w")
    currentconfig.write("[%s]\n" % (profilename))
    for item in readconfig(mainfnsettings):
        if item in readconfig(settingsfile)["SyncedSettings"]:
            if item == "sg.FoliageQuality":
                currentconfig.write(item + "=" + str(grasstoggle) + "\n")
            elif item == "FrontendFrameRateLimit":
                currentconfig.write(item + "=" + str(lobbyfpscap) + "\n")
            else:
                currentconfig.write(item + "=" + readconfig(mainfnsettings)[item] + "\n")
    currentconfig.close()

def exportprofile():
    exportlocation = ""
    exportlocation = asksaveasfilename(filetypes=[("Fortnite Settings Manager Save File", "*.fsm")], title="Export Fortnite Settings Manager Profile", initialfile="%s.fsm" % (readconfig(pgmdir + "\Profile%d.txt" % (profile))["Line0"]).strip("[]"))
    if exportlocation != "":
        currentconfig = open(pgmdir + "\Profile%d.txt" % (profile), "r")
        exportfile = open(exportlocation, "w")
        for line in currentconfig:
            exportfile.write(line)
        exportfile.close()
        currentconfig.close()

def importprofile(profile):
    importlocation = ""
    importlocation = askopenfilename(filetypes=[("FN Settings Manager File", "*.fsm")], title="Select a Fortnite Settings Manager Profile File to Import")
    if importlocation != "":
        currentconfig = open(pgmdir + "\Profile%d.txt" % (profile), "w")
        importfile = open(importlocation, "r")
        for line in importfile:
            if line[0] == "[":
                currentconfig.write(line)
            for item in readconfig(settingsfile)["SyncedSettings"]:
                if item in line:
                    currentconfig.write(line)
        currentconfig.close()
        importfile.close()
        switchprofile(2)

def applytogame():
    global profile
    running = False
    for p in psutil.process_iter():
        if "FortniteClient" in p.name():
            bodycanvas.itemconfig(runningtext, text="Please Close Fortnite Before Applying To Game")
            running = True
    if not running:
        bodycanvas.itemconfig(runningtext, text="")
        currentsettings = readconfig(mainfnsettings)
        profilesettings = readconfig(pgmdir + "\Profile%d.txt" % (profile))
        for item in currentsettings:
            for item2 in profilesettings:
                if (item == item2) and (not item[0:4] == "Line"):
                    currentsettings[item] = profilesettings[item2]
        writeconfig(mainfnsettings, currentsettings)

try:
    lobbyfpscap = int(readconfig(pgmdir + "\Profile%d.txt" % (profile))["FrontendFrameRateLimit"])
except:
    lobbyfpscap = 120

try:
    if int(readconfig(pgmdir + "\Profile%d.txt" % (profile))["sg.FoliageQuality"]) >= 1:
        grasstoggle = 3
    else:
        grasstoggle = 0
except:
    grasstoggle = 0

for i in range(1, 6):
    if not os.path.isfile(pgmdir + "\Profile%d.txt" % (i)):
        savetoprofile(i,("Profile%d"%(i)))

backgroundimage = PhotoImage(file ="images/backgroundimage.png")
fnlogo = PhotoImage(file ="images/pglogo.png")
fnx = PhotoImage(file ="images/fnx.png")
chooseprofile = PhotoImage(file="images/ChooseYourProfile.png")
hiddensettings = PhotoImage(file="images/HiddenSettings.png")
on = PhotoImage(file="images/on.png")
off = PhotoImage(file="images/off.png")
showgrass = PhotoImage(file="images/showgrass.png")
lobbyfps = PhotoImage(file="images/lobbyfpscap.png")

background = Canvas(master, highlightthickness=0)
bgimageholder = background.create_image(0, 0, anchor=NW, image=backgroundimage)
background.place(x=0,y=0,anchor=NW,relwidth=1, relheight=1)

mainframe = Frame(master)
mainframe.place(x=0, y=0, anchor=NW, height=60, relwidth=1)
topcanvas = Canvas(master, highlightthickness=0)
topcanvas.place(x=0, y=0, relwidth=1, relheight=1)
topcanvas.create_image(0, 0, image=backgroundimage, anchor=NW)
topcanvas.create_polygon(0,0,400,0,400,50,0,60, fill="#24293f")
topcanvas.create_image(10, 25, image=fnlogo, anchor=W)
xbutton = topcanvas.create_image(380,28, anchor=CENTER, image=fnx)

bodycanvas = Canvas(master, highlightthickness=0)
bodycanvas.place(x=0,y=60,anchor=NW, relwidth=1, relheight=1)
bodycanvas.create_image(0, -50, image=backgroundimage, anchor=NW)
bodycanvas.create_image(200,20, image=chooseprofile, anchor=N)
bodycanvas.create_image(200,150, image=hiddensettings, anchor=N)

profileleft = Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text="<", font=mainfont, command=lambda:switchprofile(0))
profileright = Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text=">", font=mainfont, command=lambda:switchprofile(1))
profilertext = Entry(master, font=mainfont, justify='center', fg="#24293f")
profilertext.insert(0, (readconfig(pgmdir + "\Profile%d.txt"%(profile))["Line0"]).strip("[]"))
profileleft.place(x= 100, y= 140, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
profileright.place(x= 300, y= 140, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
profilertext.place(x= 200, y=140, anchor=CENTER, relwidth=0.3, relheight=0.1*(400/600))

Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text="<", font=mainfont, command=lambda:togglegrass()).place(x= 160, y= 280, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text=">", font=mainfont, command=lambda:togglegrass()).place(x= 360, y= 280, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
bodycanvas.create_rectangle(260-60, 280-60-20, 260+60, 280-60+20, fill="#FFFFFF", outline="#FFFFFF")
grasslabel = bodycanvas.create_text(260, 282-60, text="Off", anchor=CENTER, font=bigfont)
grasstitle = bodycanvas.create_image(65, 280-60, image=showgrass, anchor=CENTER)

if grasstoggle == 3:
    bodycanvas.itemconfig(grasslabel, text="On")
elif grasstoggle ==0:
    bodycanvas.itemconfig(grasslabel, text="Off")

Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text="<", font=mainfont, command=lambda:inclobfpscap(-5)).place(x= 160, y= 330, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
Button(master, bg="#FFFFFF", activebackground="#cce0fa", relief="raised", text=">", font=mainfont, command=lambda:inclobfpscap(5)).place(x= 360, y= 330, anchor=CENTER, relwidth=0.15, relheight=0.1*(400/600))
bodycanvas.create_rectangle(260-60, 330-60-20, 260+60, 330-60+20, fill="#FFFFFF", outline="#FFFFFF")
lobbyfpslabel = bodycanvas.create_text(260, 332-60, text=lobbyfpscap, font=bigfont, anchor=CENTER)
lobbyfpstitle = bodycanvas.create_image(65, 330-60, image=lobbyfps, anchor=CENTER)

Button(master, bg="#FFFFFF", fg="#23293f", activebackground="#FFFFFF", activeforeground="#505465", text="Export Profile", font=mainfont, command=lambda:exportprofile()).place(x=40, y=385, anchor=NW, relwidth=0.4, relheight=0.1)
Button(master, bg="#FFFFFF", fg="#23293f", activebackground="#FFFFFF", activeforeground="#505465", text="Import Profile", font=mainfont, command=lambda:importprofile(profile)).place(x=360, y=385, anchor=NE, relwidth=0.4, relheight=0.1)
Button(master, bg="#FFFFFF", fg="#23293f", text="Save Current Game Settings To Profile", font=mainfont, command=lambda:savetoprofile(profile,profilertext.get())).place(x=200, y=450, anchor=N, relwidth=0.8, relheight=0.1)
Button(master, bg="#23293f", fg="#FFFFFF", activebackground="#505465", activeforeground="#FFFFFF", text="Apply Profile To Game", font=mainfont, command=lambda:applytogame()).place(x=200, y=515, anchor=N, relwidth=0.8, relheight=0.1)
Button(master, bg="#23293f", fg="#FFFFFF", activebackground="#505465", activeforeground="#FFFFFF", text="↪", command=lambda:subprocess.Popen(r'explorer /select,"%s"'%(mainfnsettings))).place(x=400, y=600, anchor=SE, width=20, height=20)
runningtext = bodycanvas.create_text(200, 537, anchor=S, font=smallfont, text="", fill="#FFFFFF", justify=CENTER)

if "Arial" in mainfont:
    bodycanvas.itemconfig(runningtext, text="Fortnite font missing - Please install Fortnite.otf")

def keydown(event):
    if len(profilertext.get()) > 12:
        temptextstorage = profilertext.get()
        profilertext.delete(0,END)
        profilertext.insert(0, temptextstorage[0:12])
    if not profilertext.get().isalnum():
        strippedstring = ""
        for letter in profilertext.get():
            if letter.isalnum() or (letter in "~!#$&_`;. "):
                strippedstring = strippedstring + letter
        profilertext.delete(0, END)
        profilertext.insert(0, strippedstring)

topcanvas.tag_bind(xbutton, '<Button-1>', lambda event:master.destroy())
topcanvas.bind('<B1-Motion>', move_window)
master.bind("<KeyPress>", keydown)
master.mainloop()