import uuid, subprocess  # nosec
from psutil import pids, Process
from os import path as _p
from sys import exit as exx, path as s_p
from google.colab import output  # pylint: disable=import-error
from IPython import get_ipython  # pylint: disable=import-error
from IPython.display import HTML, clear_output, display  # pylint: disable=import-error

# Ultilities Methods
class MakeButton(object):
    def __init__(self, title, callback):
        self._title = title
        self._callback = callback

    def _repr_html_(self):
        callback_id = "button-" + str(uuid.uuid4())
        output.register_callback(callback_id, self._callback)
        template = """
            <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-info" id="{callback_id}">
                {title}
            </button>
            <script>
                document.querySelector("#{callback_id}").onclick = (e) => {{
                    google.colab.kernel.invokeFunction('{callback_id}', [], {{}})
                    e.preventDefault();
                }};
            </script>
            """
        html = template.format(title=self._title, callback_id=callback_id)
        return html


def generateRandomStr():
    return str(uuid.uuid4()).split("-")[0]


def checkAvailable(path_="", user=False):

    if path_ == "":
        return False
    else:
        return (
            _p.exists(path_)
            if not user
            else _p.exists(f"/usr/local/sessionSettings/{path_}")
        )


def findProcess(process, command="", isPid=False):
    if isinstance(process, int):
        if process in pids():
            return True
    else:
        for pid in pids():
            try:
                p = Process(pid)
                if process in p.name():
                    for arg in p.cmdline():
                        if command in str(arg):
                            return True if not isPid else str(pid)
                        else:
                            pass
                else:
                    pass
            except:  # nosec
                continue


def runSh(args=["echo", "Command", "not", "found"], showOutput=True):
    if isinstance(args, list):
        newArg = args
    elif isinstance(args, str):
        newArg = " ".split(args)
    else:
        print("Wrong argument type.")
        exx()
    try:
        if showOutput:
            return subprocess.check_output(newArg).decode("utf-8")  # nosec
        else:
            return subprocess.run(newArg)  # nosec
    except:
        print(f'Error System Call with "{newArg}"')


def accessSettingFile(path="", setting={}):
    if not isinstance(setting, dict):
        print("Only accept Dictionary object.")
        exx()
    fullPath = f"/usr/local/sessionSettings/{path}"
    try:
        if not len(setting):
            if not checkAvailable(fullPath):
                print(f"File unavailable: {fullPath}.")
                exx()
            with open(fullPath) as jsonObj:
                return json.load(jsonObj)
        else:
            with open(fullPath, "w") as outfile:
                json.dumps(setting, outfile)
    except:
        print(f"Error accessing the file: {fullPath}.")
        exx()


# Prepare prerequisites


def installRclone():
    if checkAvailable("/usr/bin/rclone"):
        return
    else:
        try:
            runSh("curl -s https://rclone.org/install.sh | sudo bash -s beta")
        except:
            print("Error installing rClone.")


def installQBittorren():
    if checkAvailable("/usr/bin/qbittorrent-nox"):
        return
    else:
        try:
            runSh(
                'yes "" | add-apt-repository ppa:qbittorrent-team/qbittorrent-stable \
                    && apt install qbittorrent-nox -qq -y'
            )
        except:
            print("Error installing qBittorrent.")
            exx()


def updateApt():
    if checkAvailable("checkAptUpdate.txt", True):
        return
    else:
        try:
            log = runSh("apt update -qq -y && apt-get install -y iputils-ping")
            accessSettingFile("checkAptUpdate.txt", {"apt-log": log})
        except:
            print("Error update apt.")
            exx()


def installNgrok():
    if checkAvailable("/usr/local/bin/ngrok"):
        return
    else:
        runSh(
            "wget -qq -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip \
                && unzip -qq -n ngrok-stable-linux-amd64.zip && mv ngrok /usr/local/bin/ngrok \
                && rm -f /content/ngrok-stable-linux-amd64.zip",
            False,
        )


def installAutoSSH():
    if checkAvailable("/usr/bin/autossh"):
        return
    else:
        runSh("apt install autossh -qq -y")


def installJDownloader():
    return


def cleanContentDir():
    if not checkAvailable("/content/sample_data"):
        return
    else:
        runSh("rm -rf /content/sample_data", False)


def addSYSPATH():
    if s_p[0] == "/usr/local/sessionSettings":
        return
    s_p.insert(0, "/usr/local/sessionSettings")


def addUltis():
    if checkAvailable("/root/.ipython/rlab_utils"):
        return
    runSh(
        "wget -qq https://geart891.github.io/RLabClone/res/rlab_utils.zip \
            -O /root/.ipython/rlab_utils.zip \
                && unzip -qq -n /root/.ipython/rlab_utils.zip \
                    -d /root/.ipython/rlab_utils \
                        && rm -f /root/.ipython/rlab_utils.zip",
        False,
    )


