import os, time, datetime, pysftp, paramiko, getpass, posixpath
from stat import S_ISDIR
import signal

TIMEOUT = 80 #waits for 80 seconds for timeout
    
'''Signal handler is used to handle keyboard interrupt CTRL+c'''
def signal_handle(signum, frame):
    print("You wished to close the client by pressing CTRL+c. \n Until next time")
    exit()

signal.signal(signal.SIGINT, signal_handle)

'''Prints all the options available on the console'''
def displayOption():
        print("\n*******************************************************************************************************************")
        for option in options:
            print(option)
        print("*******************************************************************************************************************\n")

'''Single file download from server'''
def getfile(filename,sftpconn):
    
        try:
            sftpconn.get(filename, preserve_mtime=True)#downloads the file from server w.r.t. server time
        except IOError as e:#if remote folder does not exist then error is handled
            return False
        except OSError as e:#if local folder does not exist then error is handled
            return False
        
        if os.path.exists('./'+filename):#verifies downloaded file
            return True
        else:
            return False
                
'''Uploads a file to server uses pysftp.put() function'''
def putfile(filepath,filename,sftpconn):
    try:
        sftpconn.put(filepath+"/"+filename,confirm=True, preserve_mtime=False)#uploads the file to server
    except IOError as e:#if remote folder does not exist then error is handled
        return False
    except OSError as e:#if local folder does not exist then error is handled
        return False
        
    if sftpconn.exists(filepath+"/"+filename):#confirms the uploaded file on server
        return True
    else:
        return False

'''Uploads multiple files to server uses putfile() function internally'''
def putfiles(filepath, filesnames, sftpconn):
    
    for i in filesnames:#sends files one by one to the putfile() function
        if os.path.isfile(i) and os.path.exists(i):#verifies whether the files exist in local machine
            print(f"Uploading file:{i}")
            sftpconn.put(filepath+"/"+i,confirm=True, preserve_mtime=False)#uploads the file to server
            
            if sftpconn.exists(i):#confirms the uploaded file on server
                print("File Uploaded Successfully")
            else:
                print("File Upload Failed")
        else:
            print(f"Filename you entered does not exists.\n Please try again")
           
'''Used to concat user group and other permissions numerical values'''
def add(up,gp,op):
    print("assigning permissions")
    return int(up+gp+op)
    
    
