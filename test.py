import main
from utils.hermitids import HermitIDs

for hermitid in HermitIDs:
    main.main(hermitid.value['displayName'])