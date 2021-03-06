#!/usr/bin/env python3

# This is a function from a much larger project, and it has been stripped down for demonstration purposes.

__author__ = 'Matthew Markfort <matthew.markfort@gmail.com>'
__version__ = '1.0'
__date__ = '2016-05-09'

tclcode = ''

def tclblocks(start=0):
    """
    Recursively evaluate tclcode and create a one-dimension list of the Tcl whereby the contents between '{' and '}'
    are one element and between each Tcl block is also one element
    :param start: (int) the index of the character we process from
    :return: (tuple) [of length 2] where element 0 is the one-dimension list and element 1 is the index
    """
    global tclcode
    bracecount = 0
    buffer = ''
    blocks = []
    ignore = False
    inquote = False
    incommand = 0
    dex = start
    sector = len(tclcode)
    while dex < sector:
        if tclcode[dex] == '"':
            if inquote:
                inquote = False if not buffer.endswith('\\') else True
            else:
                inquote = True
            buffer += tclcode[dex]
        elif tclcode[dex] == '[':
            incommand += 1
            buffer += tclcode[dex]
        elif tclcode[dex] == ']':
            incommand -= 1
            buffer += tclcode[dex]
        elif tclcode[dex] == '#':
            if inquote is False:
                ignore = True
            else:
                buffer += tclcode[dex]
        elif tclcode[dex] == '\n':
            ignore = False if not buffer.endswith('\\') else True
            if ignore is False:
                buffer = buffer.strip()  # Clean off any whitespace fore and aft
                if len(buffer):
                    blocks.append(buffer)
                buffer = ''
        elif tclcode[dex] == ';':
            if inquote:
                buffer += tclcode[dex]
            else:
                buffer = buffer.strip()  # Clean off any whitespace fore and aft
                if len(buffer):
                    blocks.append(buffer)
                buffer = ''
        elif tclcode[dex] == '{':
            bracecount += 1
            if incommand != 0:
                buffer += tclcode[dex]
            elif inquote:
                buffer += tclcode[dex]
            elif bracecount % 2 != 0:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                temp, dex = tclblocks(dex + 1)
                blocks += temp
                buffer = ''
            else:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                buffer = ''
        elif tclcode[dex] == '}':
            bracecount -= 1
            if incommand != 0:
                buffer += tclcode[dex]
            elif inquote:
                buffer += tclcode[dex]
            elif bracecount % 2 == 0:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                return blocks, dex
            else:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                buffer = ''
        elif not ignore:
            buffer += tclcode[dex]
        dex += 1
    return blocks, dex

if __name__ == '__main__':
    tclcode = '''ltm rule /Common/test_html_rule {
when HTTP_REQUEST {
    # This is a multiline \
comment
    set html_response_string "
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error Page</title>
        <style type=\"text/css\">
            #div {
                 text-align: center;
                 text-color: #909090;
            }
        </style>
    <head>
    <body>
        <p>This is just some sample<div id=\"div\">big stuff</div></p>
    </body>
    </html>
    "
    if { [HTTP::uri] contains "php" } {
        HTTP::respond 200 content [subst $html_response_string] ; # This is a inline comment
    }
  }
}
ltm rule /Common/more_sample_rules {
when HTTP_REQUEST {
# This is a simple comment
    set pref_state {#someToken#}
    if { [HTTP::uri] equals "/cacti" } {
        HTTP::redirect "https://[getfield [HTTP::host] ":" 1][HTTP::uri]"
    } #else {
      #    drop
      #}
}
}
ltm virtual /Common/www.sample.com_vs {
    destination 10.10.10.10:80
    ip-protocol tcp
    persist {
        cookie {
            default yes
        }
    }
    profiles {
        http {}
    }
    rules {
        /Common/test_html_rule
    }
    vlans-enabled
    vlans {
        vlan900
    }
}
'''
    res, dex = tclblocks()
    for item in res:
        print(item)
