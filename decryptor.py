# by Uvajda (Karl Zander) - KryptoMagick 2021

''' Book of Mormon Cryptanalysis Tool version AAC '''

class Record:
    text ={}
    keys = {}
    modulus = 0
    mask = 0
    result = {}
    path = {}

def _file_reader(filename):
    fd = open(filename, "r")
    document = fd.read()
    fd.close()
    return document

def _insert_newlines(document):
    doc_length = len(document)
    new_document = []
    for x in range(doc_length):
        if ord(document[x]) == 20:
            new_document.append(chr(10))
        else:
            new_document.append(document[x])
    return "".join(new_document)

def _remove_empty_lines(document):
    lines = document.split('\n')
    num_lines = len(lines)
    newlines = []
    for x in range(num_lines):
        line = list(lines[x])
        if len(line) != 0:
            newlines.append(line)
    return newlines

def _alphabet_generator(n):
    alphabet = {}
    alphabet_list = []
    for c in range(n):
        x = c % 26
        letter = chr(x  + 65)
        alphabet[x % 26] = letter
        alphabet_list.append(letter)
    return alphabet, alphabet_list

def char_interpreter(char):
    if ((ord(char) >= 65) and (ord(char) >= 90)) or ((ord(char) <= 122) and (ord(char) >= 97)):
        return True
    if (ord(char) == 32):
        return 2
    else:
        return False

def char_converter(char):
    if (ord(char) >= 65 and (ord(char)) <= 90):
        return ord(char) - 65
    elif (ord(char) >= 97 and (ord(char)) <= 122):
        return ord(char) - 97
    elif (ord(char) == 32):
        return 0
    else:
        char_tmp = ord(char) - 32
    return char_tmp

def _code_generator(lines, alphabet, mask):
    num_lines = len(lines)
    msg = []
    space_code0 = []
    space_code1 = []
    line_code = []
    if mask == 23:
        msg0 = []
        msg1 = []
        msg2 = []
        for x in range(num_lines):
            newline = []
            line = list(lines[x])
            line_len = len(line)
            z = 0
            line2_len = len(lines[(x + 1) % num_lines])
            for y in range(line_len):
                tmpA = lines[x][y]
                tmpB = lines[(x + 1) % num_lines][z]
                z = (z + 1) % line2_len
                if char_interpreter(tmpA) and char_interpreter(tmpB):
                    charA = char_converter(tmpA)
                    charB = char_converter(tmpB)
                    numberA = charA
                    numberB = charB
                    output = (numberA + numberB) % 26
                    letter = alphabet[output]
                    newline.append(letter)
                else:
                    ciA = char_interpreter(tmpA)
                    ciB = char_interpreter(tmpB)
                    if (ciA == False) and (ciB == True):
                        space_code0.append(chr(48))
                        space_code1.append(chr(49))
                    elif (ciA == True) and (ciB == False):
                        space_code0.append(chr(49))
                        space_code1.append(chr(48))
            if len(newline) != 0:
                nl = "".join(newline)
                msg0.append(nl)
        
    for x in range(num_lines):
            newline = []
            line = list(lines[x])
            line_len = len(line)
            z = 0
            line2_len = len(lines[(x + 1) % num_lines])
            for y in range(line_len):
                tmpA = lines[x][y]
                tmpB = lines[(x + 1) % num_lines][z]
                z = (z + 1) % line2_len
                if char_interpreter(tmpA) and char_interpreter(tmpB):
                    charA = char_converter(tmpA)
                    charB = char_converter(tmpB)
                    numberA = charA
                    numberB = charB
                    output = (numberA - numberB) % 26
                    letter = alphabet[output]
                    newline.append(letter)
            if len(newline) != 0:
                msg1.append("".join(newline))
    
    for x in range(num_lines):
            newline = []
            line = list(lines[x])
            line_len = len(line)
            z = 0
            line2_len = len(lines[(x + 1) % num_lines])
            for y in range(line_len):
                tmpA = lines[x][y]
                tmpB = lines[(x + 1) % num_lines][z]
                z = (z + 1) % line2_len
                if char_interpreter(tmpA) and char_interpreter(tmpB):
                    charA = char_converter(tmpA)
                    charB = char_converter(tmpB)
                    numberA = charA
                    numberB = charB
                    output = (numberB - numberA) % 26
                    letter = alphabet[output]
                    newline.append(letter)
            if len(newline) != 0:
                msg2.append("".join(newline))
    return "".join(msg0), "".join(msg1), "".join(msg2), "".join(space_code0), "".join(space_code1)

def hash_generator():
    return None

def _double_func_add(alphabet, text):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        output = (number + number) % 26
        letter = alphabet[output]
        msg.append(letter)
    return "".join(msg)