def FileOptions(sftpconn):
        global login_user, working_dir
        displayOption()
       
        while(True):
            
            print(f"you are now in the following directory :{sftpconn.pwd}")#prints the present working directory
            print("Enter your choice:")
            choice = input()
            
            if choice.lower() == "help":#displays the options
                displayOption()
                
            if choice.lower() == "listdir": #lists all the files and folders in the current directory
                for info in sftpconn.listdir_attr(remotepath='.'):#displays files and folder information like we see in console for command ls -al
                    print(info)
                
            if choice.lower() == "cd": #changes user driectory on remote server
                print("Enter name of directory :")
                working_dir = input()
                print(working_dir)
                try:    
                    if sftpconn.isdir(working_dir):#verifies whether the given name is a directory on remote server or not
                        sftpconn.cwd(working_dir)
                    else:
                        print("The name of the directory you entered is incorrect. Please try again")
                except Exception as e:
                    print("An error occured while changing directory:",e)
            
            if choice.lower() == "getfile": #downloads a file from current directory on remote server to current directory on local machine
                
                    print("enter the name of the file with extension from the current directory")
                    filename = input()
                    if sftpconn.isfile(filename):#verifies the given name is a file and exists on the server or not
                        print(f"Downloading file:{filename} from current directory")
                        if getfile(filename,sftpconn):#call the getfile function, passing the filename to perform file download
                            print("Downloaded successfully")
                        else:
                            print("Download failed. \n retrying to download automatically")
                            if getfile(filename):#resumes failed file download 
                               print("Downloaded successfully")
                            else:
                                print("Download failed again.\n Please try again after some time")
                                continue
                    else:
                        print(f"Filename you entered does not exist.\n Please try again")
                        
            if choice.lower() == "seeya": #logout request from the user
                print("Are you sure to logout?(y/n)")
                logout = input()
                if logout == 'y':#logout user
                    sftpconn.close()
                    exit()
                elif logout == 'n':#continue to use the ftpclient
                    continue
            
            if choice.lower() == "getfiles":#downloads multiple files at a  time from the server
                print("enter the file names from the current directory with space")
                
                files = input()

                fileslist = files.split()#files are sliptted by " " and are stored in a list
                
                for i in fileslist:#downloads all the files one by one
                
                    if sftpconn.isfile(i) and sftpconn.exists(i):#verifies whether file exists or not
                        print(f"Downloading file:{i} from current directory")
                        #print(f"Downloading file:{i} from current directory")
                        if getfile(i,sftpconn):#getfile() function downloads the file
                            print("Downloaded successfully")
                        else:
                            print("Download failed.")
                            continue
                    else:
                        print(f"Filename you entered does not exists.\n Please try again")
                    
            if choice.lower() == "listloc": #lists files and folders in location machine on current directory
                print("listingfiles and folders in current directory")
                for paths in os.scandir(os.getcwd()): #grabs and displays all the filename/foldername
                    print(paths.name)
                
            if choice.lower() == "putfile":# uploads a file from local machine to remote server
                print("Enter the filepath on local directory")
                filepath = input()
                if os.path.isdir(filepath): #verifies filepath existance on local machine
                    print("Enter the filename from the mentioned directory")
                    filename = input()
                    if putfile(filepath,filename,sftpconn):#uploads and confirms file upload on remote server
                        print("File uploaded successfully")
                    else:
                        print("File upload failed.")
                        continue
                    
            if choice.lower() == "putfiles":# uploads multiple files to server
                print("enter the file names from the current directory with space")
                files = input()
                filepath = '.'
                filesnames = files.split()#filenames are separated by " " and stored in a list
                putfiles(filepath, filesnames, sftpconn) #verfies whether file was uploaded successfully or not
                print("Files upload complete")
            
            if choice.lower() == "createdir":#creates a folder on remote server
                print("Enter the name of the directory you want to create :")
                newdir = input() 
                if sftpconn.isdir(newdir) and sftpconn.exists(newdir):#rejects directory creation if a folder already exists with the given name
                    print("The directory name you entered already exists. Try again:")
                
                else:
                    print(f"Creating a new directory with name: {newdir}")
                    sftpconn.mkdir(newdir,mode=777)#creates a direcotry with read,write and execute permissions
                    
                    if sftpconn.exists(newdir):# confirms created folder
                        print(f"Created a new directory with name: {newdir} successfully")
                        for info in sftpconn.listdir_attr(remotepath='.'):#displays files and folder information like we see in console for command ls -al
                            print(info)
                    else:
                        print(f"an error occured while craeting {newdir} creating")
                        
            if choice.lower() == "deletefile":#deletes file on remote server
                print("Enter file name to delete from server")
                delfname = input()
                
                if sftpconn.isfile(delfname) and sftpconn.exists(delfname):#verifies the existance given file if existed on remote server
                    print("Deleting the file you entered...")
                    sftpconn.remove(delfname)# deletes the file
                    if sftpconn.exists(delfname):#confirms deleted file
                        print("Deleting file failed. Please try again")
                    else:
                        print("Deleted the file successfully")
                else:
                    print(f"The file name you entered does not exist")
                    
            if choice.lower() == "deletedir":#deletes a directory on remote server, deletes all files and folders inside if it's an non-empty directory
                print("Enter directory name to delete from server")
                deldir = input()
                level=0
                if sftpconn.exists(deldir):#verifies existance of directory on remote server to delete
                    print("Deleting the directory you entered...")
                    for contents in sftpconn.listdir_attr(deldir):#retirves files and folder inside the given directory
                        rempath = posixpath.join(deldir, contents.filename)#posixpath is used join files and filepath to delete the files
                        if S_ISDIR(contents.st_mode):#if a subfolder exists this enters and grabs all the files
                            rmtree(sftpconn, rempath, level=(level + 1))
                        else:
                            rempath = posixpath.join(deldir, contents.filename)#stores all the files in rempath to delete
                            print('removing %s%s' % ('    ' * level, rempath))
                            sftpconn.remove(rempath)#remove funcstion deletes all files in the given directory: this empties the entire directory
                    sftpconn.rmdir(deldir)#finally the directory which is empties is removed
                    if sftpconn.exists(deldir):#confirms directory deletion
                        print("Deleting folder failed. Please try again")
                    else:
                        print("Deleted the directory successfully")
                else:
                    print(f"The directory name you entered does not exist")
                    
            if choice.lower() == "modperm":# file or folder perimissions on remote server are modified. Initially User perimissions, followed by group and others permissions are assigned
                uperm =7
                gperm =7
                operm =7
                
                print("Enter the filename/foldername you want to change permissions")
                
                permfile = input()
                #verifies whether the given filename/foldername exists in the current directory and is a file
                
                if sftpconn.isfile(permfile) or sftpconn.isdir(permfile) and sftpconn.exists(permfile):
                        print("Set user permissions to the file/folder by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")
                        
                        print("Do you want user to have read permissions? y/n")
                        uread = input().lower()
                        if uread == 'y':
                            uperm=4
                        elif uread == 'n':
                            uperm = 0
                        
                        print("Do you want user to have write permissions? y/n")
                        uwrite = input().lower()
                        
                        if uwrite == 'y':
                           uperm = uperm+2
                        elif uwrite == 'n':
                           uperm = uperm+0
                           
                        print("Do you want user to have execute permissions? y/n")
                        uexecute = input().lower()
                        if uexecute == 'y':
                            uperm = uperm+1
                        elif uexecute == 'n':
                            uperm =uperm+0
                        
                        print(f"user permission chmod {permfile} is {uperm}")
                        
                        print("Set group permissions to the file by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")
                        
                        print("Do you want group to have read permissions? y/n")
                        
                        gread=input().lower()
                        if gread == 'y':
                            gperm=4
                        elif gread == 'n':
                            gperm = 0
                        
                        print("Do you want group to have write permissions? y/n")
                        gwrite = input().lower()
                        
                        if gwrite == 'y':
                           gperm = gperm+2
                        elif gwrite == 'n':
                           gperm = gperm+0
                           
                        print("Do you want group to have execute permissions? y/n")
                        gexecute = input().lower()
                        if gexecute == 'y':
                            gperm = gperm+1
                        elif gexecute == 'n':
                            gperm =gperm+0
                            
                            
                        print("Set others permissions to the file by answering the following questions \n NOTE: by default the permissions are set to read,write and execute")
                        
                        print("Do you want others to have read permissions? y/n")
                        oread =input().lower()
                        if oread == 'y':
                            operm=4
                        elif oread == 'n':
                            operm = 0
                        
                        print("Do you want others to have write permissions? y/n")
                        owrite = input().lower()
                        
                        if owrite == 'y':
                           operm = operm+2
                        elif owrite == 'n':
                           operm = operm+0
                           
                        print("Do you want others to have execute permissions? y/n")
                        oexecute = input().lower()
                        if oexecute == 'y':
                            operm = operm+1
                        elif oexecute == 'n':
                            operm =operm+0
                            
                        print("Changing file permissions as per permissions set above...")
                        
                        finalmod = add(str(uperm),str(gperm), str(operm))
                        
                        print(finalmod, type(finalmod))
                        try:
                            sftpconn.chmod(permfile, finalmod)
                            print("Changed file permissions successfully")
                        except IOError as e:
                            print("Error while assigning permissions. Verify if the file/folder still exists on the server")
                            continue
                else:
                    
                    print("file/folder name you enetered does not exist. Please try again")  
                    
            if choice.lower() == 'renremo':# renames remote file
                print("Enter the filename you want to rename on the server")
                renrfname= input() #takes the old filename
                if sftpconn.isfile(renrfname) and sftpconn.exists(renrfname):#verifies existance of file on remote server
                    #renrpath=os.path.abs(renlfname)
                    print("Enter the new name you want for the file")
                    newrenrfname= input()#takes the new filename
                    if sftpconn.isfile(newrenrfname) and sftpconn.exists(newrenrfname):#rejects if a file exists on remote server with newfile name
                        print("the new filename already exists")
                    else:
                        sftpconn.rename(renrfname, newrenrfname)# renames the filename 
                        if sftpconn.isfile(newrenrfname) and sftpconn.exists(newrenrfname):#confirms file rename
                            print("File renamed successfully") 
                        else:
                            print("File rename unsuccessful. Please try again")
                else:
                    print("The filename you entered dooes not exist")       
                    
            if choice.lower() == "renloc":#renames filename on local machine on current directory
                print("Enter the filename you want to rename on the local machine")
                renlfname= input()#takes filename to change
                    #renlpath=os.path.abs(renlfname)
                if os.path.isfile(renlfname) and os.path.exists(renlfname):#verifies existance of filename on local machine
                    print("Enter the new name you want for the file")
                    newrenlfname= input()#takes new filename
                    if os.path.isfile(newrenlfname) and os.path.exists(newrenlfname):#rejects if a file exists on local machine with newfile name
                        print("the new filename already exists")
                    else:
                        os.rename(renlfname, newrenlfname)# renames the filename
                        if os.path.isfile(newrenlfname) and os.path.exists(newrenlfname):#confirms file rename
                            print("File renamed successfully") 
                        else:
                            print("File rename unsuccessful. Please try again")
                else:
                    print("The filename you entered dooes not exist")
                
                
            if choice.lower() == "cpremo":# copies directories on remote server
                print("Enter the directory you want to copy:")
                remotesrc= input()# takes source folder name on remote server
                if sftpconn.isdir(remotesrc):# verifies existance of filename on remote server
                    print("Enter the directory you want copy to:")
                    remotedest= input()# takes destination folder name to copy
                    
                    if sftpconn.exists(remotedest):#rejects the destination name if exists on remote server
                        print(f"the directory you entered already exists.")
                    else:
                        print(f"Copy the directory {remotesrc} to {remotedest}")
                        
                        comm = 'cp -R'+' '+remotesrc + ' ' +remotedest # command is used to copy remote directories
                        try:
                            print(sftpconn.execute(comm))#executes copy command
                        
                        except Exception as e:
                            print(f"There was an erroe while copying directories. {e} \n Please Try again")
                            continue
                else:
                    print("Enter the directory does not exist:")
                    
