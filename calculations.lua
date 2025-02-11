local bc = require('baseconvertion')

local F = {}

for name, value in pairs(math) do
    _G[name] = value
end

function ln(x)
    return log(x)
end

function sin(x)
    if deg_is_on then x = rad(x) end
    return math.sin(x)
end

function cos(x)
    if deg_is_on then x = rad(x) end
    return math.cos(x)
end

function tan(x)
    if deg_is_on then x = rad(x) end
    return math.tan(x)
end

function sinh(x)
    if deg_is_on then x = rad(x) end
    return math.sinh(x)
end

function cosh(x)
    if deg_is_on then x = rad(x) end
    return math.cosh(x)
end

function tanh(x)
    if deg_is_on then x = rad(x) end
    return math.tanh(x)
end

function asin(x)
    if deg_is_on then return deg(math.asin(x)) end
    return math.asin(x)
end

function acos(x)
    if deg_is_on then return deg(math.acos(x)) end
    return math.acos(x)
end

function atan(x)
    if deg_is_on then return deg(math.atan(x)) end
    return math.atan(x)
end

function asinh(x)
    if deg_is_on then return deg(ln(x+sqrt(x^2+1))) end
    return ln(x+sqrt(x^2+1))
end

function acosh(x)
    if deg_is_on then return deg(ln(x+sqrt(x^2-1))) end
    return ln(x+sqrt(x^2-1))
end

function atanh(x)
    if deg_is_on then return deg((1/2)*ln((1+x)/(1-x))) end
    return (1/2)*ln((1+x)/(1-x))
end

function root(x,y)
    return x^(1/y)
end

function F.convertexpressiontodec(numbers, symbols)

    for i = 1, #numbers do
        numbers[i] = bc.basetodec(numbers[i], 12)
    end

    local index = 1
    for i = 1, #symbols do
        if symbols[i] == 'ª' then
            symbols[i] = numbers[index]
            index = index + 1
        end

        if index > #numbers then break end
    end

    return table.concat(symbols,''):gsub('ª','')

end

function fact (n)
    if n <= 0 then
      return 1
    else
      return n * fact(n-1)
    end
  end

function treatexpression(expression)

    for key, value in pairs(replacements) do
        expression = expression:gsub(key, value)
    end
    -- os.execute('clear')
    expression = expression:gsub('%s+', '')                     -- 3(11)+3!*(5^2)!sinπ-2acosh(1)cos(2π)3|10|
    expression = expression:gsub('([%d%.%u]+)(!)', 'fact(%1)')         -- 3(11)+fact(3)*(5^2)!sinπ-2acosh(1)cos(2π)3|10|
    expression = expression:gsub('(%|)([^%|]+)(%|)', 'abs(%2)') -- 3(11)+fact(3)*(5^2)!sinπ-2acosh(1)cos(2π)3abs(10)
    expression = expression:gsub('(%([^%(]+%))(!)', 'fact%1')   -- 3(11)+fact(3)*fact(5^2)sinπ-2acosh(1)cos(2π)3abs(10)
    expression = expression:gsub('([%l]+)([%π%d%.%,%u]+)', '%1(%2)')  -- 3(11)+fact(3)*fact(5^2)sin(π)-2acosh(1)cos(2π)3abs(10)
    expression = expression:gsub('(%))([%l%d%.]+)', '%1*%2')      -- 3(11)+fact(3)*fact(5^2)*sin(π)-2acosh(1)*cos(2π)*3abs(10)
    expression = expression:gsub('([%d%.%u]+)([%π%(])', '%1*%2')    -- 3*(11)+fact(3)*fact(5^2)*sin(π)-2acosh(1)*cos(2*π)*3abs(10)
    expression = expression:gsub('([%d%.%u]+)(%l+)', '%1*%2')         -- 3*(11)+fact(3)*fact(5^2)*sin(π)-2*acosh(1)*cos(2*π)*3*abs(10)
    expression = expression:gsub('π', 'pi')
    expression = expression:gsub('[%d%.%u]+', function(x)             -- 3*(B)+fact(3)*fact(5^2)*sin(π)-2*acosh(1)*cos(2*π)*3*abs(A)
        return bc.basetodec(x, 12) end) 
    print(expression)
    return expression
end

function F.solveexpressiondec(expression)

    expression = load('return ' .. expression)
    local result = expression()
    if expression ~= nil and result == result then
        return result
    end
    return nil

end

function F.solve(expression, rad_is_on)
    rad_is_on = rad_is_on or false
    expression = treatexpression(expression)
    expression = F.solveexpressiondec(expression, rad_is_on)
    if expression == nil or result ~= result then return nil
    elseif expression == 'inf' or expression>999999999999999 then return 'inf'
    elseif expression == '-inf' or expression<-999999999999999 then return '-inf' end
    if math.abs(expression)<0.0000000000001 then expression = 0 end
    expression = bc.dectobase(string.format('%.40f',(tostring(expression))), 12)
    expression = expression:gsub('%.$','')
    return expression
end

e = 2.7182818284590452353602874713527
lne = ln(e)

replacements = {
    ['²'] = '^2',
    ['³'] = '^3',
    ['÷'] = '/',
    ['×'] = '*',
    ['√'] = 'sqrt',

}

return F