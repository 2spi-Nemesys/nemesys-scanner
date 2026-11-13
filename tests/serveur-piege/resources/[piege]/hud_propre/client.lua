local vitesse = 0
CreateThread(function()
    while true do
        vitesse += 1
        local h = `adder`
        Wait(500)
    end
end)