def compound_func():
    ''' BAAAX(H) '''
    return None

def _double_func_sub(alphabet, text):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        for y in range(number):
            alphabet.append(alphabet.pop(0))
        letter = alphabet[number]
        msg.append(letter)
    return "".join(msg)

def _double_func_sub_sub(alphabet, text):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        output = (number - number) % 26
        letter = alphabet[output]
        msg.append(letter)
    return "".join(msg)

def _path_shift(alphabet, text, s=1):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        for y in range(s):
            alphabet.append(alphabet.pop(0))
        letter = alphabet[number]
        msg.append(letter)
    return "".join(msg)

def _left_shift_beta(alphabet, text, s=1):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        for y in range(s):
            alphabet.insert(0, alphabet.pop(25))
        letter = alphabet[number]
        msg.append(letter)
    return "".join(msg)

def _right_shift_beta(alphabet, text, s=1):
    textlen = len(text)
    msg = []
    for x in range(textlen):
        number = ord(text[x]) - 65
        for y in range(s):
            alphabet.insert(0, alphabet.pop(25))
        letter = alphabet[number]
        msg.append(letter)
    return "".join(msg)

def _right_shift_alpha(alphabet, text, s):
    result = []
    textlen = len(text)
    for x in range(textlen):
        number = ord(text[x]) - 65
        output = (number + s) % 26
        letter = alphabet[output]
        result.append(letter)
    return "".join(result)

def _left_shift_alpha(alphabet, text, s):
    result = []
    textlen = len(text)
    for x in range(textlen):
        number = ord(text[x]) - 65
        output = (number - s) % 26
        letter = alphabet[output]
        result.append(letter)
    return "".join(result)

def _betel_shift_alpha(alphabet, keyword):
    result = []
    textlen = len(keyword)
    shift_order = [1, 9, 0, 9, 0]
    shift_order_length = len(shift_order)
    c = 0
    for x in range(textlen):
        number = ord(keyword[x]) - 65
        output = (number + shift_order[c]) % 26
        letter = alphabet[output]
        c = (c + 1) % shift_order_length
        result.append(letter)
    return "".join(result)

def _betel_shift_beta(alphabet, keyword):
    result = []
    textlen = len(keyword)
    shift_order = [0, 0, 9, 0, 0]
    shift_order_length = len(shift_order)
    c = 0
    for x in range(textlen):
        number = ord(keyword[x]) - 65
        output = (number - shift_order[c]) % 26
        letter = alphabet[output]
        c = (c + 1) % shift_order_length
        result.append(letter)
    return "".join(result)

def _betel_shift_gamma(alphabet, keyword):
    result = []
    textlen = len(keyword)
    shift_order = [2, 10, 2, 10, 1]
    shift_order_length = len(shift_order)
    c = 0
    for x in range(textlen):
        number = ord(keyword[x]) - 65
        output = (number - shift_order[c]) % 26
        letter = alphabet[output]
        c = (c + 1) % shift_order_length
        result.append(letter)
    return "".join(result)

def _betel_shift_omega(alphabet, keyword):
    result = []
    textlen = len(keyword)
    shift_order = [0, 10, 0, 10, 0]
    shift_order_length = len(shift_order)
    c = 0
    for x in range(textlen):
        number = ord(keyword[x]) - 65
        output = (number - shift_order[c]) % 26
        letter = alphabet[output]
        c = (c + 1) % shift_order_length
        result.append(letter)
    return "".join(result)

def _line_converter(line, prefix=None):
    n = []
    if prefix != None:
        n.append(prefix)
    for char in line:
        str_char = str(char_converter(char))
        n.append(str_char)
    return int("".join(n))

def _line_multiplier(a, b, m):
    return ((a * b) % m)

def _line_power(a, b, m):
    return pow(a, b, m)

def _line_square(a):
    return (a ** a)

def _line_square_mod(a, m):
    return ((a ** a) % m)

def _number_to_string(n):
    return str(n)

def _line_upon_line(lines, m=68):
    converted_lines = []
    m_lines = []
    p_lines = []
    for line in lines:
        c_line = _line_converter(line)
        converted_lines.append(c_line)
    c_len = len(converted_lines)
    for x in range(c_len):
        a = converted_lines[x]
        b = converted_lines[(x + 1) % c_len]
        c = _line_multiplier(a, b, m)
        m_lines.append(c)
        d = _line_power(a, b, m)
        p_lines.append(d)
    return m_lines, p_lines

