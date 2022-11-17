body_type_de = """MPV
N.v.t.
Niet geregistreerd
aanhangw. Met stijve dissel
achterwaartse kipper
afneembare bovenbouw
afzetbak
ambulance
betonmixer
brandweerwagen
bus
cabriolet
caravan
compressor
containercarrier
coupe
detailhandel/expositiedoel.
dieplader
gecond. met temperatuurreg.
gecond. zndr temperatuurreg.
geconditioneerd voertuig
gepantserd voertuig
gesloten opbouw
hatchback
hoogwerker
huifopbouw
kampeerwagen
keetwagen
kipper
koelwagen
kolkenzuiger
kraanwagen
lijkwagen
limousine
medische hulpwagen
mobiele kraan
neerklapbare zijschotten
niet nader aangeduid
open laadvloer
open wagen
open wagen met vast dak
opleggertrekker
pick-up truck
resteelwagen
sedan
servicewagen
speciale groep
stationwagen
straatvgr,reiniger,rioolzgr
takelwagen
tank v.v. gevaarl. Stoffen
tankwagen
terreinvoertuig
truckstationwagen
v.vervoer zweefvliegtuigen
veewagen
voertuig met haakarm
voor rolstoelen toegankelijk voertuig
voor vervoer boten
voor vervoer voertuigen
vuilniswagen""".splitlines()

body_type_en = """MPV
N/A
Rivet registered
appendix Met stijve dissel
aft tipper
afneembare bovenbouw
afzetbak
outpatient
concrete mixer
fire truck
bus
convertible
caravan
compressor
container carrier
coupe
retail trade/exposited oil.
theplader
cond. with temperature reg.
cond. zndr temperature reg.
conditioneerd voertuig
panted beforehand
slotted opbouw
hatchback
hoogwerker
huifopbouw
camper van
keetwagen
tipper
koelwagen
kolkenzuiger
crane truck
lijkwagen
limousine
medical hulp wagon
mobile crane
foldable zijschotten
not nader aangeduid
open loader
open car
open wagon with vast dak
opleggertrekker
pick up truck
resteel wagon
sedan
service car
special group
station car
straatvgr, cleaner, rioolzgr
trolley
tank v.v. gevaarl fabrics
tank truck
terreinvoertuig
truck station car
v.vervoer zweefvliegentuigen
vehicle
voertuig met haakarm
for rolstoelen toegankelijk voertuig
voor vervoer bots
voor vervoer vortuigen
vehicle""".splitlines()

body_type_trans = dict(zip(body_type_de,body_type_en))