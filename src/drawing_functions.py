from reportlab.lib.units import cm, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.barcode import code39

from io import BytesIO
import math
from datetime import datetime, timedelta

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from config import use_mapping
from error_handling import check_fields

def create_pdf(data, background_tasks):
    print("data: ", data)
    bfr = BytesIO()
    c = canvas.Canvas(bfr, pagesize=A4, bottomup=0)
    
    # Draw the front page.
    group = data["print_group_name"]
    print("group: ", group)
    service_point = use_mapping["service_points"][group]
    layout = use_mapping["layouts"][group]
    objs = data["data"]
    if not check_fields(layout, objs):
    	print("Please edit your JSON file.\n")
    	return
    
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M")
    draw_front_page(c, " ".join(group.split(" ")[1:]), timestamp)
    c.showPage()
    
    # Sorting.
    # If the JSON file contains 5 objects numbered 0 to 4,
    # these are sorted as 4,2,0 - EMPTY,3,1 on 2 pages.
    page_num = math.ceil(len(objs) / 3)
    for i in range(0, page_num):
    	json_obj1 = objs[i]
    	
    	json_obj2 = None
    	if (i + page_num) <= (len(objs) - 1):
    	    json_obj2 = objs[i+page_num]
    	    
    	json_obj3 = None
    	if (i + 2*page_num) <= (len(objs) - 1):
    	    json_obj3 = objs[i+2*page_num]
    	    
    	draw_3_slip_prints(c, service_point, layout, json_obj1, json_obj2, json_obj3)
    	c.showPage()
    	
    c.save()
    
    background_tasks.add_task(bfr.close)
    pdf = bfr.getvalue()
    return pdf

def draw_front_page(c, bereich, date_time):
    """Defines the width and height of the front page slip prints, 
       the distance between them, and their distance from the page 
       edges. Calls the function for drawing the individual front 
       page slip prints.

       Parameters
       ----------
       bereich : str
           The name of the Bereich of the orders. (?)
           
       date_time : str
           Date and time of creation of the JSON/PDF file.
           Must be in format "DD-MM-YYYY HH:MM".

       Returns
       -------
       void
    """
    margin_left = 1
    margin_top = 1
    dist = 0.45
    width = 18.7
    height = 8.8
    
    draw_front_page_slip_print(c, margin_left, margin_top, width, height, bereich, date_time, "3")
    
    draw_front_page_slip_print(c, margin_left, margin_top + height + dist, width, height, bereich, date_time, "2")
    
    draw_front_page_slip_print(c, margin_left, margin_top + height * 2 + dist * 2, width, height, bereich, date_time, "1")
    	
def draw_front_page_slip_print(c, offsetLeft, offsetTop, width, height, bereich, date_time, number):
    """Draws an individual front page slip print, which features a
       number, the text "UB FFM", the Bereich, and the creation date.

       Parameters
       ----------
       offsetLeft : float
           Distance of the print from the left edge of the page in px.
           
       offsetTop : float
           Distance of the print from the top edge of the page in px.
           
       width : float
           Width of the slip print in px.
       
       height : float
           Height of the slip print in px.
           
       bereich : str
       	   The name of the Bereich of the group.
       
       date_time : str
           Date and time of creation of the JSON/PDF file.
           Must be in format "DD-MM-YYYY HH:MM".
           
       number : int
           Large number on the print, can have value 1-3.

       Returns
       -------
       void
    """

    # UB FFM.
    c.setFont("Times-Roman", 40)
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 4.8)*cm, "UB FFM")
    
    # Bereich.
    c.setFont("Times-Roman", 20)
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 6.2)*cm, "Bereich:")
    c.setFont("Helvetica", 16)
    c.drawString((offsetLeft + 3.1)*cm, (offsetTop + 6.2)*cm, bereich)
    
    # Bestellzetteldruck.
    c.setFont("Times-Roman", 20)
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 7.5)*cm, "Bestellzetteldruck")
    
    # Erstellungsdatum.
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 8.3)*cm, "Erstellungsdatum:")
    c.setFont("Helvetica", 16)
    c.drawString((offsetLeft + 5.9)*cm, (offsetTop + 8.3)*cm, date_time)   
    
    # Large number.
    c.setFont("Times-Roman", 300)
    c.saveState()
    c.translate((offsetLeft + 18.7)*cm, (offsetTop + 4.4)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, number)
    c.restoreState()
    
