from .metadata_validator_imagery_historic import MetadataValidatorImageryHistoric
from .metadata_validator_repo import MetadataValidatorRepository
from .metadata_validator_tiff import MetadataValidatorTiff

metadata_validator_repo = MetadataValidatorRepository()
metadata_validator_repo.append(MetadataValidatorTiff())
metadata_validator_repo.append(MetadataValidatorImageryHistoric())
