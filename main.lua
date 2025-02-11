-- Code by Jefik
-- https://github.com/Jefik37/base-12-calculator

function love.load()
   calc = require('calculations')
   utf8 = require("utf8")

   starting_width = 4320
   starting_height = 7680

   safe_x,safe_y,width,height = love.window.getSafeArea()
   scale_x = width/starting_width
   scale_y = height/starting_height
   scale = math.min(scale_x, scale_y)
   love.keyboard.setKeyRepeat(true)

   local os = love.system.getOS()
   if  os == "Android" or os == "iOS" then mobile = true end

   if mobile then
      love.window.setMode(width, height, {resizable = false})
   else
      love.window.setMode(starting_width/10, starting_height/10, {resizable = true})
   end

   startup = true
   equal_pressed = false
   shift_is_on = false
   hyp_is_on = false
   deg_is_on = false
   
   fontsize = 300
   font = love.graphics.setNewFont('assets/fonts/JetBrainsMono-Regular-Modified.otf', fontsize)

   colors = {
      black = {0,0,0}, white = {1,1,1}, red = {1,0,0,0.3}, blue = {0,0,1}, purple = {1,0,1},
      orange = {0.8,0.3,0}, gray = {0.5,0.5,0.5}, green = {0,1,0}, cyan = {0,1,1},
   }

   texts = {
      history = {
         scale = 0.6,
         color = colors.gray,
         height = 0,
         texts = {
            -- {'9+1', '= A'}, {'6*2', '= 10'}, {'10-3', '= 9'}
         },
      },
      expression = {
         scale = 2,
         color = colors.white,
         height = 0,
         text = '0',
      },
      preview = {
         scale = 1,
         color = colors.gray,
         height = 0,
         text = '',
      }
   } 

   upkeyboardscale = 0.6