def draw_3_slip_prints(c, service_point, layout, json_obj1, json_obj2, json_obj3):
    """Defines the width and height of the 3 (or less) slip prints 
       on a page, the distance between them, and their distance 
       from the page edges. Calls the function for drawing individual 
       slip prints.

       Parameters
       ----------
       json_obj1 : dict
           Contains all of the properties for drawing the top slip
           print on the page.
           
       json_obj2 : dict
           Contains all of the properties for drawing the middle slip
           print on the page.
           
       json_obj3 : dict
           Contains all of the properties for drawing the bottom slip
           print on the page.

       Returns
       -------
       void
    """
    margin_left = 1
    margin_top = 1
    dist = 0.45
    slip_print_width = 18.7
    slip_print_height = 8.8
    
    
    if json_obj3 != None:
    	globals()[layout](c, service_point, margin_left, margin_top, slip_print_width, slip_print_height, json_obj3)
    
    if json_obj2 != None:
    	globals()[layout](c, service_point, margin_left, margin_top + slip_print_height + dist, slip_print_width, slip_print_height, json_obj2)
    
    globals()[layout](c, service_point, margin_left, margin_top + slip_print_height * 2 + dist * 2, slip_print_width, slip_print_height, json_obj1) 

def layout_1_def(c, service_point, offsetLeft, offsetTop, width, height, obj):
    """Draws an individual slip print, which features a border,
       8 horizontal lines, 5 vertical lines, 2 rectangles, 11 pieces 
       of horizontal text, 4 pieces of vertical text, 2 (vertical)
       barcodes.

       Parameters
       ----------
       offsetLeft : float
           Distance of the print from the left edge of the page in px.
           
       offsetTop : float
           Distance of the print from the top edge of the page in px.
           
       width : float
           Width of the slip print in px.
       
       height : float
           Height of the slip print in px.
           
       bereich : str
       	   The name of the Bereich of the group.
       	   
       obj : dict
           Contains all of the properties for drawing the slip print.

       Returns
       -------
       void
    """
    
    # Border.
    c.rect(offsetLeft*cm, offsetTop*cm, width*cm, height*cm)
    
    # Horizontal lines from top to bottom.
    c.line(offsetLeft*cm, (offsetTop + 1.3)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 1.3)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.1)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.1)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.9)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.9)*cm)
    c.line(offsetLeft*cm, (offsetTop + 3.7)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 3.7)*cm)
    c.line(offsetLeft*cm, (offsetTop + 4.5)*cm, (offsetLeft + 15)*cm, (offsetTop + 4.5)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 5.3)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop + 5.3)*cm, (offsetLeft + width)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 7.6)*cm, (offsetLeft + 17)*cm, (offsetTop + 7.6)*cm)
    
    # Vertical lines from left to right.
    c.line((offsetLeft + 2.55)*cm, (offsetTop + 2.1)*cm, (offsetLeft + 2.55)*cm, (offsetTop + 2.9)*cm)
    c.line((offsetLeft + 3.7)*cm, (offsetTop)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 3.7)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop)*cm, (offsetLeft + 15)*cm, (offsetTop + height)*cm)
    c.line((offsetLeft + 15.8)*cm, (offsetTop)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 7.6)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop)*cm, (offsetLeft + 17)*cm, (offsetTop + height)*cm)
    
    # Text, from top to bottom, then from left to right.
    # Requester id:
    person_id = obj["requesterBarcode"]
    c.setFont("Times-Roman", 9)
    c.drawString((offsetLeft + 0.2)*cm, (offsetTop + 0.85)*cm, person_id[:4])
    c.setFont("Times-Roman", 16)
    c.drawString((offsetLeft + 0.95)*cm, (offsetTop + 0.85)*cm, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    
    # Request time:
    req_time_lst = obj["requestDate"].split("T")
    req_date = "-".join(req_time_lst[0].split("-")[::-1])
    req_hour = ":".join(req_time_lst[1].split(":")[:2])
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 1.275)*cm, (offsetTop + 2.66)*cm, req_date)
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 3.125)*cm, (offsetTop + 2.66)*cm, req_hour)
    
    # Author name and book title:
    c.setFont("Times-Roman", 12)
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 5.3)*cm, obj["instanceContributorName"])
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 5.9)*cm, obj["instanceTitle"])
    
    # Checkboxes:
    c.rect((offsetLeft + 1.15)*cm, (offsetTop + 6.85)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 1.8)*cm, (offsetTop + 7.15)*cm, "verliehen")
    c.rect((offsetLeft + 7.15)*cm, (offsetTop + 6.85)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 7.8)*cm, (offsetTop + 7.15)*cm, "nicht am Standort")
    
    # Universitätsbibliothek Frankfurt am Main:
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 8.35)*cm, "Universitätsbibliothek Frankfurt am Main")
    
    # Item call number:
    c.setFont("Times-Roman", 16)
    width = stringWidth(obj["itemCallNumber"], "Times-Roman", 16)
    c.drawString(442.425 - width, (offsetTop + 0.85)*cm, obj["itemCallNumber"])
    
    # Item ID:
    item_id = obj["itemBarcode"]
    c.setFont("Helvetica", 16)
    c.saveState()
    c.translate((offsetLeft + 15.6)*cm, (offsetTop + 1.85)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, item_id[:2] + " " + item_id[2:5] + " " + item_id[5:])
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Times-Roman", 12)
    c.saveState()
    c.translate((offsetLeft + 15.55)*cm, (offsetTop + 6.45)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, req_date)
    c.restoreState()
    
    # Pickup service point:
    c.setFont("Helvetica", 16)
    if len(service_point) <= 3:
	    c.saveState()
	    c.translate((offsetLeft + 16.2)*cm, (offsetTop + 8.2)*cm)
	    c.rotate(-90)
	    c.drawCentredString(0, 0, service_point)
	    c.restoreState()
    else:
    	c.drawCentredString((offsetLeft + 16)*cm, (offsetTop + 8.4)*cm, service_point)
    
    # Requester ID vertical:
    c.setFont("Times-Roman", 9)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 8.65)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[:4])
    c.restoreState()
    
    c.setFont("Times-Roman", 16)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 7.95)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    c.restoreState()
    
    # Barcodes.
    # Item barcode:
    item_barcode=code39.Extended39(item_id, barWidth=0.3*mm, barHeight=7*mm, checksum=0)
    c.saveState()
    if len(item_id) == 8:
    	c.translate((offsetLeft + 16.05)*cm, (offsetTop + 6.5)*cm)
    else:
    	c.translate((offsetLeft + 16.05)*cm, (offsetTop + 6.9)*cm)
    c.rotate(-90)
    item_barcode.drawOn(c, 0, 0)
    c.restoreState()
    
    # Requester barcode.
    person_barcode=code39.Extended39(person_id, barWidth=0.2*mm, barHeight=12*mm, checksum=0)
    c.saveState()
    c.translate((offsetLeft + 17.25)*cm, (offsetTop + 5.2)*cm)
    c.rotate(-90)
    person_barcode.drawOn(c, 0, 0)
    c.restoreState()

