import boto
import boto.ec2
import boto.vpc
import boto.utils
import functools

# global cache of queried data
__cache = {}


def cached(f):
    @functools.wraps(f)
    def with_caching(*args, **kwargs):
        name = f.__name__
        if name in __cache:
            return __cache[name]
        result = f(*args, **kwargs)
        __cache[name] = result
        return result
    return with_caching


def cache():
    return __cache


@cached
def instance_metadata():
    return boto.utils.get_instance_metadata()


def toplevel(name=None):
    im = instance_metadata()
    assert name in im, "Invalid metadata attribute=" + name
    return im[name]


def region():
    return availability_zone()[:-1]


def zone():
    return availability_zone()


def availability_zone():
    return placement()['availability-zone']


def placement():
    return toplevel('placement')


def vpc_id():
    return network_interface()['vpc-id']


@cached
def vpc_tags():
    vpc_conn = boto.vpc.connect_to_region(region())
    vpcs = vpc_conn.get_all_vpcs(vpc_ids=[vpc_id()])
    assert len(vpcs) == 1, \
        'Should have one vpc with id={}, not {}'.format(vpc_id(), vpcs)
    return vpcs[0].tags


def vpc_tag(name):
    return vpc_tags().get(name, None)


def vpc_name():
    return vpc_tag('Name')


def type():
    return toplevel('instance-type')


def id():
    return toplevel('instance-id')


def instance_id():
    return toplevel('instance-id')


@cached
def instance_tags():
    ec2 = boto.ec2.connect_to_region(region())
    instances = ec2.get_only_instances(instance_ids=[instance_id()])
    assert len(instances) == 1, \
        'Should have one instance with id={}, not {}'.format(
            instance_id(), instances)
    return instances[0].tags


def instance_tag(name):
    return instance_tags().get(name, None)


def instance_name():
    return instance_tag('Name')


def public_keys():
    return toplevel('public-keys')


def public_key(name=None):
    keys = public_keys()
    if name in keys:
        return keys[name]

    else:
        assert len(keys.keys()) == 1
        name = keys.keys()[0]
        return keys[name]


def network_interfaces():
    return toplevel('network')['interfaces']['macs']


def network_interface(mac=None):
    macs = network_interfaces()
    if mac in macs:
        return macs[mac]

    else:
        assert len(macs.keys()) == 1
        mac = macs.keys()[0]
        return macs[mac]


def security_groups():
    return network_interface()['security-groups']


def security_group_ids():
    return network_interface()['security-group-ids']
