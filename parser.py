from operator import itemgetter, attrgetter, methodcaller
import csv


def parse_tesseract(contents):
    """
    Takes in the results of pytesseract image_to_boxes and returns a list of transactions
    in a csv format (string)
    Input Type: array from pytesseracts image_to_boxes function
    Output Type: string that is csv compliant
    """
    all_lines = determine_information_lines(contents)
    fieldnames = ['description', 'total', 'location']
    csvfile = 'exampletest.csv'
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in all_lines:
        # TODO: Determine which indexes to pull from and if line is invalid
        # and should be skipped
        line_to_write = {
                'description': i[0],
                'total': i[1],
                'location': i[2]
                }
        writer.writerow(line_to_write)


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
            if is_close_enough(lines[j]['x'], lines[j]['y'], i.x, i.y):
                home_found = True
                lines[j]['contents'] += [i]
        if not home_found:
            lines += [{'x': i.x, 'y': i.y, 'contents': [i]}]
    # Now we want to sort given line contents by x coordinates
    to_return = []
    for i in lines:
        line = sorted(i['contents'], key=attrgetter('x'))


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