def _key_message_B(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = ((ord(msg[x]) - 65) + k[c]) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _key_message_BA(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = ((ord(msg[x]) - 65) - k[c]) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _key_message_BB(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = (k[c] - (ord(msg[x]) - 65)) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _key_message_DA(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = (k[c] + k[c] + (ord(msg[x]) - 65)) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _key_message_DB(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = (k[c] - k[c] - (ord(msg[x]) - 65)) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _key_message_DD(msg, key):
    k = []
    for char in key:
        k.append(ord(char) - 65)
    c = 0
    keyed_message = []
    msg_length = len(msg)
    key_length = len(key)
    for x in range(msg_length):
        output = ((ord(msg[x]) - 65) - k[c] - k[c]) % 26
        keyed_message.append(chr(output + 65))
        c = (c + 1) % key_length
    return "".join(keyed_message)

def _hebew_transformation(alphabet, text, s=1):
    ''' Hebew Transformation '''
    double = _double_func_add(alphabet, text)
    RS = _right_shift_beta(alphabet, double)
    LS = _right_shift_beta(alphabet, RS)
    return double, "".join(RS), "".join(LS)

def _betel_transformation(alphabet, text, s=2):
    ''' Betel Transformation '''
    double = _double_func_add(alphabet, text)
    RS = _right_shift_alpha(alphabet, double, 5)
    LS = _left_shift_alpha(alphabet, RS, 2)
    return double, "".join(RS), "".join(LS)

def _betel_heqet_venus_transformation(alphabet, text, s=2):
    ''' Betel Heqet Venus Transformation '''
    double = _double_func_add(alphabet, text)
    triple = _double_func_add(alphabet, double)
    bsA = _betel_shift_alpha(alphabet, double)
    bsB = _betel_shift_beta(alphabet, bsA)
    bsG = _betel_shift_gamma(alphabet, bsB)
    return double, triple, bsB, bsG

def _U_transformation(alphabet, text, s=2):
    ''' U Transformation '''
    double = _double_func_add(alphabet, text)
    triple = _double_func_add(alphabet, double)
    bsA = _betel_shift_alpha(alphabet, double)
    bsB = _betel_shift_beta(alphabet, bsA)
    return double, triple, bsB, bsA

def guide_func():
    return None

def _run():
    _text_filename = input("Enter input filename: ")
    _output_filename = input("Enter output filename: ")
    _modulus = input("Enter modulus number: ")
    _keyword = input("Enter keyword: ")
    n = int(_modulus)
    m = 23

    record = _file_reader(_text_filename)
    new_document = _insert_newlines(record)
    new_documentS = _remove_empty_lines(new_document)
    alphabet, alphabet_list = _alphabet_generator(n)
    msg0, msg1, msg2, space_code0, space_code1 = _code_generator(new_documentS, alphabet, m)
    out_file = open(_output_filename, "w")
    out_file.write("Book of Mormon Decrypted: Modulo "+_modulus+"\n")
    out_file.write("Keyword: "+_keyword+"\n")
    out_file.write("Prepared by: KryptoMagick (Uvajda)\n\n")
    out_file.write("Space Code0: "+space_code0+"\n")
    out_file.write("Space Code1: "+space_code1+"\n")
    #print("Space Code0: ", space_code0+"\n")
    #print("Space Code1: ", space_code1+"\n")
    out_file.write("phase0: "+msg0+"\n")
    out_file.write("phase1: "+msg1+"\n")
    out_file.write("phase2: "+msg2+"\n")
    
    #print("phase0: ", msg0+"\n")
    #print("phase1 ", msg1+"\n")
    #print("phase2: ", msg2+"\n")

    m_lines, p_lines = _line_upon_line(new_documentS)
    m0_lines, p0_lines = _line_upon_line(msg0)
    m1_lines, p1_lines = _line_upon_line(msg1)
    m2_lines, p2_lines = _line_upon_line(msg2)

    out_file.write("plaintext lines multiplied modulo 68: "+str(m_lines)+"\n")
    out_file.write("plaintext lines raised modulo 68: "+str(p_lines)+"\n")
    out_file.write("msg0 multiplied modulo 68: "+str(m0_lines)+"\n")
    out_file.write("msg0 raised modulo 68: "+str(p0_lines)+"\n")
    out_file.write("msg1 multiplied modulo 68: "+str(m1_lines)+"\n")
    out_file.write("msg1 raised modulo 68: "+str(p1_lines)+"\n")
    out_file.write("msg2 multiplied modulo 68: "+str(m2_lines)+"\n")
    out_file.write("msg2 raised modulo 68: "+str(p2_lines)+"\n")

    keyed_msg0B = _key_message_B(msg0, _keyword)
    keyed_msg0BA = _key_message_BA(msg0, _keyword)
    keyed_msg0BB = _key_message_BB(msg0, _keyword)
    keyed_msg0DA = _key_message_DA(msg0, _keyword)
    keyed_msg0DB = _key_message_DB(msg0, _keyword)
    keyed_msg0DD = _key_message_DD(msg0, _keyword)
    
    keyed_msg1B = _key_message_B(msg1, _keyword)
    keyed_msg1BA = _key_message_BA(msg1, _keyword)
    keyed_msg1BB = _key_message_BB(msg1, _keyword)
    keyed_msg1DA = _key_message_DA(msg1, _keyword)
    keyed_msg1DB = _key_message_DB(msg1, _keyword)
    keyed_msg1DD = _key_message_DD(msg1, _keyword)
    
    keyed_msg2B = _key_message_B(msg2, _keyword)
    keyed_msg2BA = _key_message_BA(msg2, _keyword)
    keyed_msg2BB = _key_message_BB(msg2, _keyword)
    keyed_msg2DA = _key_message_DA(msg2, _keyword)
    keyed_msg2DB = _key_message_DB(msg2, _keyword)
    keyed_msg2DD = _key_message_DD(msg2, _keyword)
    
    out_file.write("keyed msg0B: "+keyed_msg0B+"\n")
    out_file.write("keyed msg0BA: "+keyed_msg0BA+"\n")
    out_file.write("keyed msg0BB: "+keyed_msg0BB+"\n")
    out_file.write("keyed msg0DA: "+keyed_msg0DA+"\n")
    out_file.write("keyed msg0DB: "+keyed_msg0DB+"\n")
    out_file.write("keyed msg0DD: "+keyed_msg0DD+"\n")
    
    out_file.write("keyed msg1B: "+keyed_msg1B+"\n")
    out_file.write("keyed msg1BA: "+keyed_msg1BA+"\n")
    out_file.write("keyed msg1BB: "+keyed_msg1BB+"\n")
    out_file.write("keyed msg1DA: "+keyed_msg1DA+"\n")
    out_file.write("keyed msg1DB: "+keyed_msg1DB+"\n")
    out_file.write("keyed msg1DD: "+keyed_msg1DD+"\n")
    
    out_file.write("keyed msg2B: "+keyed_msg2B+"\n")
    out_file.write("keyed msg2BA: "+keyed_msg2BA+"\n")
    out_file.write("keyed msg2BB: "+keyed_msg2BB+"\n")
    out_file.write("keyed msg2DA: "+keyed_msg2DA+"\n")
    out_file.write("keyed msg2DB: "+keyed_msg2DB+"\n")
    out_file.write("keyed msg2DD: "+keyed_msg2DD+"\n")

    path0 = _path_shift(list(alphabet_list), msg0)
    #print("path0: ", path0+"\n")
    path1 = _path_shift(list(alphabet_list), msg1)
    #print("path1: ", path1+"\n")
    path2 = _path_shift(list(alphabet_list), msg2)
    #print("path2: ", path2+"\n")
    out_file.write("path0: "+path0+"\n")
    out_file.write("path1: "+path1+"\n")
    out_file.write("path2: "+path2+"\n")
    double_msg0 = _double_func_add(list(alphabet_list), msg0)
    #print("double + ", double_msg0+"\n")
    double_msg1 = _double_func_sub(list(alphabet_list), msg1)
    #print("double - ", double_msg1+"\n")
    out_file.write("double + "+double_msg0+"\n")
    out_file.write("double - "+double_msg1+"\n")
    hebewD, hebewB, hebewA = _hebew_transformation(list(alphabet_list), msg0)
    #print("Hebew Delta", hebewD+"\n")
    #print("Hebew Transformations", hebewB, hebewA+"\n")
    out_file.write("Hebew Delta "+hebewD+"\n")
    out_file.write("Hebew Transformations (Beta Alpha)"+hebewB+" "+hebewA+"\n")
    betelD, betelB, betelA = _betel_transformation(list(alphabet_list), msg0)
    #print("Betel Delta", betelD)
    #print("Betel Transformations", betelB, betelA)
    out_file.write("Betel Delta "+betelD+"\n")
    out_file.write("Betel Transformations (Beta Alpha)"+betelB+" "+betelA+"\n")
    betelHeqetVenusD, betelHeqetVenusT, betelHeqetVenusB, betelHeqetVenusA = _betel_heqet_venus_transformation(list(alphabet_list), _keyword)
    #print("Betel Heqet Venus Delta", betelHeqetVenusD)
    #print("Betel Heqet Venus T", betelHeqetVenusT)
    #print("Betel Heqet Venus Transformations", betelHeqetVenusB, betelHeqetVenusA)
    out_file.write("Betel Heqet Venus Delta "+betelHeqetVenusD+"\n")
    out_file.write("Betel Heqet Venus T "+betelHeqetVenusT+"\n")
    out_file.write("Betel Transformations (Beta Alpha)"+betelHeqetVenusB+" "+betelHeqetVenusA+"\n")

_run()