def layout_1_zss(c, service_point, offsetLeft, offsetTop, width, height, obj):
    
    # Border.
    c.rect(offsetLeft*cm, offsetTop*cm, width*cm, height*cm)
    
    # Horizontal lines from top to bottom.
    c.line(offsetLeft*cm, (offsetTop + 1.3)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 1.3)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.1)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.1)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.9)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.9)*cm)
    c.line(offsetLeft*cm, (offsetTop + 3.7)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 3.7)*cm)
    c.line(offsetLeft*cm, (offsetTop + 4.5)*cm, (offsetLeft + 15)*cm, (offsetTop + 4.5)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 5.3)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop + 5.3)*cm, (offsetLeft + width)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 7.6)*cm, (offsetLeft + 17)*cm, (offsetTop + 7.6)*cm)
    
    # Vertical lines from left to right.
    c.line((offsetLeft + 2.55)*cm, (offsetTop + 2.1)*cm, (offsetLeft + 2.55)*cm, (offsetTop + 2.9)*cm)
    c.line((offsetLeft + 3.7)*cm, (offsetTop)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 3.7)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop)*cm, (offsetLeft + 15)*cm, (offsetTop + height)*cm)
    c.line((offsetLeft + 15.8)*cm, (offsetTop)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 7.6)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop)*cm, (offsetLeft + 17)*cm, (offsetTop + height)*cm)
    
    # Text, from top to bottom, then from left to right.
    # Requester id:
    person_id = obj["requesterBarcode"]
    c.setFont("Times-Roman", 9)
    c.drawString((offsetLeft + 0.2)*cm, (offsetTop + 0.85)*cm, person_id[:4])
    c.setFont("Times-Roman", 16)
    c.drawString((offsetLeft + 0.95)*cm, (offsetTop + 0.85)*cm, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    
    # Request time:
    req_time_lst = obj["requestDate"].split("T")
    req_date = "-".join(req_time_lst[0].split("-")[::-1])
    req_hour = ":".join(req_time_lst[1].split(":")[:2])
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 1.275)*cm, (offsetTop + 2.66)*cm, req_date)
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 3.125)*cm, (offsetTop + 2.66)*cm, req_hour)
    
    # Author name and book title:
    c.setFont("Times-Roman", 12)
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 5.3)*cm, obj["instanceContributorName"])
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 5.9)*cm, obj["instanceTitle"])
    
    # Checkboxes:
    c.rect((offsetLeft + 1.15)*cm, (offsetTop + 6.85)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 1.8)*cm, (offsetTop + 7.15)*cm, "verliehen")
    c.rect((offsetLeft + 7.15)*cm, (offsetTop + 6.85)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 7.8)*cm, (offsetTop + 7.15)*cm, "nicht am Standort")
    
    # Universitätsbibliothek Frankfurt am Main:
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 8.35)*cm, "Universitätsbibliothek Frankfurt am Main")
    
    # Item call number:
    c.setFont("Times-Roman", 16)
    width = stringWidth(obj["itemCallNumber"], "Times-Roman", 16)
    c.drawString(442.425 - width, (offsetTop + 0.85)*cm, obj["itemCallNumber"])
    
    # Item ID:
    item_id = "zzzzzzzz"
    c.setFont("Helvetica", 16)
    c.saveState()
    c.translate((offsetLeft + 15.6)*cm, (offsetTop + 1.85)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, item_id[:2] + " " + item_id[2:5] + " " + item_id[5:])
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Times-Roman", 12)
    c.saveState()
    c.translate((offsetLeft + 15.55)*cm, (offsetTop + 6.45)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, req_date)
    c.restoreState()
    
    # Pickup service point:
    c.setFont("Helvetica", 16)
    if len(service_point) <= 3:
	    c.saveState()
	    c.translate((offsetLeft + 16.2)*cm, (offsetTop + 8.2)*cm)
	    c.rotate(-90)
	    c.drawCentredString(0, 0, service_point)
	    c.restoreState()
    else:
    	c.drawCentredString((offsetLeft + 16)*cm, (offsetTop + 8.4)*cm, service_point)
    
    # Requester ID vertical:
    c.setFont("Times-Roman", 9)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 8.65)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[:4])
    c.restoreState()
    
    c.setFont("Times-Roman", 16)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 7.95)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    c.restoreState()
    
    # Requester barcode.
    person_barcode=code39.Extended39(person_id, barWidth=0.2*mm, barHeight=12*mm, checksum=0)
    c.saveState()
    c.translate((offsetLeft + 17.25)*cm, (offsetTop + 5.2)*cm)
    c.rotate(-90)
    person_barcode.drawOn(c, 0, 0)
    c.restoreState()
    
