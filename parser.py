from operator import itemgetter, attrgetter, methodcaller
import csv

def parse_tesseract(contents):
    all_lines = determine_information_lines(contents)
    fieldnames = ['description', 'total', 'location']
    csvfile = 'exampletest.csv'
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in all_lines:
        # TODO: Determine which indexes to pull from and if line is invalid and should be skipped
        line_to_write = {
                'description': i[0],
                'total': i[1],
                'location': i[2]
                }
        writer.writerow(line_to_write)


def determine_information_lines(contents):
    # Beware, this current implementation is fairly costly with O(N^2)
    lines = []
    for i in contents:
        home_found = False
        for j in range(len(lines)):
            if is_close_enough(lines[j]['x'], lines[j]['y'], i.x, i.y):
                home_found = True
                lines[j]['contents'] += [i]
        if not home_found:
            lines += [{ 'x': i.x, 'y': i.y, 'contents': [i]}]
    # Now we want to sort given line contents by x coordinates
    to_return = []
    for i in lines:
        line = sorted(i['contents'], key=attrgetter('x'))

# It's so simple it works, but a more intelligent threshold construction that
# adapts to the statistical line distribution in any given document would be better
def is_close_enough(x1, y1, x2, y2):
    THRESHOLD = 4
    if abs(y1 - y2) < THRESHOLD:
        return True
    return False
