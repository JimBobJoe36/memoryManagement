# Import statements
import os
import subprocess
import sys
# Install packages
packages = [
    "scikit-learn",
    "psutil",
    "numpy"
]

def installPkg(package):
    '''
    Installs Python packages, based on the value passed into the function

    :param package: the Python package to be installed
    '''
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-qqq", package])

def clear() -> None:
    '''
    Clears the terminal, allowing it to be easily read
    '''
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

try:
    from sklearn.ensemble import IsolationForest
    import psutil
    import numpy
except Exception:
    for pkg in packages:
        installPkg(pkg)
        clear()

    # Import after installed
    from sklearn.ensemble import IsolationForest
    import psutil
    import numpy

# Global Variables
processes = {}
saveDirectoryPath = f"C:\\Users\\{os.getlogin()}\\Desktop"
windowsPrograms = [
    "System Idle Process",
    "",
    "Registry",
    "LockApp.exe",
    "dwm.exe",
    "MsMpEng.exe",
    "explorer.exe",
    "TextInputHost.exe",
    "SearchHost.exe",
    "ShellHost.exe",
    "StartMenuExperienceHost.exe",
    "Widgets.exe",
    "SystemSettings.exe",
    "Microsoft.Management.Services.IntuneWindowsAgent.exe",
    "powershell.exe",
    "OfficeClickToRun.exe",
    "PhoneExperienceHost.exe",
    "msedgewebview2.exe",
    "MemCompression"

]

# Function definitions
def collectData() -> dict:
    '''
    Collects the process name and the memory that the process is taking up
    
    :return processes: The process name and process memory, in Mb
    :rtype processes: dict
    '''
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        info = proc.info
        processID = info["pid"]
        processName = info['name']
        # Memory usage (in Mb)
        processMemory = info['memory_info'].rss / (1024 * 1024)

        # Sets a key-value pair. Example would be "chrome.exe":0.234
        processes[processName] = processMemory

    return processes

def searchForOutliers(data: dict, savePath: str) -> None:
    '''
    Searches for outliers based on memory usage, then reports back to the user
    
    :param data: The data to search for outliers. For this purpose, we will pass in a dictionary with
    the name of process and the total bytes used.
    :type data: dict
    :param savePath: The directory to save the output to
    :type savePath: str
    '''
    # Setup
    global windowsPrograms
    keys = []
    values = []
    for key in data: keys.append(key); values.append(data[key])
    outlierDetector = IsolationForest(contamination=0.2, random_state=42)

    # Get all outliers
    valArray = numpy.array(values)
    valArray = valArray.reshape(-1, 1)
    outlierList = outlierDetector.fit_predict(valArray)

    # Recombine Data
    recombinedData = {}
    for key, out in zip(keys, outlierList):
        recombinedData[key] = int(out)  # 1 for inlier, -1 for outlier
    
    # Log Data, not necessary until the end
    with open(f"{savePath}\\memData.txt", "w") as save:
        for entry in data:
            print(f"{entry}: {data[entry]}")
            save.write(f"{entry}: {data[entry]} \n")
    
    # TODO Change $data to the dict of outliers
    with open(f"{savePath}\\memOutlier.txt", "w") as outs:
        for outlier in recombinedData:
            if (recombinedData[outlier] == -1) and (outlier not in windowsPrograms):
                outs.write(f'{outlier}\n')
    
    
    # Load vectorizer (Maybe? I need to determine how to work with lists, in this case)
    #vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1,8))

# main loop
if __name__ == "__main__":
    processes = collectData()
    for entry in processes:
            print(f"{entry}: {processes[entry]}") 
    searchForOutliers(processes, saveDirectoryPath)
    clear()
    print("[END] Outliers have been found. Results stored on Desktop")