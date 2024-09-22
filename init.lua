local conection = vim.uv.new_tcp()

local command_type = {
    [0] = "vim_insert",
    [1] = "vim_after",
    [2] = "vim_command",
    [3] = "system_command",
}

function START()
    conection:connect("127.0.0.1", 8080, function(err)
        if err then
            conection:close()
            conection:shutdown()
            error("it's joever", err)
            return
        end

        vim.uv.read_start(conection, vim.schedule_wrap(function(_, chunk)
            if chunk then
                local type = command_type[string.byte(chunk, 1)]
                local data = string.sub(chunk, 2)
                print(data)
                vim.cmd(data)
            end
        end))
    end)
end

function STOP()
    conection:shutdown()
end
