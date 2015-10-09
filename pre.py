"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()
logger = None

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    
    sinal = 0

    entry = { }
    cooked = [ ]

    for line in raw:
        line = line.rstrip()
#        logger.debug("Looking at line: " + line)
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                base = arrow.get(content, 'MM/DD/YYYY')
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }           
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content + '  - ' + str(base.replace(weeks = +int(content)-1).format('MM/DD/YYYY'))
            if sinal == 0 and base.replace(weeks =+ int(content)) > arrow.get():
                sinal = 1
                entry['current_week'] = 1
        
        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