def savecon(hname,user,passd):#saves new connection information
    while(True):
        if os.path.isfile("savecon.log"):#opens savecon.log file if already exists and writes host,user, and password on it
            savefile = os.path.join(os.getcwd(),"savecon.log")
            save = open(savefile, "a")
            save.write("\nConnection:succesful\n")
            save.write(f"host:{hname}\n")
            save.write(f"username:{user}\n")
            save.write(f"pass:{passd}\n")
            break
        else:
            save=open("savecon.log", "x")#creates savecon.log file for the first time and writes host,user, and password on it
            continue
            
def usesavecon(num):#uses last saved connection credentials to login
    if os.path.exists("savecon.log"):#opens savecon.log file if already exists and grabs host,user, and password from last connection
        savefile = os.path.join(os.getcwd(),"savecon.log")
        save = open(savefile, "r")
        credlines= save.readlines()
        credline=credlines[-num:]
        credi = dict(cred.rstrip("\n").split(':') for cred in credline)
        hname=credi.get("host")
        user=credi.get("username")
        passd=credi.get("pass")
        
        return hname,user,passd # returns saved hostname, username and password
    else: #rejects if no connections were saved previously 
        print("no previous connection information available")
        creds()# continues to execute intial function creds()
        
options = ["Type help to print options", "Type listdir to list files on remote directory", "Type cd to change directory", "Type getfile to download a file", "Type seeya to logout", "Type getfiles to download multiple files", "Type listloc to list local directory" ,"Type putfile to upload a file" ,"Type putfiles to upload multiple files" ,"Type createdir to create a directory on remote server",
            "Type deletefile to delete a file on server", "Type modperm to change file permissions on server", "Type renremo to rename file on server","Type renloc to rename file on local machine", "Type cpremo to copy directories on server",
            "Type deletedir to delete directory from server"]            

