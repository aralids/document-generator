zb= {"service_points": {"UBJCS ZB alle": "OL",
		        "UBJCS ZB UG2": "OL",
		        "UBJCS ZB EG": "OL",
			"UBJCS ZB OM30": "OL",
		        "UBJCS ZB LS": "LS",
			"UBJCS ZB ZSS Spezial": "LS Spz",
	    	        "UBJCS ZB LS2": "LS2",
			"UBJCS ZB UG2 BZG": "BZG",
		        "UBJCS ZB ZSS BZG": "BZG",
		        "UBJCS ZB OM30 BSKW": "BSKW",
		        "UBJCS ZB EG BSKW": "BSKW",
		        "UBJCS BSKW": "BSKW",
		        "UBJCS BRUW": "BRuW",
			"UBJCS BSP": "BSP",
			"UBJCS BNAT": "BNAT",
			"UBJCS MedHB": "MedHB",
 		        "UBJCS MAR": "OL",
		        "UBJCS RETRO MAR": "OL",
                        "UBJCS MAR ZSS": "OL",
                        "UBJCS ZB Vormerkungen": ""},
	    "layouts": {"UBJCS ZB alle": "layout_1_def",
			"UBJCS ZB UG2": "layout_1_def",
            		"UBJCS ZB EG": "layout_1_def",
			"UBJCS ZB OM30": "layout_1_def",
            		"UBJCS ZB LS": "layout_1_def",
			"UBJCS ZB ZSS Spezial": "layout_1_zss",
			"UBJCS ZB LS2": "layout_1_def",
			"UBJCS ZB UG2 BZG": "layout_1_def",
		        "UBJCS ZB ZSS BZG": "layout_1_zss",
		        "UBJCS ZB OM30 BSKW": "layout_1_def",
		        "UBJCS ZB EG BSKW": "layout_1_def",
		        "UBJCS BSKW": "layout_1_def",
		        "UBJCS BRUW": "layout_1_def",
			"UBJCS BSP": "layout_1_def",
			"UBJCS BNAT": "layout_1_def",
			"UBJCS MedHB": "layout_1_def",
		        "UBJCS MAR": "layout_1_def",
		        "UBJCS RETRO MAR": "layout_1_ret",
		        "UBJCS MAR ZSS": "layout_1_zss",
		        "UBJCS ZB Vormerkungen": "layout_2"},
    }


use_mapping = zb
#
# Mappings print_group_name:values
# where values are
# service_points: Abholtheken
# layouts: Zettellayout
# "Bereich" on the front page just prints the print_group_name (where "UBJCS" might not be necessary)
# layout_1_def_def : default magazine request layout_1_def
# layout_1_def_zss: like layout_1_def but "zz zzz zzz" in field Buchnummer (itemBarcode)
# layout_1_def_ret: like layout_1_def but with image in the title data area
# layout_2 : layout for Vormerkzettel (requestType hold) - no print groups defined yet
