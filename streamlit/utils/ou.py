from database import get_districts


def get_district_applikator_id(district):
    ids = [d.applikator_id for d in filter(lambda x: x.nexus_name == district, get_districts())]

    if len(ids) > 0:
        return ids
    else:
        return None


def get_district_vitacomm(district):
    districts = [d.vitacomm_district for d in filter(lambda x: x.nexus_name == district, get_districts())]

    if len(districts) > 0:
        return districts
    else:
        return None


def get_district_names():
    return tuple(sorted(set([d.nexus_name for d in get_districts() if d.nexus_name != 'Intet distrikt'])))


def get_nexus_district(district):
    nexus_district = [d.nexus_name for d in filter(lambda x: x.vitacomm_name in district, get_districts())]

    if len(nexus_district) == 1:
        return nexus_district[0]
    else:
        return 'Intet distrikt'
