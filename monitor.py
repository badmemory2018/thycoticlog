import subprocess 
 
def runThycoticSystem():
    scheduler_order = "nohup python3 ThycoticSystemLog.py 2>&1 &"
    return_info = subprocess.Popen(scheduler_order, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

def runThycoticAudit():
    scheduler_order = "nohup python3 ThycoticAuditLog.py 2>&1 &"
    return_info = subprocess.Popen(scheduler_order, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    
if __name__=="__main__":
    while True:
        systemflag = False
        auditflag = False
        scheduler_order = "ps -ef | grep Thy" 
        return_info = subprocess.Popen(scheduler_order, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) 
        for next_line in return_info.stdout: 
            return_line = next_line.decode("utf-8", "ignore")
            if "ThycoticSystem" in return_line:
                systemflag == True
                print("SystemPY termination found")
            elif "ThycoticAudit" in return_line:
                auditflag == True
                print("AuditPY termination found")
        if systemflag:
            print("System script start to run")
            runThycoticSystem()
        if auditflag:
            print("Audit script start to run")
            runThycoticAudit()
        time.sleep(5)