def checkServer(hostname):
    return True if runSh(f"ping -c 1 {hostname}", False).returncode == 0 else False


def configTimezone(auto=True):
    if checkAvailable("timezone.txt", True):
        return
    if not auto:
        runSh("sudo dpkg-reconfigure tzdata")
    else:
        runSh(
            "sudo ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
                && sudo dpkg-reconfigure -f noninteractive tzdata",
            False,
        )
    timezone = {"timezone": runSh("cat /etc/timezone")[0]}
    accessSettingFile("timezone.txt", timezone)


def uploadRcloneConfig(localUpload=False):
    if not localUpload and checkAvailable("rclone.conf", True):
        return
    elif not localUpload:
        runSh(
            "wget -qq https://geart891.github.io/RLabClone/res/rclonelab/rclone.conf -O /usr/local/sessionSettings/rclone.conf",
            False,
        )
    else:
        try:
            print("Select config file (rclone.conf) from your computer.")
            uploadedFileName = files.upload().keys()
            if len(uploadedFileName) > 1:
                for fn in uploadedFileName:
                    runSh(f'rm -f "/content/{fn}"', False)
                return print("Please only upload a single config file.")
            elif len(uploadedFileName) == 0:
                return print("File upload cancelled.")
            elif checkAvailable(f"/content/{uploadedFileName[0]}"):
                runSh(
                    f'mv -f "/content/{uploadedFileName[0]}" /usr/local/sessionSettings/rclone.conf \
                        && chmod 666 /usr/local/sessionSettings/rclone.conf',
                    False,
                )
            else:
                pass
        except:
            return print("Upload process Error.")


def uploadQBittorrentConfig():
    if checkAvailable("updatedQBSettings.txt", True):
        return
    runSh(
        "mkdir -p -m 755 /{content/qBittorrent,root/{.qBittorrent_temp,.config/qBittorrent}} \
            && wget -qq https://geart891.github.io/RLabClone/res/qbittorrent/qBittorrent.conf \
                -O /root/.config/qBittorrent/qBittorrent.conf",
        False,
    )
    accessSettingFile("updatedQBSettings.txt", {"uploaded": True})


def prepareSession():
    if checkAvailable("ready.start", True):
        return
    else:
        try:
            addSYSPATH()
            addUltis()
            cleanContentDir()
            configTimezone()
            uploadRcloneConfig()
            uploadQBittorrentConfig()
            updateApt()
            accessSettingFile("ready.start", {"prepared": True})
        except:
            print("Error preparing Remote.")
            exx()


# rClone

PATH_RClone_Config = "/usr/local/sessionSettings"
PATH_RClone_Log = "/usr/local/sessionSettings/rclone_log"


def displayOutput(output="None", color="#ce2121"):
    if isinstance(output, list):
        display(
            HTML(
                f"""
                <a style="font-family:monospace;color:#2cff29;font-size:14px;">
                    {'<br>'.join(output[-10:])}
                </a>\
                <center>
                    <h2 style="font-family:Trebuchet MS;color:#00b24c;">
                        ✅ Operation has been successfully completed.
                    </h2>
                    <br>
                </center>
                """
            )
        )
    elif isinstance(output, str):
        display(
            HTML(
                f"""
                <center>\
                    <h2 style="font-family:Trebuchet MS;color:{color};">
                        {output}
                    </h2>
                    <br>
                </center>
                """
            )
        )
    else:
        print("Type errors.")
        exx()


# qBittorrent

tokens = {
    "ddn": "6qGnEsrCL4GqZ7hMfqpyz_7ejAThUCjVnU9gD5pbP5u",
    "tdn": "1Q4i7F6isO7zZRrrjBKZzZhwsMu_74yJqoEs1HrJh1zYyxNo1",
    "mnc": "1QPZGQMEBBI1O3L8G1GtWUiphvF_2d3C6kux93P6p4Zy7SSib",
    "api001": "1Q3zMbZhIunjp92RvrZpnyuJxZL_3V3JUziX5Dp1sQbTMAPrr",
    "api002": "1Q45NXgsx6oyusN3GiNAYvkNJPS_AveYUDBcPHsvRvf21WZv",
    "api003": "1Q6smHt4Bzz9VEXTwj3a7p5Gdx2_5mp6ivT6N6nB3YmRHUEM3",
}


def displayUrl(data, buRemotem, reset):
    clear_output(wait=True)
    print(f'Web UI: {data["url"]} : {data["port"]}')
    if "surl" in data.keys():
        print(f'Web UI (S): {data["surl"]} : {data["port"]}')
    display(MakeButton("Start Backup Remote", buRemotem))
    if "token" in data.keys():
        display(MakeButton("Reset", reset))

