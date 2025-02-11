local F = {}

function F.dectobase(number, base)
    number = tostring(number)
    base = tonumber(base) or 12
    if base < 2 or base ~= math.floor(base) then return nil end
    local sign, integer, fractional = number:match('^([+-]?)(%d+)(%.?%d*)')

    ------------------ INTEGER PART ------------------
    local integers = {}
    integer = tonumber(integer)

    while integer ~= 0 do
        local remainder = integer % base
        if remainder>=10 then remainder = string.char(55+remainder) end
        integer = math.floor(integer/base)
        table.insert(integers, 1, remainder) 
    end
    integers = table.concat(integers)
    ------------------ INTEGER PART ------------------

    ------------------ FRACTIONAL PART ------------------
    local fractionals = {}
    fractional = tonumber(fractional) or 0
    while fractional ~= 0 do
        fractional = fractional * base
        integer = math.floor(fractional)
        fractional = fractional - integer
        if integer>=10 then integer = string.char(55+integer) end
        table.insert(fractionals, integer)
    end
    if integers == '' then integers = '0' end
    fractionals = table.concat(fractionals):gsub('([%d%u]+)','.%1')
    ------------------ FRACTIONAL PART ------------------

    ------------------ REPETITION FIX ------------------
    local precision = 11
    if fractionals:sub(precision+1,precision+1) ~= '' then
        local add_sub = 1
        if F.basetodec(fractionals:sub(precision+1,precision+1), base) < base/2 then
            add_sub = 0
        end
        local x = F.dectobase(F.basetodec(fractionals:sub(2,precision),base)+add_sub, base)
        while #x<precision-1 do x = '0'..x end
        if #x>precision-1 then
            integers = F.basetodec(integers,base)
            integers = F.basetodec(integers+1, base)
            x = x:sub(2)
        end
        -- print(x)
        fractionals = '.'..x
    end
    ------------------ REPETITION FIX ------------------

    return sign..integers..fractionals:gsub('0+$', '')
end

function F.basetodec(number, base)
    base = tonumber(base) or 12
    number = tostring(number)
    if base < 2 or base ~= math.floor(base) then return nil end

    local sign, integer, fractional = number:match('^([+-]?)([%d%u]+)(%.?[%d%u]*)')
    local result = 0

    ------------------ INTEGER PART ------------------
    local result = 0

    for i = 1, #integer do
        local char_ = integer:sub(i,i)
        if string.byte(char_)>=65 then
            char_ = string.byte(char_)-55
        end
        result = result + char_*base^(#integer-i)
    end
    ------------------ INTEGER PART ------------------

    ------------------ FRACTIONAL PART ------------------
    for i = 1, #fractional-1 do
        local char_ = fractional:sub(i+1,i+1)
        if string.byte(char_)>=65 then
            char_ = string.byte(char_)-55
        end
        result = result + char_*base^(-i)
    end
    ------------------ FRACTIONAL PART ------------------

    return tonumber(string.format('%.40f',tonumber(sign..result)))
end

function F.basetobase(number, base_origin, base_goal)

    local result = F.basetodec(number, base_origin)
    result = F.dectobase(result, base_goal)
    return result

end

return F