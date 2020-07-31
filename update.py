import oci
import logging
from oci.config import from_file

config = from_file()

# Function to convert namespace.key = value to {"namespace1": {"key1":"value1","Key2":"value2"}}
def extract_tags(tags):
     t = dict()
     for k,v in tags.items():
          temp = k.split(".")
          try:
               t[temp[0]] = {**t[temp[0]], temp[1]: v}
          except KeyError:
               t[temp[0]] = {temp[1]: v}
     return t



def update_compute_tag(instance_id, tags):
     try:
          client = oci.core.ComputeClient(config)
          temp = extract_tags(tags)
          # print(temp)
          update_details = oci.core.models.UpdateInstanceDetails(
               defined_tags = temp
          )
          res = client.update_instance(instance_id, update_details)
          print(res.data)
     except oci.exceptions.ServiceError as e:
          print(e.message)
     
  
