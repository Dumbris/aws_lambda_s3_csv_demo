vehicle_type_de = """Aanhangwagen
Autonome aanhangwagen
Bedrijfsauto
Bromfiets
Bus
Driewielig motorrijtuig
Land- of bosb aanhw of getr uitr stuk
Land- of bosbouwtrekker
Middenasaanhangwagen
Mobiele machine
Motorfiets
Motorfiets met zijspan
Motorrijtuig met beperkte snelheid
Oplegger
Personenauto""".splitlines()

vehicle_type_en = """trailer wagon
Autonomous trailers
Bedrijfsauto
bromfiets
bus
Three times motorrijtuig
Land- of bosb aanhw of getr uitr stuk
Land- of bosbouwtrekker
Middenasa trailer
Mobile machine
motor fiets
Motorfiets met zijspan
Motorized gear with covered speed
Oplegger
passenger car""".splitlines()

vehicle_type_trans = dict(zip(vehicle_type_de,vehicle_type_en))