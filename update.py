import oci
import logging
from oci.config import from_file
import resources

config = from_file()
IDENTITY_CLIENT = oci.identity.IdentityClient(config)
TAG = dict()



logging.basicConfig(filename="output.log", 
                    format='%(asctime)s %(levelname)s %(message)s ', 
                    filemode='w') 

logger = logging.getLogger()

logger.setLevel(logging.INFO) 
def list_namespace():
    tenancy_id = config["tenancy"]
    return oci.pagination.list_call_get_all_results(
        IDENTITY_CLIENT.list_tag_namespaces, tenancy_id, include_subcompartments=True
    ).data

def list_tag(namespace):
    res = IDENTITY_CLIENT.list_tags(namespace.id).data
    tag_list = list()
    for i in res:
        tag_list.append(i.name)
    TAG[namespace.name] = tag_list



def validate_tag_namespace(namespace, tag_namespace, tag_key):

    if(tag_namespace not in list(TAG.keys())):
        print(tag_namespace + " not there in namespace")
        logger.error(tag_namespace + " not there in namespace")
        raise Exception
        # tag_ids.append(get_id_from_namespace(namespace, tag_namespace))
    if tag_key not in TAG[tag_namespace]:
        print(tag_key + " not in tag key")
        logger.error(tag_key + " not in tag key")
        raise Exception
    

namespaces = list_namespace()
for i in namespaces:
    list_tag(i)
        


# Function to convert namespace.key = value to {"namespace1": {"key1":"value1","Key2":"value2"}}
def extract_tags(tags):
    t = dict()    
    for k, v in tags.items():
        temp = k.split(".")
        validate_tag_namespace(namespaces, temp[0], temp[1])
        try:
            t[temp[0]] = {**t[temp[0]], temp[1]: v}
        except KeyError as e:
            t[temp[0]] = {temp[1]: v}

    return t


COUNT = 0


def update_tag(**kwargs):
    try:
        resource_list = resources.get_resource(kwargs["resource_type"])
        client = resource_list[0](config)
        temp = extract_tags(kwargs["tags"])
        update_details = resource_list[1](defined_tags=temp)
        res = eval(
            "client." + resource_list[2] + "(kwargs['resource_id'], update_details)"
        )
        logger.info("Successfully updated "+ kwargs['resource_id'])
        print(res.status, kwargs['resource_id'])
    except oci.exceptions.ServiceError as e:
        print(e.message)
        logger.error("updating "+ kwargs['resource_id'])
        logger.error(e.message)


# validate_tag_namespace(tags)
