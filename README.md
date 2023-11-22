# Enable-ConcurrentRDP
A script to enable concurrent login sessions on a Windows machine.

![Demo](/img/win11rdp.png)

### About

This script uses the [RDP wrapper](https://github.com/stascorp/rdpwrap) library to allow concurrent login sessions on a Windows Desktop Operating System. This allows a user to be logged in locally while another user can log in remotely over RDP at the same time. RDP Will also be enabled if it had not already been enabled.

### Tested On

| Operating System | Version |
|-|-|
| Windows 11 | 23H2 |
| Windows 10 | 22H2 |

### Generation Script Usage

| Class | Argument | Description |
|-|-|-|
| Output | -o, --outfile | Name of the file to write the payload out to |
| Output | -p, --print | Print the payload to the terminal rather than writing to disk |
| Output | -t, --tee | Print the payload to the terminal AND write to disk |
| Output | -v, --verbose | Print verbose information about the obfuscation being performed |
| Obfuscation | -e, --encode | Encode payload with base64, disabled string obfuscation |
| Obfuscation | -n, --no_output | Remove Write-Host calls from payload |
| Obfuscation | -s, --skip_obf | Skip all obfuscation methods |
| URL | -c, --config | Specify an alternative download URL for the configuration file
| URL | -d, dl_path | Specify an alternative download URL for the ZIP archive containing the rdp wrap installer |

### Notes

The RDP wrap library requires a new configuration for each build iteration of windows. RDP Wrap will not work if it has a configuration file that doesn't have a termsrv patch for the version of Windows that it's running on.

RDP Wrap is likely to be detected as PUA by EDR solutions and defender. It's likely necessary to disable or bypass the EDR for the library to be dropped on the machine without detection from monitoring tools.

The script needs to be executed from an administrator / high integrity level process for the modifications to work. 