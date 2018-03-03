from enigma import getDesktop
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.About import about
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
import Components.Harddisk
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists
import os
from skin import parseColor
from boxbranding import getImageDistro, getDriverDate
PLUGINVERSION = '2.7 - 29.11.2017 - EGAMI Team'
EGAMIBootInstallation_Skin = '\n\t\t<screen name="EGAMIBootInstallation" position="center,center" size="902,380" title="EGAMIBoot - Installation" >\n\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <widget name="config" position="10,160" size="840,200" scrollbarMode="showOnDemand" transparent="1"/>\n\t\t      <ePixmap pixmap="skin_default/buttons/red.png" position="10,290" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="150,290" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/blue.png" position="300,290" size="140,40" alphatest="on" />\n\t\t      <widget name="key_red" position="10,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_green" position="150,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_blue" position="300,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t</screen>'
EGAMIBootImageInstall_Skin = '\n\t\t    <screen name="EGAMIBootImageInstall" position="center,center" size="770,340" title="EGAMIBoot - Image Installation" >\n\t\t\t      <widget name="config" position="10,10" size="750,220" scrollbarMode="showOnDemand" transparent="1"/>\n\t\t\t      <ePixmap pixmap="skin_default/buttons/red.png" position="10,290" size="140,40" alphatest="on" />\n\t\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="150,290" size="140,40" alphatest="on" />\n\t\t\t      <ePixmap pixmap="skin_default/buttons/yellow.png" position="290,290" size="140,40" alphatest="on" />\n\t\t\t      <widget name="HelpWindow" position="330,310" zPosition="5" size="1,1" transparent="1" alphatest="on" />      \n\t\t\t      <widget name="key_red" position="10,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t      <widget name="key_green" position="150,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t      <widget name="key_yellow" position="290,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t    </screen>'

def Freespace(dev):
    statdev = os.statvfs(dev)
    space = statdev.f_bavail * statdev.f_frsize / 1024
    print '[EGAMIBoot] Free space on %s = %i kilobytes' % (dev, space)
    return space


