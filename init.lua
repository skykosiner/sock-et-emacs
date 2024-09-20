local conection = vim.uv.new_tcp()

--- Enum for Command values
---@enum Command
local Command = {
    vim_insert = 0,    --- Insert mode in Vim
    vim_normal = 1,    --- Normal mode in Vim
    system_command = 2 --- System-level command
}

---@class message
---@field public command Command  -- Using the Command enum
---@field public message string   -- A string message
local Message = {}
Message.__index = Message

--- Constructor for Message class
---@param command Command
---@param message string
---@return message
function Message:new(command, message)
    local obj = setmetatable({}, self)
    obj.command = command
    obj.message = message
    return obj
end

function START()
    conection:connect("127.0.0.1", 8080, function(err)
        if err then
            conection:close()
            conection:shutdown()
            error("it's joever", err)
            return
        end

        vim.uv.read_start(conection, vim.schedule_wrap(function(_, chunk)
            local json_data = vim.json.decode(chunk)
            local msg = Message:new(json_data.command, json_data.message)

            if msg.command == Command.vim_insert then
                vim.cmd("silent norm i" .. msg.message)
            elseif msg.command == Command.vim_normal then
                vim.cmd("silent norm " .. msg.message)
            elseif msg.command == Command.system_command then
                vim.cmd("silent !" .. msg.message)
            end
        end))
    end)
end

function STOP()
    conection:shutdown()
end
