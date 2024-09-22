local que = require "control-me-daddy.que"

local conection = vim.uv.new_tcp()
local command_que = que:new()

local M = {}

local function process_que()
    while command_que.length > 0 do
        local message = command_que:deque()

        if message then
            vim.cmd(message.message)
        end
    end
end

function M.START()
    conection:connect("127.0.0.1", 8080, function(err)
        if err then
            conection:close()
            conection:shutdown()
            error("it's joever", err)
            return
        end

        vim.uv.read_start(conection, vim.schedule_wrap(function(_, chunk)
            if chunk then
                ---@type Message
                local message = {
                    command = string.byte(chunk, 1),
                    message = string.sub(chunk, 2)
                }

                command_que:enque(message)
            end
        end))

        vim.loop.new_timer():start(0, 5000, vim.schedule_wrap(function()
            process_que()
        end))
    end)
end

function M.STOP()
    conection:shutdown()
end

return M
