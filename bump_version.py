import os 
import sys

"""
Util for quickly bumping version of all packages in current directory
"""

def check_version_format(version:str):
    """
    returns true if version is in form of x.y.z, false otherwise

    args: 
        version: string in form of x.y.z
    """
    version = version.split(".")
    if len(version) != 3:
        return False
    for i in version:
        if not i.isnumeric():
            return False
    return True

def compare_versions(v1:str, v2:str):
    """
    Returns true if v2 is greater than v1, false otherwise

    Args: 
        v1 str: in form of x.y.z
        v2 str: in form of i.j.k
    """
    v1 = v1.split(".")
    v2 = v2.split(".")
    for i in range(len(v1)):
        if int(v2[i]) > int(v1[i]):
            return True
        elif int(v2[i]) < int(v1[i]):
            return False
    return False    

def bump_version(new_version: str):
    """Bumps version of all packages in current directory

    Args:
        new_version str: in form of x.y.z

    Raises:
        Exception: if new version is not greater than current version
    """
    for path in os.listdir(path="./"):
        if not os.path.isdir(path):
            continue
        if "setup.py" in os.listdir(f"./{path}"):
            with open(f"./{path}/setup.py", "r") as fs:
                lines = fs.readlines()
                for i in range(len(lines)):
                    if lines[i].find("version='") != -1:
                        current_version = lines[i].split("'")[1]
                        
                        if not compare_versions(current_version, new_version):
                            raise Exception(f"New version is not greater than current version, packge ./{path} not bumped")

                        lines[i] = f"    version='{new_version}',\n"
            
            with open(f"./{path}/setup.py", "w") as fs:
                fs.writelines(lines)
                print(f"Version bumped from {current_version} to {new_version} in {path}/setup.py")


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if not check_version_format(args[1]):
            raise Exception("Version is not in form of x.y.z")
        
        bump_version(args[1])
    else:
        raise Exception("No version given, usage 'python bump_version.py x.y.z'")