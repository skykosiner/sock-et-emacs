local uv = vim.loop
local conection = uv.new_tcp()

function START()
    conection:connect("127.0.0.1", 8080, function(err)
        if err then
            conection = nil
            error("it's joever", err)
            return
        end

        uv.read_start(conection, vim.schedule_wrap(function(_, chunk)
            print(chunk)
        end))
    end)
end

function STOP()
    conection = nil
end
