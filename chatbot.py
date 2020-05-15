commands_list = ['setRoomName',]
bot_prefix = './'  # change this to whatever suits your needs, everything starting with this will be interpreted as a command

# setRoomName - set's the room name to name
def setRoomName(name):
    try:
        room_name = name
        print(f"setRoomName({name}): room name set to {name} successfully")
        return True
    except:
        print(f"setRoomName({name}): something went wrong")
        return False

# evalCommands: handle bot commands by calling the right functions or not at all
# permissions and shit might be a good idea to be implemented inside here
def evalCommand(command):
    # skips messages that aren't really commands.
    # sorry for wasting tiny bit of memory in the call stack for implementing this tiny part inside the function
    if not command.startswith(bot_prefix):
        return None
    command = command.replace(bot_prefix, "")
    if command not in commands_list:
        return None
    else:
        print(f"command: {command} has been executed")
        return command  # here will be handling of commands
