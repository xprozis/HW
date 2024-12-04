page_number = 0

def nav_back():
    global page_number
    if page_number > 0:
        page_number+=-1

def nav_foward():
    global page_number
    if page_number < 3:
        page_number+=1