import oci

compute = [
    oci.core.ComputeClient, 
    oci.core.models.UpdateInstanceDetails, 
    "update_instance"
]

volume = [
    oci.core.BlockstorageClient, 
    oci.core.models.UpdateVolumeDetails, 
    "update_volume"
]

database = [
    oci.database.DatabaseClient,
    oci.database.models.UpdateDatabaseDetails,
    "update_database"
]

db_system = [
    oci.database.DatabaseClient,
    oci.database.models.UpdateDbSystemDetails,
    "update_db_system"
]

def get_resource(resource):
    return eval(resource)
