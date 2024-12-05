def check_fields(layout_name, obj_list):
    if layout_name == "layout_1_def":
        for i in range(0, len(obj_list)):	
            obj = obj_list[i]
            
            # mandatory
            try:
                field = obj["requesterBarcode"]
            except KeyError:
                print("\nThe requesterBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
            
            # not mandatory
            try:
                field = obj["requestDate"]
            except KeyError:
                print("\nThe requestDate field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # mandatory
            try:
                field = obj["instanceContributorName"]
            except KeyError:
                print("\nThe instanceContributorName field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
            
            # mandatory 
            try:
                field = obj["instanceTitle"]
            except KeyError:
                print("\nThe instanceTitle field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # mandatory
            try:
                field = obj["itemCallNumber"]
            except KeyError:
                print("\nThe itemCallNumber field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # mandatory
            try:
                field = obj["itemBarcode"]
            except KeyError:
                print("\nThe itemBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
    elif layout_name == "layout_1_zss":
        for i in range(0, len(obj_list)):	
            obj = obj_list[i]
            
            # mandatory
            try:
                field = obj["requesterBarcode"]
            except KeyError:
                print("\nThe requesterBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # not mandatory
            try:
                field = obj["requestDate"]
            except KeyError:
                print("\nThe requestDate field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # not mandatory
            try:
                field = obj["instanceContributorName"]
            except KeyError:
                print("\nThe instanceContributorName field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # mandatory
            try:
                field = obj["instanceTitle"]
            except KeyError:
                print("\nThe instanceTitle field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # mandatory
            try:
                field = obj["itemCallNumber"]
            except KeyError:
                print("\nThe itemCallNumber field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False

    elif layout_name == "layout_1_ret":
        for i in range(0, len(obj_list)):	
            obj = obj_list[i]
            
            # mandatory
            try:
                field = obj["itemBarcode"]
            except KeyError:
                print("\nThe itemBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
            
            # mandatory
            try:
                field = obj["requesterBarcode"]
            except KeyError:
                print("\nThe requesterBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # not mandatory
            try:
                field = obj["requestDate"]
            except KeyError:
                print("\nThe requestDate field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            # not mandatory
            try:
                field = obj["itemCallNumber"]
            except KeyError:
                print("\nThe itemCallNumber field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False

    elif layout_name == "layout_2":
        for i in range(0, len(obj_list)):	
            obj = obj_list[i]
            
            # mandatory all
            try:
                field = obj["pickupServicePointName"]
            except KeyError:
                print("\nThe pickupServicePointName field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
            
            try:
                field = obj["requesterBarcode"]
            except KeyError:
                print("\nThe requesterBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            try:
                field = obj["itemBarcode"]
            except KeyError:
                print("\nThe itemBarcode field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            try:
                field = obj["itemCallNumber"]
            except KeyError:
                print("\nThe itemCallNumber field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
                
            try:
                field = obj["instanceTitle"]
            except KeyError:
                print("\nThe instanceTitle field does not exist or holds an invalid value for the JSON object at index " + str(i) + ".")
                return False
            
    return True
