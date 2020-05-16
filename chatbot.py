import config

commands_list = ['setRoomName', 'setBotPrefix', 'auth', 'editname', 'kick', 'whoadmin']

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
            config.adminID = int(id)
            print(f"setAdmin({id}, {token}): admin ID set to {id} successfully")
            print(f"config.adminID: {config.adminID}")
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

# kickUser - check if the user calling kick is allowed to kick. the kick is done by the server not the bot via special reply string
def kickUser(userID, userToKick):
    try:
        if userID == config.adminID:
            print(f"kickUser({userID}, {userToKick}): kick {userToKick} successfully")
            return True
        else:
            return False
    except:
        print(f"kickUser({userID}, {userToKick}): something went wrong")
        return False

def getAdmin():
    try:
        print(f"getAdmin(): got admin successfully")
        if config.adminID == 0:
            return "Not yet set"
        else:
            print(f"config.name_list[config.adminID]: {config.name_list[config.adminID]}")
            return config.name_list[config.adminID]
    except Exception as e:
        print(f"getAdmin(): something went wrong")
        print(e)
# evalCommands - handle bot commands by calling the right functions or not at all
# returns the command after executing it with a prefix of private: public: fail: or returns None if the command isn't valid.
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
        reply = "fail"
        print(f"command: {command} has been called")
        if commandArgs[0] == "setRoomName":
            if setRoomName(command.replace(commandArgs[0] + " ", "")):  # gets rid of the first command arg and space
                reply = "public"
        elif commandArgs[0] == "setBotPrefix":
            if setBotPrefix(command.replace(commandArgs[0] + " ", "")): # gets rid of the first command arg and space
                reply = "public"
        elif commandArgs[0] == "auth":
            if setAdmin(commandArgs[1], commandArgs[2]):
                reply = "private"
        elif commandArgs[0] == "editname":
            if setName(userID, command.replace(commandArgs[0] + " ", "")):
                reply = "private"
        elif commandArgs[0] == "kick":
            if kickUser(userID, command.replace(commandArgs[0] + " ", "")):
                reply = "kick"+"="+f"{command.replace(commandArgs[0] + ' ', '')}"  # Server does the kicking with this reply
        elif commandArgs[0] == "whoadmin":
            admin = getAdmin()
            if admin:
                return f"public: Admin - {admin}"

        return reply + ":" + command
