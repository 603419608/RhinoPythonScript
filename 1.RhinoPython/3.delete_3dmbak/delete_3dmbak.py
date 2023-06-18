#coding=utf-8
import rhinoscriptsyntax as rs
import os
from System.Threading.Tasks import Task
from System import Array


def delete_3dmbak():
    message = "Select the folder to be cleaned."
    folder = rs.BrowseForFolder(message)
    if not folder: return
    
    tasks = [
        Task.Factory.StartNew(lambda m_path: os.remove(m_path),os.path.join(path, file_name))
        for path,dir_List, file_list in os.walk(folder)
        for file_name in file_list
        if os.path.splitext(file_name)[-1] == ".3dmbak"]
    
    
    if(len(tasks)==0): return
    
    try:
        Task.WaitAll(Array[Task](tasks))
        print("Cleaning completed!")
    except :
        print("error!")
    

if __name__ =="__main__":
    delete_3dmbak()