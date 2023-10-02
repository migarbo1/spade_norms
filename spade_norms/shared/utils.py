def filter_kwargs(name_list, kwargs: dict):
    filtered_kwargs = {}
    if len(name_list) > 0:
        for arg_name in name_list:
            
            if not kwargs.keys().__contains__(arg_name):
                raise Exception(f"Argument with name :{arg_name} not exists in kwargs dict: {kwargs}")
            
            filtered_kwargs[arg_name] = kwargs[arg_name]

    return filtered_kwargs