import re
import os
import wx

class Mfunc():

    def __init__(self, function_name, start, end=0):
        self.function_name = function_name
        self.start = start
        self.end = end
        #self.content=''
        self.calledfunc= set([])

    #def addcontent(self,content):
    #    self.content=content

    def getstartend(self):
        return (self.start,self.end)

#    def extractfunc(self):

#         it=re.finditer(r"(\w*)\(.*\);",self.content, re.MULTILINE)
        #it=re.finditer(r"([A-Za-z_][.A-Za-z_0-9+]*)\(",self.content, re.MULTILINE)
        #if it:
        #    for ii in it:
        #        self.calledfunc.append(ii.group(1))

    def __str__(self):

        return str(self.function_name) + '\n' + str(self.start) + "--" + str(self.end) + '\n[' + ','.join(self.calledfunc) + ']'

obj_list=[]
c_inbuilt = ['for','if','while','switch','init','return']

for dir, dirs, files in os.walk('.'):
    for f in files:
      if f.endswith(".c"):
        file_obj_list = []
        path = os.path.join(dir, f)


        string=''
        myreadlines=[]

        with open(path,"r") as f:

            num_lines = sum(1 for _ in f)
            f.seek(0)
            string=f.read()
        #     readlines=f.readlines()
            myreadlines=string.split('\n')

        end='.*\n'
        line=[]
        for m in re.finditer(end, string):
            line.append(m.end())

        print "****",line

        pattern = "((void|boolean|int|string|uMonoByte|uDiByte|uTetraByte)\s(?<=[\s:~])\*?([\w*]*)\s*\(([\w\s,<>\[\].=&':/*]*?)\)\s*(const|REENTRANT)?\s*){"
        match=re.compile(pattern, re.MULTILINE|re.DOTALL)

        #obj_list=[]

        for m in re.finditer(match, string):
            #print 'lineno :%d, %s' %(next(i+1 for i in range(len(line)) if line[i]>m.start(1)), m.group(1))
            a,b=(next(i+1 for i in range(len(line)) if line[i]>m.start(1)), m.group(3))

            temp= Mfunc(b.strip(),a)
            file_obj_list.append(temp)
            #print ('end', a-1)
            if len(file_obj_list) > 1:
                file_obj_list[-2].end = a-1


        file_obj_list[-1].end = num_lines

        for i in file_obj_list:
            s,e=i.getstartend()
            #print s,e
            ts=''
            #print path
            #print (s,e)
            for j in range(s,e):
                #print j
                ts=ts+myreadlines[j]
            #i.content=ts
            #i.extractfunc()
            it=re.finditer(r"([A-Za-z_][.A-Za-z_0-9+]*)\(",ts, re.MULTILINE)
            if it:
               for ii in it:
                   if (ii.group(1)).strip() not in c_inbuilt:
                       #print ii.group(1)
                       i.calledfunc.add((ii.group(1)).strip())

        obj_list.extend(file_obj_list)

final_object = {}
for func_obj in obj_list:
    final_object[func_obj.function_name] = func_obj

print len(final_object)
for k,e in final_object.items():
    print 'object name : ' + k
    print list(e.calledfunc)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mkeys = final_object.keys()
mkeys.sort()

def travel(ob,vnode,vtree):
    mkeys=final_object.keys()
    if ob != None:
        print ob.function_name
        vlist=list(ob.calledfunc)
        vtree.SetItemBold(vnode, bold=True)
        # tnode=vtree.AppendItem(vnode, ob.function_name)
        print vlist

        if vlist:
            for cfunc in vlist:
                tnode1 = vtree.AppendItem(vnode, cfunc)
                print '****************' + cfunc
                if cfunc in mkeys:
                    ff=final_object[cfunc]
                    if ff:
                        travel(ff,tnode1,vtree)
        else:
            return
    else:
        return

class TreeFrame(wx.Frame):

    def __init__(self):

        dialog = wx.SingleChoiceDialog(None, "Pick Your Coice", "Choices", mkeys)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            self.state = dialog.GetStringSelection()
            dialog.Destroy()

        wx.Frame.__init__(self, None, title='TreeCtrl',size=(600,600))
        mpanel = wx.Panel(self, -1)
        # Create a box sizer that will contain the left panel contents

        self.tree_ctrl = wx.TreeCtrl(mpanel, -1, style=wx.TR_DEFAULT_STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree_ctrl, 1, wx.EXPAND | wx.ALL)

        mbutton=wx.Button(mpanel, wx.ID_ANY, 'Choose Another Function')
        mbutton.SetBackgroundColour('blue')
        mbutton.SetForegroundColour('white')

        self.Bind(wx.EVT_BUTTON, self.onOK, mbutton)

        sizer.Add(mbutton,0,wx.CENTER)
        mpanel.SetSizer(sizer)

        myobj=final_object[self.state]
        childs=myobj.calledfunc
        # Add the tree root

        root = self.tree_ctrl.AddRoot(myobj.function_name)
        self.tree_ctrl.SetItemBold(root,bold=True)

        travel(myobj,root,self.tree_ctrl)

        self.tree_ctrl.ExpandAll()
        self.Centre()

    def onOK(self, event):
        # mkeys = final_object.keys()
        # mkeys.sort()
        dialog = wx.SingleChoiceDialog(None, "Pick Your Coice", "Choices", mkeys)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            self.state = dialog.GetStringSelection()
            dialog.Destroy()
        self.tree_ctrl.DeleteAllItems()
        myobj = final_object[self.state]
        childs = myobj.calledfunc
        # Add the tree root

        root = self.tree_ctrl.AddRoot(myobj.function_name)
        self.tree_ctrl.SetItemBold(root, bold=True)

        travel(myobj, root, self.tree_ctrl)

        self.tree_ctrl.ExpandAll()


if __name__ == '__main__':
    app = wx.App(0)
    frame = TreeFrame()
    frame.Show()
    app.MainLoop()


