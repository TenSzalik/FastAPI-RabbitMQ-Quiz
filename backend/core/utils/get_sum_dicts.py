def get_sum_dicts(data: list) -> dict:
    result_dict = {}

    for item in data:
        for key, value in item.items():
            if key in result_dict:
                result_dict[key] += value
            else:
                result_dict[key] = value

    return result_dict
