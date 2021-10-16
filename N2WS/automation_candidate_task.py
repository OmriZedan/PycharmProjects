from enum import Enum
from typing import Union, List
import re


class AwsObjType(Enum):
    AWS_OBJ = "generic AWS object"
    AWS_INSTANCE = "instance"
    AWS_VOLUME = "volume"
    AWS_SNAPSHOT = "snapshot"


class AwsInstanceType(Enum):
    MICRO = "micro"
    LARGE = "large1"
    XLARGE = "xlarge3"


class AwsInstanceState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"


class AwsVolumeState(Enum):
    IN_USE = "in-use"
    AVAILABLE = "available"


# ================================================= HELPER CLASSES =================================================== #
class AWSObj:
    """
    Generic AWS object class.
    """

    def __init__(self, obj_id: int = None, obj_name: str = None,
                 obj_type: AwsObjType = AwsObjType.AWS_OBJ,
                 instance_type: AwsInstanceType = None,
                 instance_state: AwsInstanceState = None,
                 volume_state: AwsVolumeState = None,
                 region: str = None,
                 attached_instance_id: int = None,
                 source_volume_id: int = None):
        """
        Generic AWS object constructor
        :param obj_id: unique identifier of AWS object.
        :param obj_name: AWS object name.
        :param obj_type: AWS object type.
        :param instance_type: AWS instance type.
        :param instance_state: AWS instance state.
        :param volume_state: AWS volume state.
        :param region: AWS instance region.
        :param attached_instance_id: AWS instance id that volume belongs to.
        :param source_volume_id: AWS volume id that snapshot was taken from.
        """
        self.obj_id = obj_id
        self.obj_name = obj_name
        self.obj_type = obj_type
        self.instance_type = instance_type
        self.instance_state = instance_state
        self.volume_state = volume_state
        self.region = region
        self.attached_instance_id = attached_instance_id
        self.source_volume_id = source_volume_id

    def __repr__(self):
        """
        String representation of common AWS attribute.
        :return:
        """
        return f"{self.obj_type.value}\tID: {self.obj_id}, NAME: {self.obj_name}, REGION: {self.region} "

    def get_attribute(self, attr: str) -> str:
        """
        Retrieve AWS object attribute
        :param attr: attribute name, i.e state, region, type, etc.
        :return: string representation of the attribute's value
        """
        attr = attr.lower()

        if attr == "id":
            return str(self.obj_id)
        else:
            raise AttributeError(f"Message: Attribute NOT found on object! {self.obj_type.value}:{self.obj_id}"
                                 f" has no attribute {attr}")


class AWSInstance(AWSObj):
    """
    AWS Instance class.
    """

    def __init__(self, **kwargs):
        """
        AWS Instance constructor
        :param kwargs: AWS instance details
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """
        String representation of AWS instance.
        :return: str
        """
        return super().__repr__() + f"INSTANCE TYPE: {self.instance_type.value}, INSTANCE STATE: {self.instance_state.value}"

    def get_attribute(self, attr: str) -> str:
        """
        Retrieve AWS object attribute
        :param attr: attribute name, i.e state, region, type, etc.
        :return: string representation of the attribute's value
        """
        attr = attr.lower()
        if attr == "id":
            return str(self.obj_id)
        elif attr == "name":
            return self.obj_name
        elif attr == "type":
            return str(self.instance_type.value)
        elif attr == "state":
            return str(self.instance_state.value)
        elif attr == "region":
            return self.region
        else:
            super().get_attribute(attr=attr)


class AWSVolume(AWSObj):
    """
    AWS Volume class.
    """

    def __init__(self, **kwargs):
        """
        AWS Volume constructor
        :param kwargs: AWS instance details
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """
        String representation of AWS volume.
        :return: str
        """
        return super().__repr__() + f"VOLUME STATE: {self.volume_state.value}, INSTANCE ID: {self.attached_instance_id}"

    def get_attribute(self, attr: str) -> str:
        """
        Retrieve AWS object attribute
        :param attr: attribute name, i.e state, region, type, etc.
        :return: string representation of the attribute's value
        """
        attr = attr.lower()
        if attr == "id":
            return str(self.obj_id)
        elif attr == "name":
            return self.obj_name
        elif attr == "state":
            return str(self.volume_state.value)
        elif attr == "attached_instance_id":
            return str(self.attached_instance_id)
        elif attr == "region":
            return self.region
        else:
            super().get_attribute(attr=attr)