def layout_1_ret(c, service_point, offsetLeft, offsetTop, width, height, obj):
    
    # Image.
    img_url = "https://resolver.hebis.de/retro/" + obj["itemBarcode"]
    c.saveState()
    c.translate((offsetLeft + 15)*cm, (offsetTop + 1.3)*cm)
    c.scale(1,-1)
    c.drawImage(img_url, 0, 0, width=-11.3*cm, height=-6.3*cm, mask=None)
    c.restoreState()
    
    
    # Border.
    c.rect(offsetLeft*cm, offsetTop*cm, width*cm, height*cm)
    
    # Horizontal lines from top to bottom.
    c.line(offsetLeft*cm, (offsetTop + 1.3)*cm, (offsetLeft + width)*cm, (offsetTop + 1.3)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.1)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.1)*cm)
    c.line(offsetLeft*cm, (offsetTop + 2.9)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 2.9)*cm)
    c.line(offsetLeft*cm, (offsetTop + 3.7)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 3.7)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 3.7)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 3.7)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 5.3)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop + 5.3)*cm, (offsetLeft + width)*cm, (offsetTop + 5.3)*cm)
    c.line((offsetLeft + 3.7)*cm, (offsetTop + 7.6)*cm, (offsetLeft + 17)*cm, (offsetTop + 7.6)*cm)
    
    # Vertical lines from left to right.
    c.line((offsetLeft + 2.55)*cm, (offsetTop + 2.1)*cm, (offsetLeft + 2.55)*cm, (offsetTop + 2.9)*cm)
    c.line((offsetLeft + 3.7)*cm, (offsetTop)*cm, (offsetLeft + 3.7)*cm, (offsetTop + 7.6)*cm)
    c.line((offsetLeft + 15)*cm, (offsetTop + 1.3)*cm, (offsetLeft + 15)*cm, (offsetTop + height)*cm)
    c.line((offsetLeft + 15.8)*cm, (offsetTop + 1.3)*cm, (offsetLeft + 15.8)*cm, (offsetTop + 7.6)*cm)
    c.line((offsetLeft + 17)*cm, (offsetTop + 1.3)*cm, (offsetLeft + 17)*cm, (offsetTop + height)*cm)
    
    # Text, from top to bottom, then from left to right.
    # Requester id:
    person_id = obj["requesterBarcode"]
    c.setFont("Times-Roman", 9)
    c.drawString((offsetLeft + 0.2)*cm, (offsetTop + 0.85)*cm, person_id[:4])
    c.setFont("Times-Roman", 16)
    c.drawString((offsetLeft + 0.95)*cm, (offsetTop + 0.85)*cm, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    
    # Request time:
    req_time_lst = obj["requestDate"].split("T")
    req_date = "-".join(req_time_lst[0].split("-")[::-1])
    req_hour = ":".join(req_time_lst[1].split(":")[:2])
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 1.275)*cm, (offsetTop + 2.66)*cm, req_date)
    c.setFont("Times-Roman", 12)
    c.drawCentredString((offsetLeft + 3.125)*cm, (offsetTop + 2.66)*cm, req_hour)
    
    # Checkboxes:
    c.rect((offsetLeft + 0.1)*cm, (offsetTop + 5)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 0.6)*cm, (offsetTop + 5.3)*cm, "verliehen")
    c.rect((offsetLeft + 0.1)*cm, (offsetTop + 6)*cm, 0.4*cm, 0.4*cm)
    c.drawString((offsetLeft + 0.6)*cm, (offsetTop + 6.3)*cm, "nicht am Standort")
    
    # Universitätsbibliothek Frankfurt am Main:
    c.drawString((offsetLeft + 0.36)*cm, (offsetTop + 8.35)*cm, "Universitätsbibliothek Frankfurt am Main")
    
    # Item call number:
    c.setFont("Times-Roman", 16)
    width = stringWidth(obj["itemCallNumber"], "Times-Roman", 16)
    c.drawString(542.425 - width, (offsetTop + 0.85)*cm, obj["itemCallNumber"])
    
    # Item ID:
    item_id = obj["itemBarcode"]
    c.setFont("Helvetica", 11)
    c.saveState()
    c.translate((offsetLeft + 15.55)*cm, (offsetTop + 2.5)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, item_id[:2] + " " + item_id[2:5] + " " + item_id[5:])
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Times-Roman", 12)
    c.saveState()
    c.translate((offsetLeft + 15.55)*cm, (offsetTop + 6.45)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, req_date)
    c.restoreState()
    
    # Pickup service point:
    c.setFont("Helvetica", 16)
    if len(service_point) <= 3:
	    c.saveState()
	    c.translate((offsetLeft + 16.2)*cm, (offsetTop + 8.2)*cm)
	    c.rotate(-90)
	    c.drawCentredString(0, 0, service_point)
	    c.restoreState()
    else:
    	c.drawCentredString((offsetLeft + 16)*cm, (offsetTop + 8.4)*cm, service_point)
    
    # Requester ID vertical:
    c.setFont("Times-Roman", 9)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 8.65)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[:4])
    c.restoreState()
    
    c.setFont("Times-Roman", 16)
    c.saveState()
    c.translate((offsetLeft + 18.05)*cm, (offsetTop + 7.95)*cm)
    c.rotate(-90)
    c.drawString(0, 0, person_id[4:6] + " " + person_id[6:9] + " " + person_id[9:])
    c.restoreState()
    
    # Requester barcode.
    person_barcode=code39.Extended39(person_id, barWidth=0.2*mm, barHeight=12*mm, checksum=0)
    c.saveState()
    c.translate((offsetLeft + 17.25)*cm, (offsetTop + 5.8)*cm)
    c.rotate(-90)
    person_barcode.drawOn(c, 0, 0)
    c.restoreState()
    
