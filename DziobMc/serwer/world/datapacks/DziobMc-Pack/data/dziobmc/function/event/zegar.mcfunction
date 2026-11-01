# Wywoływany co sekundę. Eventy działają tylko gdy ktoś jest online.
execute unless entity @a run return 0
execute if score #event dz.data matches 1.. run return run function dziobmc:event/trwa
function dziobmc:event/odliczanie
