import config

commands_list = ['setRoomName', 'setBotPrefix', 'auth', 'editname']

# setRoomName - sets the room name to name. return True on sucess False on failure
def setRoomName(name):
    try:
        config.room_name = name
        print(f"setRoomName({name}): room name set to {name} successfully")
        return True
    except:
        print(f"setRoomName({name}): something went wrong")
        return False

# setBotPrefix - sets the bot prefix for commands. return True on sucess False on failure
def setBotPrefix(prefix):
    try:
        config.bot_prefix = prefix
        print(f"setBotPrefix({prefix}): bot prefix set to {prefix} successfully")
        return True
    except:
        print(f"setBotPrefix({prefix}): something went wrong")
        return False

# setAdmin - set the adminID to the id the authenticator if the token is right
def setAdmin(id, token):
    try:
        id = id.split(":")[1]
        token = token.split(':')[1]
        if token == config.token:
            config.adminID = id
            print(f"setAdmin({id}, {token}): admin ID set to {id} successfully")
            return True
        else:
            return False
    except:
        print(f"setAdmin({id}, {token}): something went wrong")
        return False

# setName - change the name for a specific id
def setName(userID, name):
    try:
        config.name_list[userID] = name
        print(f"setName({userID}, {name}): name set to {name} successfully")
        return True
    except:
        print(f"setName({userID}, {name}): something went wrong")
        return False

# evalCommands - handle bot commands by calling the right functions or not at all
# returns the command after executing it with a prefix of private: public: or None if the command isn't valid.
def evalCommand(command, userID):
    # skips messages that aren't really commands.
    # sorry for wasting tiny bit of memory in the call stack for implementing this tiny part inside the function
    if not command.startswith(config.bot_prefix):
        return None
    command = command.replace(config.bot_prefix, "")
    commandArgs = command.split(" ")  # split for arguments
    if commandArgs[0] not in commands_list:
        return None
    else:
        reply = "private"
        print(f"command: {command} has been called")
        if commandArgs[0] == "setRoomName":
            setRoomName(command.replace(commandArgs[0] + " ", ""))  # gets rid of the first command arg and space
            reply = "public"
        elif commandArgs[0] == "setBotPrefix":
            setBotPrefix(command.replace(commandArgs[0] + " ", "")) # gets rid of the first command arg and space
            reply = "public"
        elif commandArgs[0] == "auth":
            setAdmin(commandArgs[1], commandArgs[2])
            reply = "private"
        elif commandArgs[0] == "editname":
            setName(userID, command.replace(commandArgs[0] + " ", ""))
            reply = "private"

        return reply + ":" + command  #