def layout_2(c, service_point, offsetLeft, offsetTop, width, height, obj):
    """Draws an individual slip print, which features a border,
       8 horizontal lines, 5 vertical lines, 2 rectangles, 11 pieces 
       of horizontal text, 4 pieces of vertical text, 2 (vertical)
       barcodes.

       Parameters
       ----------
       offsetLeft : float
           Distance of the print from the left edge of the page in px.
           
       offsetTop : float
           Distance of the print from the top edge of the page in px.
           
       width : float
           Width of the slip print in px.
       
       height : float
           Height of the slip print in px.
           
       bereich : str
       	   The name of the Bereich of the group.
       	   
       obj : dict
           Contains all of the properties for drawing the slip print.

       Returns
       -------
       void
    """
    
    # Border.
    c.setFillColorRGB(0.64, 0.91, 0.33)
    c.setStrokeColorRGB(0.9, 0.9, 0.9)
    c.rect(offsetLeft*cm, offsetTop*cm, width*cm, height*cm, fill=0)
    c.setFillColorRGB(0, 0, 0)
    c.setStrokeColorRGB(0, 0, 0)
    
    # Universitätsbibliothek Frankfurt am Main:
    c.setFont("Helvetica", 14)
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 1.5)*cm, "Universitätsbibliothek Johann Christian Senckenberg")
    c.setFont("Helvetica-Bold", 16)
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 2.1)*cm, "Vormerkung")
    
    c.setFont("Helvetica", 12)
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%Y")
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 3.45)*cm, "Fristzettel vom " + timestamp)
    
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 4.35)*cm, "für")
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 4.85)*cm, obj["requesterBarcode"])
    # c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 5.35)*cm, obj["data"]["requestStatus"])
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 6.75)*cm, "Signatur:")
    c.setFont("Helvetica", 12)
    c.drawString((offsetLeft + 3.5)*cm, (offsetTop + 6.75)*cm, obj["itemCallNumber"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 7.25)*cm, "Titel:")
    c.setFont("Helvetica", 12)
    c.drawString((offsetLeft + 2.7)*cm, (offsetTop + 7.25)*cm, obj["instanceTitle"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString((offsetLeft + 1.5)*cm, (offsetTop + 7.75)*cm, "Buchnr:")
    c.setFont("Helvetica", 12)
    c.drawString((offsetLeft + 3.25)*cm, (offsetTop + 7.75)*cm, obj["itemBarcode"])
    
    # Request date vertical:
    c.setFont("Helvetica-Bold", 17)
    c.saveState()
    c.translate((offsetLeft + 16.1)*cm, (offsetTop + (height / 2))*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, obj["pickupServicePointName"])
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Helvetica-Bold", 17)
    c.saveState()
    c.translate((offsetLeft + 16.8)*cm, (offsetTop + (height / 2))*cm)
    c.rotate(-90)
    week_after = now + timedelta(days=7)
    timestamp1 = week_after.strftime("%d.%m.%Y")
    c.drawCentredString(0, 0, "Abräumen " + timestamp1)
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Helvetica-Bold", 17)
    c.saveState()
    c.translate((offsetLeft + 17.75)*cm, (offsetTop + 6.8)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, obj["requesterBarcode"][:4])
    c.restoreState()
    
    # Request date vertical:
    c.setFont("Helvetica-Bold", 25)
    c.saveState()
    c.translate((offsetLeft + 17.75)*cm, (offsetTop + 3.65)*cm)
    c.rotate(-90)
    c.drawCentredString(0, 0, obj["requesterBarcode"][4:6] + " " + obj["requesterBarcode"][6:9] + " " + obj["requesterBarcode"][9:])
    c.restoreState()