class AWSSnapshot(AWSObj):
    """
    AWS snapshot class.
    """

    def __init__(self, **kwargs):
        """
        AWS Snapshot constructor
        :param kwargs: AWS instance details
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """
        String representation of AWS snapshot.
        :return: str
        """
        return super().__repr__() + f"VOLUME ID: {self.source_volume_id}"

    def get_attribute(self, attr: str):
        """

        :param attr:
        :return:
        """
        attr = attr.lower()
        if attr == "id":
            return self.obj_id
        elif attr == "name":
            return self.obj_name
        elif attr == "source_volume_id":
            return self.source_volume_id
        elif attr == "region":
            return self.region
        else:
            super().get_attribute(attr=attr)


# =============================================== \ HELPER CLASSES =================================================== #
# ==================================================================================================================== #
# ================================================= HELPER METHODS =================================================== #

def parse_aws_data(aws_type: Union[str, AwsObjType], data_str: str) -> List[AWSObj]:
    """
    Parse AWS data string and extract certain AWS objects from it.
    :param aws_type: AWS object type to look for.
    :param data_str: data string.
    :return: a list of provided-type AWS objects.
    """

    def _get_instances(_data_str: str) -> List[AWSInstance]:
        """
        Build AWS instances according to provided data string.
        :param _data_str: data string.
        :return: a list of AWS instances.
        """
        match = re.search(r"aws_instance_data\W*\='(.*?)' ", _data_str)
        instances_data_str = match.group(1)
        instances_data_list = instances_data_str.split('%')
        instance_list = []
        for instance_data in instances_data_list:
            if not instance_data:
                continue
            kwargs = dict(
                obj_id=re.search(r"id\:(\d+),", instance_data).group(1),
                obj_type=AwsObjType.AWS_INSTANCE,
                instance_type=AwsInstanceType(re.search(r"type\:(\w*),", instance_data).group(1)),
                instance_state=AwsInstanceState(re.search(r"state\:(\w*),", instance_data).group(1)),
                region=re.search(r"region\:([\w\.]*)", instance_data).group(1),
            )

            instance = AWSInstance(**kwargs)
            instance_list.append(instance)

        return instance_list

    def _get_volumes(_data_str: str) -> List[AWSVolume]:
        """
        Build AWS volumes according to provided data string.
        :param _data_str: data string.
        :return: a list of AWS volumes.
        """
        match = re.search(r"aws_volume_data\W*\='(.*?)' ", _data_str)
        volumes_data_str = match.group(1)
        volumes_data_list = volumes_data_str.split('%')
        volume_list = []
        for volume_data in volumes_data_list:
            if not volume_data:
                continue
            kwargs = dict(
                obj_id=re.search(r"id\:(\d+),", volume_data).group(1),
                obj_type=AwsObjType.AWS_VOLUME,
                obj_name=re.search(r"name\:(\w*),", volume_data).group(1),
                volume_state=AwsVolumeState(re.search(r"state\:([\w-]+),", volume_data).group(1)),
                region=re.search(r"region\:([\w\.]*),", volume_data).group(1),
                attached_instance_id=re.search(r"attached_instance_id\:(\d*)", volume_data).group(1),
            )

            volume = AWSVolume(**kwargs)
            volume_list.append(volume)

        return volume_list

    def _get_snapshots(_data_str: str) -> List[AWSSnapshot]:
        """
        Build AWS snapshots according to provided data string.
        :param _data_str: data string.
        :return: a list of AWS snapshots.
        """
        match = re.search(r"aws_snapshot_data\W*\='(.*?)' ", _data_str)
        snaps_data_str = match.group(1)
        snaps_data_str.strip()
        snaps_data_list = snaps_data_str.split('%')
        snap_list = []
        for snap_data in snaps_data_list:
            if not snap_data:
                continue
            kwargs = dict(
                obj_id=re.search(r"id\:(\d+),", snap_data).group(1),
                obj_type=AwsObjType.AWS_SNAPSHOT,
                obj_name=re.search(r"name\:(\w*),", snap_data).group(1),
                region=re.search(r"region\:([\w\.]*),", snap_data).group(1),
                source_volume_id=re.search(r"source_volume_id\:(\d+)", snap_data).group(1),
            )
            snap = AWSSnapshot(**kwargs)
            snap_list.append(snap)

        return snap_list

    # Prepare the data string for regex search
    data_str = data_str.lower()
    ' '.join(data_str.split())
    data_str += ' '

    # retrieve AWS objects of requested type
    aws_type = aws_type.value if isinstance(aws_type, AwsObjType) else aws_type
    if aws_type == AwsObjType.AWS_INSTANCE.value:
        return _get_instances(_data_str=data_str)

    elif aws_type == AwsObjType.AWS_VOLUME.value:
        return _get_volumes(_data_str=data_str)

    elif aws_type == AwsObjType.AWS_SNAPSHOT.value:
        return _get_snapshots(_data_str=data_str)

    # If the code reached this point, then the requested type was illegal
    raise Exception(f"Message: Invalid type! type {aws_type} is not defined")


def aws_lookup(aws_obj_list: List[AWSObj], property_dict: dict = None) -> List[AWSObj]:
    """
    Retrieve a subset of the provided AWS objects, filtered according to given properties.
    :param aws_obj_list: objects to choose from.
    :param property_dict: criteria for filtering the data. i.e. dict(state=running)
    :return: a list of AWS objects that matches the provided criteria.
    """

    matching_aws_obj_list = aws_obj_list
    for attr, value in property_dict.items():
        matching_aws_obj_list = [aws_obj for aws_obj in matching_aws_obj_list if
                                 aws_obj.get_attribute(attr=attr) == value]

    return matching_aws_obj_list


# =============================================== \ HELPER METHODS =================================================== #
# ==================================================================================================================== #
# ================================================  MAIN SCRIPT  ===================================================== #

aws_data_str = "aws_instance_data =" \
               "'id:1100,type:micro,state:running,region:oregon%" \
               "Id:1200,type:large1,state:terminated,region:n.virginia%" \
               "Id:1300,type:xlarge3,state:stopped,region:pasific%" \
               "Id:1400,type:large1,state:running,region:oregon' " \
               "aws_volume_data =" \
               "'id:2100,name:data1,state:available,region:ohio,attached_instance_id:%" \
               "id:2200,name:data1,state:in-use,region:ohio,attached_instance_id:1100%" \
               "id:2300,name:data2,state:available,region:london,attached_instance_id:1200%" \
               "id:2400,name:data2,state:in-use,region:oregon,attached_instance_id:1300' " \
               "aws_snapshot_data =" \
               "'id:3100,name:data1_backup,region:oregon,source_volume_id:2100%" \
               "id:3200,name:data2_backup,region:virginia,source_volume_id:2400%'"

# =============================================== test parse_aws_data ================================================ #
aws_instance_list = parse_aws_data(AwsObjType.AWS_INSTANCE, aws_data_str)
print(*aws_instance_list, '\n', sep='\n')

aws_volume_list = parse_aws_data(AwsObjType.AWS_VOLUME, aws_data_str)
print(*aws_volume_list, '\n', sep='\n')

aws_snap_list = parse_aws_data(AwsObjType.AWS_SNAPSHOT, aws_data_str)
print(*aws_snap_list, '\n', sep='\n')

# =============================================== test aws_lookup ==================================================== #
running_aws_instance_list = aws_lookup(aws_obj_list=aws_instance_list,
                                       property_dict=dict(state="running", region="oregon", type="micro"))

print(*running_aws_instance_list, '\n', sep='\n')

available_aws_volume_list = aws_lookup(aws_obj_list=aws_volume_list,
                                       property_dict=dict(state="available", region="ohio"))

print(*available_aws_volume_list, '\n', sep='\n')

virginia_aws_snap_list = aws_lookup(aws_obj_list=aws_snap_list,
                                    property_dict=dict(region="virginia"))

print(*virginia_aws_snap_list, '\n', sep='\n')