def creds():# takes hostname, uername, and password from user and returns them
    print("Enter the ftp server name :")
    hname = input()
    print("Enter your user name :")
    user = input()
    print("Enter your password :")
    passd = getpass.getpass(stream=None)# does not echo the entered password on console
    
    return hname,user,passd #returns hostname, username and password

def ask():#requests user to use saved connection to login or continue to login with new credentials
    if os.path.exists("savecon.log"):
        print("Would you like to use your previously saved login details?(y/n)")
        descision=input()#takes descision
        if descision == 'y':
            response=usesavecon(3)
            print(f"Saved credentials: {response[0]},{response[1]}")
            connect(response[0],response[1],response[2])
        else:
            credos=creds()
            connect(credos[0],credos[1],credos[2])
    else:
        credos=creds()
        connect(credos[0],credos[1],credos[2])
        
def connect(hname,user,passd):#connects to the remote server with given or saved credentials
    try:
        print(f"Connceting to: {hname} with username:{user}")
        sftpconn= pysftp.Connection(host=hname,username=user,password=passd)# connection oject from remote server is stored in sftpconn
        savecon(hname,user,passd)
        #   print("Connection information saved")
        print("Connected successfully", sftpconn)
        #sftp.cwd()
        #FileOptions(sftpconn)
        sftpconn.cwd(f'/u/{user}')
        FileOptions(sftpconn)
        #exit()     
    except Exception as e:
        print("Connection Error. Please connect again.")
        print("\n Exiting....")
        exit()
        
if __name__ == "__main__":
    try:
        ask()
    except Exception as e:
        print(f"Error occured:{e}. Please Try Again")
        exit()