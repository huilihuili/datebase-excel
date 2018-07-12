import copy


def has_attr(o, fields):
    for field in fields:
        if hasattr(o, field):
            return True
    return False


def create_objects(o, length):
    object_results = []
    for i in range(length):
        object_results.append(copy.copy(o))
    return object_results


def set_object_attr_value(o, attr, value):
    if hasattr(o, attr):
        setattr(o, attr, value)


def set_objects(object_results, fields, values):
    for i, field in enumerate(fields):
        for j, value in enumerate(values):
            set_object_attr_value(object_results[j], field, value[i])


def get_objects_with_fields_and_values(o, fields, values):
    object_results = create_objects(o, len(values))
    set_objects(object_results, fields, values)
    return object_results


def get_object_attrs(objects, *attr):
    result = []
    for o in objects:
        if len(attr) > 1:
            r = []
            for at in attr:
                if hasattr(o, at):
                    r.append(getattr(o, at))
            result.append(r)
        else:
            if hasattr(o, attr[0]):
                result.append(getattr(o, attr[0]))
    return result