-- ❮❯↕±
   buttons = {
      leftpar = {text = '(', color = colors.black, text_color = colors.orange, fontscale = 1},
      rightpar = {text = ')', color = colors.black, text_color = colors.orange, fontscale = 1},
      clear = {text = 'C', color = colors.black, text_color = colors.orange, fontscale = 1},
      backspace = {text = '⌫', color = colors.black, text_color = colors.orange, fontscale = 1},
      nine = {text = '9', color = colors.black, text_color = colors.white, fontscale = 1},
      A = {text = 'A', color = colors.black, text_color = colors.white, fontscale = 1},
      B = {text = 'B', color = colors.black, text_color = colors.white, fontscale = 1},
      multiply = {text = '×', color = colors.black, text_color = colors.orange, fontscale = 1},
      squared = {text = 'x²', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      six = {text = '6', color = colors.black, text_color = colors.white, fontscale = 1},
      seven = {text = '7', color = colors.black, text_color = colors.white, fontscale = 1},
      eight = {text = '8', color = colors.black, text_color = colors.white, fontscale = 1},
      divide = {text = '÷', color = colors.black, text_color = colors.orange, fontscale = 1},
      sqrt = {text = '²√x', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      three = {text = '3', color = colors.black, text_color = colors.white, fontscale = 1},
      four = {text = '4', color = colors.black, text_color = colors.white, fontscale = 1},
      five = {text = '5', color = colors.black, text_color = colors.white, fontscale = 1},
      plus = {text = '+', color = colors.black, text_color = colors.orange, fontscale = 1},
      comma = {text = '.', color = colors.black, text_color = colors.white, fontscale = 1},
      zero = {text = '0', color = colors.black, text_color = colors.white, fontscale = 1},
      one = {text = '1', color = colors.black, text_color = colors.white, fontscale = 1},
      two = {text = '2', color = colors.black, text_color = colors.white, fontscale = 1},
      minus = {text = '-', color = colors.black, text_color = colors.orange, fontscale = 1},
      equals = {text = '=', color = colors.orange, text_color = colors.white, fontscale = 1},
      hyp = {text = 'hyp', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      shift = {text = '2nd', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      sin = {text = 'sin', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      cos = {text = 'cos', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      tan = {text = 'tan', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      rad = {text = 'rad(π)', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      pi = {text = 'π', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      e = {text = 'e', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      abs = {text = '|x|', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      floor = {text = '⌊x⌋', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      log = {text = 'ln', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      plusminus = {text = '+/-', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      inverse = {text = 'x¯¹', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      percentage = {text = '%', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      fact = {text = 'x!', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
      mod = {text = 'mod', color = colors.black, text_color = colors.gray, fontscale = upkeyboardscale},
   }
 
   simple_keyboard = {
      layout = {
         {buttons.abs, buttons.floor, buttons.squared, buttons.sqrt, buttons.log},
         {buttons.e, buttons.pi, buttons.sin, buttons.cos, buttons.tan},
         {buttons.plusminus, buttons.inverse, buttons.mod, buttons.fact, buttons.percentage},
         {buttons.clear, buttons.leftpar, buttons.rightpar, buttons.backspace, buttons.divide},
         {buttons.shift, buttons.nine, buttons.A, buttons.B, buttons.multiply},
         {buttons.hyp, buttons.six, buttons.seven, buttons.eight, buttons.minus},
         {buttons.rad, buttons.three, buttons.four, buttons.five, buttons.plus},
         {buttons.comma, buttons.zero, buttons.one, buttons.two, buttons.equals},
         
      },
      width = starting_width,
   }

   simple_keyboard.height = 600*#simple_keyboard.layout
   simple_keyboard.canvas = love.graphics.newCanvas(simple_keyboard.width, simple_keyboard.height)
   simple_keyboard.hover = love.graphics.newCanvas(simple_keyboard.width, simple_keyboard.height)

   drawcanvas(simple_keyboard)

end

function love.update()

   width = love.graphics.getWidth()
   height = love.graphics.getHeight()

   scale_x = width/starting_width
   scale_y = height/starting_height

   scale = math.min(scale_x, scale_y)

   offset_x = (width - 4320*scale)/2
   offset_y = (height - 7680*scale)/2

   local success, preview_text = pcall(calc.solve, texts.expression.text, deg_is_on)
   if success and preview_text and preview_text ~= texts.expression.text:gsub("%s+", "") then 
      texts.preview.text = '= '..preview_text
   else
      texts.preview.text = ''
   end

end

function love.draw()

   love.graphics.push('all')

   love.graphics.translate(offset_x, height - 7680*scale)

   love.graphics.scale(scale, scale)
   love.graphics.setBlendMode('alpha')
   love.graphics.draw(simple_keyboard.canvas, 0, height/scale_y-simple_keyboard.height)
   love.graphics.setLineWidth(1)
   love.graphics.setColor(colors.gray)
   love.graphics.line(100, height/scale_y-simple_keyboard.height-100,simple_keyboard.width-100,height/scale_y-simple_keyboard.height-100)

   if love.mouse.isDown(1) or #love.touch.getTouches()>0 then checkhover() end

   text_offset = 200
   printtext(texts.preview, 100, text_offset)
   text_offset = text_offset + texts.preview.height
   printtext(texts.expression,100, text_offset)
   text_offset = text_offset + texts.expression.height + 200
   for i = 1, #texts.history.texts do
      printtext(texts.history,100, text_offset, texts.history.texts[i][2])
      text_offset = text_offset + texts.history.height
      printtext(texts.history,100, text_offset, texts.history.texts[i][1])
      text_offset = text_offset + texts.history.height + 200
   end

   love.graphics.pop()
end

function check_shift_hyp(condition)

   if shift_is_on then
      buttons.squared.text = 'xʸ'
      buttons.log.text = 'logᵧx'
      buttons.floor.text = '⌈x⌉'
      buttons.sqrt.text = 'ʸ√x'
      buttons.comma.text = ','
      buttons.squared.text_color = colors.blue
      buttons.log.text_color = colors.blue
      buttons.floor.text_color = colors.blue
      buttons.sqrt.text_color = colors.blue
      buttons.shift.text_color = colors.blue
      buttons.comma.text_color = colors.blue
   else
      buttons.squared.text = 'x²'
      buttons.log.text = 'ln'
      buttons.floor.text = '⌊x⌋'
      buttons.sqrt.text = '²√x'
      buttons.comma.text = '.'
      buttons.squared.text_color = colors.gray
      buttons.log.text_color = colors.gray
      buttons.floor.text_color = colors.gray
      buttons.sqrt.text_color = colors.gray
      buttons.shift.text_color = colors.gray
      buttons.comma.text_color = colors.gray
   end

   if hyp_is_on then 
      buttons.hyp.text_color = colors.green
   else
      buttons.hyp.text_color = colors.gray
   end

   if shift_is_on and not hyp_is_on then
      buttons.sin.text = 'sin¯¹'
      buttons.cos.text = 'cos¯¹'
      buttons.tan.text = 'tan¯¹'
      buttons.sin.text_color = colors.blue
      buttons.cos.text_color = colors.blue
      buttons.tan.text_color = colors.blue
   elseif shift_is_on and hyp_is_on then
      buttons.sin.text = 'sinh¯¹'
      buttons.cos.text = 'cosh¯¹'
      buttons.tan.text = 'tanh¯¹'
      buttons.sin.text_color = colors.cyan
      buttons.cos.text_color = colors.cyan
      buttons.tan.text_color = colors.cyan
   elseif not shift_is_on and hyp_is_on then
      buttons.sin.text = 'sinh'
      buttons.cos.text = 'cosh'
      buttons.tan.text = 'tanh'
      buttons.sin.text_color = colors.green
      buttons.cos.text_color = colors.green
      buttons.tan.text_color = colors.green
   elseif not shift_is_on and not hyp_is_on then
      buttons.sin.text = 'sin'
      buttons.cos.text = 'cos'
      buttons.tan.text = 'tan'
      buttons.sin.text_color = colors.gray
      buttons.cos.text_color = colors.gray
      buttons.tan.text_color = colors.gray
   end

   drawcanvas(simple_keyboard)

end

function check_deg()

   deg_is_on = not deg_is_on

   if deg_is_on then
      buttons.rad.text = 'deg(°)'
      buttons.rad.text_color = colors.purple
   else
      buttons.rad.text = 'rad(π)'
      buttons.rad.text_color = colors.gray
   end
   drawcanvas(simple_keyboard)

end

function love.textinput(t)

   if t =='=' and not equal_pressed then
      equals()

   elseif not t:match("[!=]") then
      texts.expression.text = texts.expression.text .. t
   end
end

function len(str)
   local count = 0
   for _ in str:gmatch("[^\128-\191]") do
       count = count + 1
   end
   return count
end

function printtext(field,offset_x_, offset_y_, text)

   local text = text or field.text
   local scale_ = field.scale
   local width_ = len(text)*fontsize*scale_*(3/5) -- 3:5 is the aspect ratio of the font

   if width_ > simple_keyboard.width-200 then 
      scale_ = (5 * (simple_keyboard.width - 200)) / (3 * len(text) * fontsize)
      width_ = len(text)*fontsize*scale_*(3/5)
   end

   field.height = fontsize*1.3*scale_
   local x_ = simple_keyboard.width - width_-offset_x_
   local y_ = height/scale_y-simple_keyboard.height-field.height-offset_y_

   love.graphics.setColor(field.color)
   -- love.graphics.rectangle('line', x_, y_, width_, field.height) -- text hitbox
   love.graphics.print(text, x_ ,y_,0,scale_)

end 

function checkhover()
   for k, v in pairs(buttons) do
      if collision(v) then
         love.graphics.setColor(colors.red)
         love.graphics.setBlendMode('add', 'alphamultiply')
         love.graphics.rectangle('fill', v.x, v.y, v.width, v.height)
      end
   end
end

function collision(button)

   local mouse_x = (love.mouse.getX()-offset_x)/scale
   local mouse_y = (love.mouse.getY()-(height - 7680*scale))/scale
   if mouse_x > button.x and mouse_x < button.x + button.width and
      mouse_y > button.y and mouse_y < button.y + button.height then
         return true
   end

   return false

end

function equals()
   if texts.preview.text ~= '' then
      equal_pressed = true
      texts.expression.scale = 1
      texts.expression.color = colors.gray
      texts.preview.scale = 2
      texts.preview.color = colors.white
      table.insert(texts.history.texts, 1, {texts.expression.text, texts.preview.text})
   end
end

function check_equal_pressed(txt)

   if startup then
      startup = false
      texts.expression.text = ''
   end

   if equal_pressed and (txt ~= '=' and txt ~= 'return') then
      equal_pressed = false
      texts.expression.scale = 2
      texts.expression.color = colors.white
      texts.expression.text = texts.preview.text:sub(3)
      texts.preview.scale = 1
      texts.preview.color = colors.gray
      texts.preview.text = ''
   end
end

function getkey(tbl, vle)
   for k, v in pairs(tbl) do
       if v == vle then
           return k
       end
   end
   return nil 
end

function backspace()
   local byteoffset = utf8.offset(texts.expression.text, -1)

   if byteoffset then
       texts.expression.text = string.sub(texts.expression.text, 1, byteoffset - 1)
   end
end

function love.mousepressed(x, y, button, istouch, presses)
   for k, v in pairs(buttons) do
      if collision(v) then
         button_key = getkey(buttons, v)
         check_equal_pressed(v.text)
         if button_key == 'equals' then
            if not equal_pressed then equals() end
         elseif button_key ==  'clear' then
            if texts.expression.text == '' then
               texts.history.texts = {}
            else 
               texts.expression.text = ''
            end
         elseif button_key == 'inverse' then
            texts.expression.text = texts.expression.text..'^(-1)'
         elseif button_key == 'backspace' then 
            backspace()
         elseif button_key == 'abs' then
            texts.expression.text = texts.expression.text..'abs'
         elseif v.text == '⌊x⌋' then
            texts.expression.text = texts.expression.text..'floor'
         elseif v.text == '⌈x⌉' then
            texts.expression.text = texts.expression.text..'ceil'
         elseif v.text == '²√x' then
            texts.expression.text = texts.expression.text..'√'
         elseif v.text == 'ʸ√x' then
            texts.expression.text = texts.expression.text..'root'
         elseif v.text == 'x²' then
            texts.expression.text = texts.expression.text..'²'
         elseif v.text == 'xʸ' then
            texts.expression.text = texts.expression.text..'^'
            elseif v.text == 'x!' then
            texts.expression.text = texts.expression.text..'!'
         elseif v.text == 'logᵧx' then
            texts.expression.text = texts.expression.text..'log'
         elseif button_key == 'mod' then
            texts.expression.text = texts.expression.text..'%'
         elseif button_key == 'percentage' then
            texts.expression.text = texts.expression.text..'/100'
         elseif button_key == 'plusminus' then
            texts.expression.text = '-('..texts.expression.text..')'
         elseif button_key == 'shift' then
            shift_is_on = not shift_is_on
            check_shift_hyp()
         elseif button_key == 'hyp' then
            hyp_is_on = not hyp_is_on
            check_shift_hyp()
         elseif button_key == 'rad' then
            check_deg()
         else
            local text_ = v.text

            if text_:match('¯¹') then
               local byteoffset = utf8.offset(text_, -2)

               if byteoffset then
                  text_ = 'a'..string.sub(text_, 1, byteoffset - 1)
               end
            end

            texts.expression.text = texts.expression.text..text_
         end
      end
   end
end

function love.keypressed(key)

   check_equal_pressed(key)
   if key == "backspace" then
      backspace()
   elseif (key == 'return') and not equal_pressed then
      equals()
   elseif key == 'escape' then
      if texts.expression.text == '' then
         texts.history.texts = {}
      else 
         texts.expression.text = ''
      end
   end
end

function drawcanvas(aspect)

   love.graphics.setCanvas(aspect.canvas)

   for i = 1, #simple_keyboard.layout do
      for j = 1, #simple_keyboard.layout[1] do
         linewidth = 50
         love.graphics.setLineWidth(linewidth)
         width_ = aspect.width/#simple_keyboard.layout[1]
         x_ = (j-1)*width_
         height_ = aspect.height/#simple_keyboard.layout
         y_ = (i-1)*height_
         simple_keyboard.layout[i][j].x = x_ +linewidth/2
         simple_keyboard.layout[i][j].y = y_ + height/scale_y-simple_keyboard.height + linewidth/2
         simple_keyboard.layout[i][j].width = width_-linewidth/2 - linewidth/2
         simple_keyboard.layout[i][j].height = height_-linewidth/2 - linewidth/2
         love.graphics.setColor(simple_keyboard.layout[i][j].color)
         love.graphics.rectangle('fill', x_, y_, width_, height_)
         love.graphics.setColor(0,0,0)
         love.graphics.rectangle('line', x_, y_, width_, height_)
         text_x = x_+(width_-1.2*simple_keyboard.layout[i][j].fontscale*fontsize*len(simple_keyboard.layout[i][j].text)/2)/2
         text_y = y_+(height_-simple_keyboard.layout[i][j].fontscale*fontsize*1.4)/2
         love.graphics.setColor(simple_keyboard.layout[i][j].text_color)
         love.graphics.print(simple_keyboard.layout[i][j].text,text_x,text_y,0,simple_keyboard.layout[i][j].fontscale)
      end
   end

   love.graphics.setColor(1,1,1)
   love.graphics.setCanvas()

end