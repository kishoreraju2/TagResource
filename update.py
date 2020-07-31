import oci
import logging
from oci.config import from_file
import resources

config = from_file()


# Function to convert namespace.key = value to {"namespace1": {"key1":"value1","Key2":"value2"}}
def extract_tags(tags):
    t = dict()
    for k, v in tags.items():
        temp = k.split(".")
        try:
            t[temp[0]] = {**t[temp[0]], temp[1]: v}
        except KeyError:
            t[temp[0]] = {temp[1]: v}
    return t

COUNT=0
def update_tag(**kwargs):
    try:
        resource_list = resources.get_resource(kwargs["resource_type"])
        client = resource_list[0](config)
        temp = extract_tags(kwargs["tags"])
        update_details = resource_list[1](defined_tags=temp)
        res = eval(
            "client." + resource_list[2] + "(kwargs['resource_id'], update_details)"
        )
        print(res.status)
    except oci.exceptions.ServiceError as e:
        if(e.code == "RelatedResourceNotAuthorizedOrNotFound"):
            print(e.message)
            raise Exception
        else:
            print(e.message)


