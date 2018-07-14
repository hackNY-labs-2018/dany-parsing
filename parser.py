from operator import attrgetter
import io
import csv
DEBUG = True


def parse_tesseract(contents):
    """
    Takes in the results of pytesseract image_to_boxes and returns a list of transactions
    in a csv format (string)
    Input Type: array from pytesseracts image_to_boxes function
    Output Type: string that is csv compliant
    """
    all_lines = determine_information_lines(contents)
    fieldnames = ['transaction_date', 'posting_date', 'description', 'location', 'reference_number', 'account_number', 'amount']
    csv_string = io.StringIO()
    writer = csv.DictWriter(csv_string, fieldnames=fieldnames)
    writer.writeheader()
    for i in all_lines:
        # Warning: This step is just a proof of concept and doesn't deliver the
        # right information
        text = i['contents']
        try:
            line_to_write = data_from_raw_line(text)
            writer.writerow(line_to_write)
        except:
            print('You should look into why this failed and remove this print statement eventually')
    raw_csv = csv_string.getvalue()
    csv_string.close()
    return raw_csv

def data_from_raw_line(line):
    """
    Uses the provided array of characters to extract all information we can and
    return that
    Input Type: array of data
    Output Type: json like object to be written
    """
    raw_line = ''
    raw_sections = []
    last_x = 0
    current_section = ''
    count = 0
    for i in line:
        threshold = 40
        if count == 2: # Description and place are very close together
            threshold = 10
        if count >= 4: # now we just have numbers so increase threshold
            threshold = 40
        delta = i['x'] - last_x
        if delta > threshold and not current_section == '':
            raw_line += '  ' # make larger differentiator
            raw_sections += [current_section]
            current_section = ''
        last_x = i['x']
        if delta <= threshold and delta > threshold/2: # Likely a space
            current_section += ' '
            raw_line += ' '
        current_section += i['contents']
        raw_line += i['contents']
    raw_sections += current_section
    '''
    transaction_date = raw_line[0:5]
    posting_date = raw_line[5:10]
    description = raw_line[10]
    location = raw_line[11]
    reference_number = raw_line[12]
    account_number = raw_line[13]
    amount = raw_line[14]
    '''
    transaction_date = raw_sections[0]
    posting_date = raw_sections[1]
    description = raw_sections[2]
    location = raw_sections[3]
    reference_number = raw_sections[4]
    account_number = raw_sections[5]
    amount_start = 6
    try:
        float(location) # If this succeeds the location is accidentally in the description
        account_number = reference_number
        reference_number = location
        location = ''
        amount_start = 5
    except:
        pass
    amount = ''
    for i in raw_sections[amount_start:]: # Conglomerate every remaining value
        amount += i
    if not amount[len(amount)-3] == '.':
        amount = amount[:len(amount)-3] + '.' + amount[len(amount)-2:]

    formatted_line = {
        'transaction_date': transaction_date,
        'posting_date': posting_date,
        'description': description,
        'location': location,
        'reference_number': reference_number,
        'account_number': account_number,
        'amount': amount
    }
    if is_line_accurate(formatted_line):
        return formatted_line
    else:
        return {'description': raw_line} # Provide the info but not nicely put together

def is_line_accurate(formatted_line):
    try:
        int(formatted_line['transaction_date'][:2]) # Date should always begin with two numerals
        return True
    except:
        return False


def determine_information_lines(contents):
    """
    Gets any lines of content that exists in the document. The goal is to then process
    these lines and retreive the transaction ones. The principle is that transaction
    details are linear and therefore by breaking the parsed content by pytesseract
    into line objects, we know any transaction will be in its own line.
    Input Type: array from pytesseracts image_to_boxes function
    Output Type: array containing lists of strings
    """
    # Beware, this current implementation is fairly costly with O(N^2)
    lines = []
    for i in contents:
        home_found = False
        for j in range(len(lines)):
            if is_close_enough(lines[j]['x'], lines[j]['y'], i['x'], i['y']):
                home_found = True
                lines[j]['contents'] += [i]
        if not home_found:
            lines += [{'x': i['x'], 'y': i['y'], 'contents': [i]}]
    # Now we want to sort given line contents by x coordinates
    to_return = []
    for i in lines:
        #line = sorted(i['contents'], key=attrgetter('x'))
        line = i
        to_return += [line]
    return to_return


# It's so simple it works, but a more intelligent threshold construction that
# adapts to the statistical line distribution in any given document would be
# better
def is_close_enough(x1, y1, x2, y2):
    """
    Determines if the x,y coordinates of two lines puts them in the same line of
    a document. The principle is that if the y-offset is small, they are on the
    same line.
    Input Type: floats of coordinates
    Output Type: boolean
    """
    THRESHOLD = 4
    if abs(y1 - y2) < THRESHOLD:
        return True
    return False
