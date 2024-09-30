local que = require "control-me-daddy.que"

local conection = vim.uv.new_tcp()
local command_que = que:new()

local M = {}

local last_processed_time = vim.loop.now()
local timeout_ms = 5000

local function process_que()
    local now = vim.loop.now()
    while command_que.length > 0 do
        local message = command_que:deque()
        if message then
            require("statusline.status_info").set_status_custom(message.status)
            vim.cmd(message.message)
            last_processed_time = now
        end
    end

    -- If the queue is empty and it's been more than 5 seconds since the last message
    if command_que.length == 0 and (now - last_processed_time) >= timeout_ms then
        require("statusline.status_info").set_status_custom("")
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
                    status = string.gsub(string.sub(chunk, 2, 53), "%z", ""),
                    message = string.gsub(string.sub(chunk, 53, 256), "%z", ""),
                }

                command_que:enque(message)
                last_processed_time = vim.loop.now()
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