class EGAMIBootInstallation(Screen):

    def __init__(self, session):
        self.skin = EGAMIBootInstallation_Skin
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Install'))
        self['key_blue'] = Label(_('Devices Panel'))
        self['label1'] = Label(_('Welcome to EGAMIBoot %s MultiBoot Plugin installation.') % PLUGINVERSION)
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\n\nPlease choose a device where You would like to install EGAMIBoot:'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.close,'green': self.install,'back': self.close,'blue': self.devpanel})
        self.updateList()

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, myhdd = ('', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'
                    continue

            f.close()
        else:
            self['label2'].setText(_('Sorry it seems that there are not Linux formatted devices mounted on your STB. To install EGAMIBoot you need a Linux formatted part1 device. Click on the blue button to open Egami Devices Panel'))
            fileExists('/proc/mounts')
        if mycf:
            self.list.append(mycf)
        else:
            mycf
        if myusb:
            self.list.append(myusb)
        else:
            myusb
        if myusb2:
            self.list.append(myusb2)
        else:
            myusb2
        if myusb3:
            self.list.append(myusb3)
        else:
            myusb3
        if mysd:
            mysd
            self.list.append(mysd)
        else:
            mysd
        if myhdd:
            myhdd
            self.list.append(myhdd)
        else:
            myhdd
        self['config'].setList(self.list)

    def devpanel(self):
        try:
            from EGAMI.EGAMI_devices_menu import EGDeviceManager
            self.session.open(EGDeviceManager)
        except:
            self.session.open(MessageBox, _('You are not running EGAMI Image. You must mount devices Your self.'), MessageBox.TYPE_INFO)

    def myclose(self):
        self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

    def checkReadWriteDir(self, configele):
        supported_filesystems = frozenset(('ext4', 'ext3', 'ext2', 'nfs'))
        candidates = []
        mounts = Components.Harddisk.getProcMounts()
        for partition in Components.Harddisk.harddiskmanager.getMountedPartitions(False, mounts):
            if partition.filesystem(mounts) in supported_filesystems:
                candidates.append((partition.description, partition.mountpoint))

        if candidates:
            locations = []
            for validdevice in candidates:
                locations.append(validdevice[1])

            if Components.Harddisk.findMountPoint(os.path.realpath(configele)) + '/' in locations or Components.Harddisk.findMountPoint(os.path.realpath(configele)) in locations:
                if fileExists(configele, 'w'):
                    return True
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not writable.\nMake sure you select a writable directory instead.') % dir, type=MessageBox.TYPE_ERROR)
                return False
            else:
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                return False
        else:
            dir = configele
            self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
            return False

    def install(self):
        check = False
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    check = True
                    continue
                if line.find('/media/usb') != -1:
                    check = True
                    continue
                if line.find('/media/usb2') != -1:
                    check = True
                    continue
                if line.find('/media/usb3') != -1:
                    check = True
                    continue
                if line.find('/media/card') != -1:
                    check = True
                    continue
                if line.find('/hdd') != -1:
                    check = True
                    continue

            f.close()
        else:
            fileExists('/proc/mounts')
        if check == False:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to install EGAMI Multiboot!'), MessageBox.TYPE_INFO)
        else:
            fileExists('/boot/dummy')
            self.mysel = self['config'].getCurrent()
            if self.checkReadWriteDir(self.mysel):
                message = _('Do You really want to install EGAMIBoot in:\n ') + self.mysel + '?'
                ybox = self.session.openWithCallback(self.install2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.close()

    def install2(self, yesno):
        if yesno:
            cmd2 = 'mkdir /media/egamiboot;mount ' + self.mysel + ' /media/egamiboot'
            os.system(cmd2)
            cmd = 'mkdir ' + self.mysel + 'EgamiBootI;mkdir ' + self.mysel + 'EgamiBootUpload'
            os.system(cmd)
            os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/bin/egamiinit /sbin/egamiinit')
            os.system('chmod 777 /sbin/egamiinit;chmod 777 /sbin/init;ln -sfn /sbin/egamiinit /sbin/init')
            os.system('mv /etc/init.d/volatile-media.sh /etc/init.d/volatile-media.sh.back')
            out2 = open('/media/egamiboot/EgamiBootI/.egamiboot', 'w')
            out2.write('Flash')
            out2.close()
            out = open('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_location', 'w')
            out.write(self.mysel)
            out.close()
            string = getDriverDate()
            year = string[0:4]
            month = string[4:6]
            day = string[6:8]
            driversdate = ('-').join((year, month, day))
            out = open('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_info', 'w')
            out.write('Kernel\n')
            out.write('Kernel-Version: ' + about.getKernelVersionString() + '\n')
            out.write('Drivers\n')
            out.write('Drivers-Version: ' + str(driversdate) + '\n')
            out.close()
            os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_location /etc/egami/')
            image = getImageDistro()
            if fileExists('/etc/image-version'):
                if 'build' not in image:
                    f = open('/etc/image-version', 'r')
                    for line in f.readlines():
                        if 'build=' in line:
                            image = image + ' build ' + line[6:-1]
                            open('/media/egamiboot/EgamiBootI/.Flash', 'w').write(image)
                            break

                    f.close()
            self.myclose2(_('EGAMIBoot has been installed succesfully!'))
        else:
            self.session.open(MessageBox, _('Installation aborted !'), MessageBox.TYPE_INFO)


class EGAMIBootImageChoose(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n\t\t\t<screen name="EGAMIBootImageChoose" position="center,center" size="1040,670">\n\t\t\t\t<widget name="label2" position="145,10" size="440,30" zPosition="1" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label3" position="145,43" size="440,30" zPosition="1" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label4" position="145,76" size="440,30" zPosition="1" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label5" position="145,109" size="440,30" zPosition="1" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label6" position="570,10" size="440,30" zPosition="1" halign="right" font="Regular;28" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label7" position="570,43" size="440,30" zPosition="1" halign="right" font="Regular;28" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label8" position="570,76" size="440,30" zPosition="1" halign="right" font="Regular;28" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label9" position="570,109" size="440,30" zPosition="1" halign="right" font="Regular;28" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label10" position="145,142" size="440,30" zPosition="1" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label11" position="570,142" size="440,30" zPosition="1" halign="right" font="Regular;28" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label1" position="25,175" size="1020,30" zPosition="1" halign="center" font="Regular;28" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="device_icon" position="25,20" size="80,80" alphatest="on" />\n\t\t\t\t<widget name="free_space_progressbar" position="265,50" size="500,15" borderWidth="1" zPosition="3" />\n\t\t\t\t<widget name="config" itemHeight="50" font="Regular;28" position="25,220" size="840,150" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap position="40,604" size="100,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="250,604" size="100,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="500,604" size="100,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<ePixmap position="780,604" size="100,40" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="blend"/>\n\t\t\t\t<widget name="key_red" position="80,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="red" transparent="1" />\n\t\t\t\t<widget name="key_green" position="290,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="green" transparent="1" />\n\t\t\t\t<widget name="key_yellow" position="540,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="yellow" transparent="1" />\n\t\t\t\t<widget name="key_blue" position="820,604" zPosition="1" size="270,35" font="Regular;32" valign="top" halign="left" backgroundColor="blue" transparent="1" />\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen name="EGAMIBootImageChoose" position="center,center" size="902,380" title="EGAMIBoot - Menu" >\n\t\t\t\t<widget name="label2" position="145,10" size="440,30" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label3" position="145,35" size="440,30" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label4" position="145,60" size="440,30" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label5" position="145,85" size="440,30" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label6" position="420,10" size="440,30" zPosition="1" halign="right" font="Regular;20" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label7" position="420,35" size="440,30" zPosition="1" halign="right" font="Regular;20" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label8" position="420,60" size="440,30" zPosition="1" halign="right" font="Regular;20" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label9" position="420,85" size="440,30" zPosition="1" halign="right" font="Regular;20" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label10" position="145,110" size="440,30" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="label11" position="420,110" size="440,30" zPosition="1" halign="right" font="Regular;20" backgroundColor="#9f1313" foregroundColor="#00389416" transparent="1"/>\n\t\t\t\t<widget name="label1" position="25,145" size="840,22" zPosition="1" halign="center" font="Regular;18" backgroundColor="#9f1313" transparent="1"/>\n\t\t\t\t<widget name="device_icon" position="25,20" size="80,80" alphatest="on" />\n\t\t\t\t<widget name="free_space_progressbar" position="265,42" size="500,13" borderWidth="1" zPosition="3" />\n\t\t\t\t<widget name="config" position="25,180" size="840,150" scrollbarMode="showOnDemand"/>\n\t\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="10,340" size="150,40" alphatest="on" />\n\t\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="260,340" size="150,40" alphatest="on" />\n\t\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="520,340" size="150,40" alphatest="on" />\n\t\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="750,340" size="150,40" alphatest="on" />\n\t\t\t\t<widget name="key_red" position="5,340" zPosition="1" size="160,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t\t<widget name="key_green" position="255,340" zPosition="1" size="160,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t\t<widget name="key_yellow" position="515,340" zPosition="1" size="160,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t\t<widget name="key_blue" position="745,340" zPosition="1" size="160,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self.setTitle('EGAMIBoot %s - Menu' % PLUGINVERSION)
        self['device_icon'] = Pixmap()
        self['free_space_progressbar'] = ProgressBar()
        self['linea'] = ProgressBar()
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Boot Image'))
        self['key_green'] = Label(_('Install Image'))
        self['key_yellow'] = Label(_('Remove Image '))
        self['key_blue'] = Label(_('Advanced'))
        self['label2'] = Label(_('EGAMIBoot is running from:'))
        self['label3'] = Label(_('Used:'))
        self['label4'] = Label(_('Available:'))
        self['label5'] = Label(_('EGAMIBoot is running image:'))
        self['label6'] = Label('')
        self['label7'] = Label('')
        self['label8'] = Label('')
        self['label9'] = Label('')
        self['label10'] = Label(_('Number of installed images in EGAMIBoot:'))
        self['label11'] = Label('')
        self['label1'] = Label(_('Here is the list of installed images in Your STB. Please choose an image to boot.'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.boot,
           'green': self.install,
           'yellow': self.remove,
           'blue': self.advanced,
           'back': self.close
           })
        self.onShow.append(self.updateList)

    def updateList(self):
        self.list = []
        try:
            pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot'
            f = open(pluginpath + '/.egamiboot_location', 'r')
            mypath = f.readline().strip()
            f.close()
        except:
            mypath = '/media/hdd'

        icon = 'dev_usb.png'
        if 'card' in mypath or 'sd' in mypath:
            icon = 'dev_sd.png'
        else:
            if 'hdd' in mypath:
                icon = 'dev_hdd.png'
            else:
                if 'cf' in mypath:
                    icon = 'dev_cf.png'
        icon = pluginpath + '/images/' + icon
        png = LoadPixmap(icon)
        self['device_icon'].instance.setPixmap(png)
        device = '/media/egamiboot'
        dev_free = dev_free_space = def_free_space_percent = ''
        rc = os.system('df > /tmp/ninfo.tmp')
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:
                    if totsp == 5:
                        dev_free = parts[1]
                        dev_free_space = parts[3]
                        def_free_space_percent = parts[4]
                    else:
                        dev_free = 'N/A   '
                        dev_free_space = parts[2]
                        def_free_space_percent = parts[3]
                    break

            f.close()
            os.remove('/tmp/ninfo.tmp')
        self.availablespace = dev_free_space[0:-3]
        perc = int(def_free_space_percent[:-1])
        self['free_space_progressbar'].setValue(perc)
        green = '#00389416'
        red = '#00ff2525'
        yellow = '#00ffe875'
        orange = '#00ff7f50'
        if perc < 30:
            color = green
        else:
            if perc < 60:
                color = yellow
            else:
                if perc < 80:
                    color = orange
                else:
                    color = red
        self['label6'].instance.setForegroundColor(parseColor(color))
        self['label7'].instance.setForegroundColor(parseColor(color))
        self['label8'].instance.setForegroundColor(parseColor(color))
        self['label9'].instance.setForegroundColor(parseColor(color))
        self['label11'].instance.setForegroundColor(parseColor(color))
        self['free_space_progressbar'].instance.setForegroundColor(parseColor(color))
        try:
            f2 = open('/media/egamiboot/EgamiBootI/.egamiboot', 'r')
            mypath2 = f2.readline().strip()
            f2.close()
        except:
            mypath2 = 'Flash'

        if mypath2 == 'Flash':
            image = getImageDistro()
            if fileExists('/etc/image-version'):
                if 'build' not in image:
                    f = open('/etc/image-version', 'r')
                    for line in f.readlines():
                        if 'build=' in line:
                            image = image + ' build ' + line[6:-1]
                            open('/media/egamiboot/EgamiBootI/.Flash', 'w').write(image)
                            break

                    f.close()
        else:
            if fileExists('/media/egamiboot/EgamiBootI/.Flash'):
                f = open('/media/egamiboot/EgamiBootI/.Flash', 'r')
                image = f.readline().strip()
                f.close()
        image = ' [' + image + ']'
        self.list.append('Flash' + image)
        self['label6'].setText(mypath)
        self['label7'].setText(def_free_space_percent)
        self['label8'].setText(dev_free_space[0:-3] + ' MB')
        self['label9'].setText(mypath2)
        mypath = '/media/egamiboot/EgamiBootI/'
        myimages = os.listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.list.append(fil)

        self['label11'].setText(str(len(self.list) - 1))
        self['config'].setList(self.list)

    def myclose(self):
        self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

    def boot(self):
        self.mysel = self['config'].getCurrent()
        if self.mysel:
            out = open('/media/egamiboot/EgamiBootI/.egamiboot', 'w')
            out.write(self.mysel)
            out.close()
            os.system('rm /tmp/.egamireboot')
            message = _('Are you sure you want to Boot Image:\n') + self.mysel + ' ?'
            ybox = self.session.openWithCallback(self.boot2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Boot Confirmation'))
        else:
            self.mysel

    def boot2(self, yesno):
        if yesno:
            os.system('touch /tmp/.egamireboot')
            os.system('reboot -f')
        else:
            os.system('touch /tmp/.egamireboot')
            self.close()

    def remove(self):
        self.mysel = self['config'].getCurrent()
        if self.mysel:
            f = open('/media/egamiboot/EgamiBootI/.egamiboot', 'r')
            mypath = f.readline().strip()
            f.close()
            try:
                if mypath == self.mysel:
                    self.session.open(MessageBox, _('Sorry you cannot delete the image currently booted from.'), MessageBox.TYPE_INFO, 4)
                if self.mysel.startswith('Flash'):
                    self.session.open(MessageBox, _('Sorry you cannot delete Flash image'), MessageBox.TYPE_INFO, 4)
                else:
                    out = open('/media/egamiboot/EgamiBootI/.egamiboot', 'w')
                    out.write('Flash')
                    out.close()
                    message = _('Are you sure you want to delete Image:\n ') + self.mysel + ' now ?'
                    ybox = self.session.openWithCallback(self.remove2, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Delete Confirmation'))
            except:
                print 'no image to remove'

        else:
            self.mysel

    def up(self):
        self.list = []
        self['config'].setList(self.list)
        self.updateList()

    def up2(self):
        try:
            self.list = []
            self['config'].setList(self.list)
            self.updateList()
        except:
            print ' '

    def remove2(self, yesno):
        if yesno:
            cmd = "echo -e '\n\nEGAMIBoot deleting image..... '"
            cmd1 = 'rm -r /media/egamiboot/EgamiBootI/' + self.mysel
            self.session.openWithCallback(self.up, Console, _('EGAMIBoot: Deleting Image'), [cmd, cmd1])
        else:
            self.session.open(MessageBox, _('Removing canceled!'), MessageBox.TYPE_INFO)

    def installMedia(self):
        images = False
        myimages = os.listdir('/media/egamiboot/EgamiBootUpload')
        print myimages
        for fil in myimages:
            if fil.endswith('.zip'):
                images = True
                break
            if fil.endswith('.nfi'):
                images = True
                break
            else:
                images = False

        if images == True:
            self.session.openWithCallback(self.up2, EGAMIBootImageInstall)
        else:
            mess = _('The /media/egamiboot/EgamiBootUpload directory is EMPTY!\n\nPlease upload one of the file:\nVU+ Solo2 images\n- ZIP format image e.x\nOpenPLi-4.0-beta-vusolo2-20140304_usb.zip\n\nXtrend ET Series images\n- ZIP format image e.x\nOpenVix-4.0-Helios-et9x00-20140424_usb.zip\n\n')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def install(self):
        count = 0
        for fn in os.listdir('/media/egamiboot/EgamiBootI'):
            dirfile = '/media/egamiboot/EgamiBootI/' + fn
            if os.path.isdir(dirfile):
                count = count + 1

        if count > 19:
            myerror = _('Sorry you can install a max of 20 images.')
            self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        else:
            menulist = []
            menulist.append((_('Install from /media/egamiboot/EgamiBootUpload'), 'media'))
            menulist.append((_('Install from Internet (OpenPLi,OpenVix,OpenATV,OpenMips,HDMU)'), 'internet'))
            self.session.openWithCallback(self.menuCallback, ChoiceBox, title='Choose they way for installation', list=menulist)

    def menuCallback(self, choice):
        self.show()
        if choice is None:
            return
        if choice[1] == 'internet':
            from Plugins.Extensions.EGAMIBoot.download_images import EGAMIChooseOnLineImage
            self.session.open(EGAMIChooseOnLineImage)
        if choice[1] == 'media':
            self.installMedia()
        return

    def advanced(self):
        menulist = []
        menulist.append((_('Remove EGAMIBoot'), 'rmegamiboot'))
        menulist.append((_('Remove all installed images'), 'rmallimg'))
        self.session.openWithCallback(self.menuAdvancedCallback, ChoiceBox, title=_('What would You like to do ?'), list=menulist)

    def menuAdvancedCallback(self, choice):
        self.show()
        if choice is None:
            return
        if choice[1] == 'rmegamiboot':
            cmd0 = "echo -e '\n\nEGAMIBoot preparing to remove....'"
            cmd1 = 'rm /sbin/egamiinit'
            cmd1a = "echo -e '\n\nEGAMIBoot removing boot manager....'"
            cmd2 = 'rm /sbin/init'
            cmd3 = 'ln -sfn /sbin/init.sysvinit /sbin/init'
            cmd4 = 'chmod 777 /sbin/init'
            cmd4a = "echo -e '\n\nEGAMIBoot restoring media mounts....'"
            cmd5 = 'mv /etc/init.d/volatile-media.sh.back /etc/init.d/volatile-media.sh'
            cmd6 = 'rm /media/egamiboot/EgamiBootI/.egamiboot'
            cmd7 = 'rm /media/egamiboot/EgamiBootI/.Flash'
            cmd8 = 'rm /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_location'
            cmd8a = "echo -e '\n\nEGAMIBoot remove complete....'"
            self.session.openWithCallback(self.close, Console, _('EGAMIBoot is removing...'), [cmd0, cmd1, cmd1a, cmd2, cmd3, cmd4, cmd4a, cmd5, cmd6, cmd7, cmd8, cmd8a])
        if choice[1] == 'rmallimg':
            cmd = "echo -e '\n\nEGAMIBoot deleting images..... '"
            cmd1 = 'rm -rf /media/egamiboot/EgamiBootI/*'
            self.session.openWithCallback(self.updateList, Console, _('EGAMIBoot: Deleting All Images'), [cmd, cmd1])
        return


class EGAMIBootImageInstall(Screen, ConfigListScreen):

    def __init__(self, session):
        self.skin = EGAMIBootImageInstall_Skin
        Screen.__init__(self, session)
        fn = 'NewImage'
        sourcelist = []
        for fn in os.listdir('/media/egamiboot/EgamiBootUpload'):
            if fn.find('.zip') != -1:
                fn = fn.replace('.zip', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.nfi') != -1:
                fn = fn.replace('.nfi', '')
                sourcelist.append((fn, fn))
                continue

        if len(sourcelist) == 0:
            sourcelist = [
             ('None', 'None')]
        self.source = ConfigSelection(choices=sourcelist)
        self.target = ConfigText(fixed_size=False)
        self.sett = ConfigYesNo(default=False)
        self.CpyPlug = ConfigYesNo(default=False)
        self.CpyChannels = ConfigYesNo(default=True)
        self.patchFTP = ConfigYesNo(default=True)
        self.target.value = ''
        self.curselimage = ''
        try:
            if self.curselimage != self.source.value:
                self.target.value = self.source.value
                self.curselimage = self.source.value
        except:
            pass

        self.createSetup()
        ConfigListScreen.__init__(self, self.list, session=session)
        self.source.addNotifier(self.typeChange)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'CiSelectionActions', 'VirtualKeyboardActions'], {'cancel': self.cancel,
           'red': self.cancel,
           'green': self.imageInstall,
           'yellow': self.openKeyboard
           }, -2)
        self['key_green'] = Label(_('Install'))
        self['key_red'] = Label(_('Cancel'))
        self['key_yellow'] = Label(_('Keyboard'))
        self['HelpWindow'] = Pixmap()
        self['HelpWindow'].hide()

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Source Image file'), self.source))
        self.list.append(getConfigListEntry(_('Image Name'), self.target))
        self.list.append(getConfigListEntry(_('Copy Channel list ?'), self.CpyChannels))
        self.list.append(getConfigListEntry(_('Copy Settings ( not recommend ) ?'), self.sett))
        self.list.append(getConfigListEntry(_('Patch FTP (recommend)'), self.patchFTP))

    def typeChange(self, value):
        self.createSetup()
        self['config'].l.setList(self.list)
        if self.curselimage != self.source.value:
            self.target.value = self.source.value[:-13]
            self.curselimage = self.source.value

    def openKeyboard(self):
        sel = self['config'].getCurrent()
        if sel:
            if sel == self.target:
                if self['config'].getCurrent()[1].help_window.instance is not None:
                    self['config'].getCurrent()[1].help_window.hide()
            self.vkvar = sel[0]
            if self.vkvar == _('Image Name'):
                self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)
        return

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return

    def imageInstall(self):
        if self.check_free_space():
            pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot'
            myerror = ''
            source = self.source.value.replace(' ', '')
            target = self.target.value.replace(' ', '')
            for fn in os.listdir('/media/egamiboot/EgamiBootI'):
                if fn == target:
                    myerror = _('Sorry, an Image with the name ') + target + _(' is already installed.\n Please try another name.')
                    continue

            if source == 'None':
                myerror = _('You have to select one Image to install.\nPlease, upload your zip file in the folder: /media/egamiboot/EgamiBootUpload and select the image to install.')
            if target == '':
                myerror = _('You have to provide a name for the new Image.')
            if target == 'Flash':
                myerror = _('Sorry this name is reserved. Choose another name for the new Image.')
            if len(target) > 35:
                myerror = _('Sorry the name of the new Image is too long.')
            if myerror:
                myerror
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
            else:
                myerror
                message = "echo -e '\n\n"
                message += _('EGAMIBoot will install the new image.\n\n')
                message += _('Please: DO NOT reboot your STB and turn off the power.\n\n')
                message += _('The new image will be installed and auto booted in few minutes.\n\n')
                message += "'"
                if fileExists(pluginpath + '/ex_init.py'):
                    cmd1 = 'python ' + pluginpath + '/ex_init.py'
                else:
                    cmd1 = 'python ' + pluginpath + '/ex_init.pyo'
                cmd = '%s %s %s %s %s %s %s' % (cmd1, source, target.replace(' ', '.'), str(self.sett.value), str(self.CpyPlug.value), str(self.CpyChannels.value), str(self.patchFTP.value))
                print '[EGAMI-BOOT]: ', cmd
                self.session.open(Console, _('EGAMIBoot: Install new image'), [message, cmd])

    def check_free_space(self):
        if Freespace('/media/egamiboot/EgamiBootUpload') < 300000:
            self.session.open(MessageBox, _('Not enough free space on /media/egamiboot/ !!\nYou need at least 300Mb free space.\n\nExit plugin.'), type=MessageBox.TYPE_ERROR)
            return False
        return True

    def cancel(self):
        self.close()


def main(session, **kwargs):
#    m = eEGAMI.getInstance().checkkernel()
    if getBoxType in ('vusolo2'):
        try:
            f = open('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_location', 'r')
            mypath = f.readline().strip()
            f.close()
            if not fileExists('/media/egamiboot'):
                os.mkdir('/media/egamiboot')
            cmd = 'mount ' + mypath + ' /media/egamiboot'
            os.system(cmd)
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/egamiboot') != -1:
                    line = line[0:9]
                    break

            cmd = 'mount ' + line + ' ' + mypath
            os.system(cmd)
            cmd = 'mount ' + mypath + ' /media/egamiboot'
            os.system(cmd)
        except:
            print '[EGAMIBoot] error'

        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/.egamiboot_location'):
            if fileExists('/media/egamiboot/EgamiBootI/.egamiboot'):
                session.open(EGAMIBootImageChoose)
            else:
                session.open(EGAMIBootInstallation)
        else:
            session.open(EGAMIBootInstallation)
    else:
        session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)


def menu(menuid, **kwargs):
#    m = eEGAMI.getInstance().checkkernel()
    if getBoxType in ('vusolo2'):
        if menuid == 'mainmenu':
            return [(_('EGAMI MultiBoot'), main, 'egami_boot', 1)]
        return []
    return []


from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        return [
         PluginDescriptor(name='EGAMIBoot', description='EGAMI MultiBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu),
         PluginDescriptor(name='EGAMIBoot', description=_('E2 Light Multiboot'), icon='plugin_iconhd.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
    return [
     PluginDescriptor(name='EGAMIBoot', description='EGAMI MultiBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu),
     PluginDescriptor(name='EGAMIBoot', description=_('E2 Light Multiboot'), icon='plugin_icon.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
