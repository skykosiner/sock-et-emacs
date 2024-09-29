---@alias CommandType number
CommandType = {
    vim_insert = 0,
    vim_after = 1,
    vim_command = 2,
    vim_colos = 3,
    system_command = 4,
    elvis = 5
}

---@class Message
---@field message string
---@field command CommandType

---@class Node
---@field value Message
---@field next Node | nil

---@class que
---@field length number
---@field head Node | nil
---@field tail Node | nil
---@field new fun(self: que): que
---@field enque fun(self: que, item: Message)
---@field deque fun(self: que): Message | nil

local que = {}
que.__index = que

---@return que
function que:new()
    return setmetatable({
        length = 0,
        head = nil,
        tail = nil,
    }, self)
end

---@param self que
---@param item Message
function que:enque(item)
    ---@type Node
    local node = { value = item }

    if self.tail == nil then
        -- The que is empty
        self.head = node
        self.tail = node
    else
        -- Attach the new node to the tail
        self.tail.next = node
        self.tail = node
    end

    self.length = self.length + 1
end

---@param self que
---@return Message | nil
function que:deque()
    if self.head == nil then
        return nil
    end

    self.length = self.length - 1

    local node = self.head
    self.head = self.head.next
    node.next = nil

    if self.length == 0 then
        self.tail = nil
    end

    if node == nil then
        return nil
    end

    return node.value
end

return que
