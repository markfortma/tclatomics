#!/usr/bin/env python3

# This is a function from a much larger project, and it has been stripped down for demonstration purposes.

__author__ = 'Matthew Markfort <matthew.markfort@gmail.com>'
__version__ = '1.0'
__date__ = '2016-05-09'

tclcode = str()

def tclblocks(start=0):
    """
    Recursively evaluate tclcode and create a one-dimension list of the Tcl whereby the contents between '{' and '}'
    are one element and between each Tcl block is also one element
    :param start: (int) the index of the character we process from
    :return: (tuple) [of length 2] where element 0 is the one-dimension list and element 1 is the index
    """
    global tclcode
    bracecount = 0
    buffer = str()
    blocks = list()
    ignore = False
    inquote = 0
    incommand = 0
    dex = start
    sector = len(tclcode)
    while dex < sector:
        if tclcode[dex] == '"':
            inquote += 1
            buffer += tclcode[dex]
        elif tclcode[dex] == '[':
            incommand += 1
            buffer += tclcode[dex]
        elif tclcode[dex] == ']':
            incommand -= 1
            buffer += tclcode[dex]
        elif tclcode[dex] == '#':
            ignore = True
        elif tclcode[dex] == '\n':
            ignore = False
            buffer = buffer.strip()  # Clean off any whitespace fore and aft
            if len(buffer):
                blocks.append(buffer)
            buffer = str()
        elif tclcode[dex] == ';':
            if inquote > 0:
                buffer += tclcode[dex]
            else:
                buffer = buffer.strip()  # Clean off any whitespace fore and aft
                if len(buffer):
                    blocks.append(buffer)
                buffer = str()
        elif tclcode[dex] == '{':
            bracecount += 1
            if incommand != 0:
                buffer += tclcode[dex]
            elif inquote % 2 != 0:
                buffer += tclcode[dex]
            elif bracecount % 2 != 0:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                temp, dex = tclblocks(dex + 1)
                blocks += temp
                buffer = str()
            else:
                buffer = buffer.strip()
                if len(buffer):
                    blocks.append(buffer)
                buffer = str()
        elif tclcode[dex] == '}':
            bracecount -= 1
            if incommand != 0:
                buffer += tclcode[dex]
            elif inquote % 2 != 0:
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
                buffer = str()
        elif not ignore:
            buffer += tclcode[dex]
        dex += 1
    return blocks, dex

if __name__ == '__main__':
    tclcode = '''when HTTP_REQUEST {
    HTTP::redirect "https://[HTTP::host][HTTP::uri]"
}'''
    print(tclblocks())
    # Output: (['when HTTP_REQUEST', 'HTTP::redirect', '"https://[HTTP::host][HTTP::uri]"'], 75)
