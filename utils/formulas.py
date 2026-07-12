def f1(numero: str) -> str:
    a = int(numero[0])
    b = int(numero[1])
    c = int(numero[2])
    d = int(numero[3])
    e = int(numero[4])
    f = int(numero[5])
    g = int(numero[6])
    h = int(numero[7])
    i = int(numero[8])
    j = int(numero[9])
    k = int(numero[10])
    l = int(numero[11])
    m = int(numero[12])
    n = int(numero[13])

    s1 = (a + b) % 10
    s2 = (c + d) % 10
    s3 = (e + f) % 10
    s4 = (g + h) % 10
    s5 = (i + j) % 10
    s6 = (k + l) % 10
    s7 = (m + n) % 10

    return f"{s1}{s2}{s3}{s4}{s5}{s6}{s7}{a}"


def f2(numero: str) -> str:
    a = int(numero[0])
    b = int(numero[1])
    c = int(numero[2])
    d = int(numero[3])
    e = int(numero[4])
    f = int(numero[5])
    g = int(numero[6])
    h = int(numero[7])
    i = int(numero[8])
    j = int(numero[9])
    k = int(numero[10])
    l = int(numero[11])
    m = int(numero[12])
    n = int(numero[13])
    o = int(numero[14])

    s1 = (b + c) % 10
    s2 = (d + e) % 10
    s3 = (f + g) % 10
    s4 = (h + i) % 10
    s5 = (j + k) % 10
    s6 = (l + m) % 10
    s7 = (n + o) % 10

    return f"{s1}{s2}{s3}{s4}{s5}{s6}{s7}{a}"


def f3(numero: str) -> str:
    a = int(numero[0])
    b = int(numero[1])
    c = int(numero[2])
    d = int(numero[3])
    e = int(numero[4])
    f = int(numero[5])
    g = int(numero[6])
    h = int(numero[7])
    i = int(numero[8])
    j = int(numero[9])
    k = int(numero[10])
    l = int(numero[11])
    m = int(numero[12])
    n = int(numero[13])
    o = int(numero[14])

    s1 = (a + b + c + d + e + f + g + h) % 10
    s2 = (b + c + d + e + f + g + h + i) % 10
    s3 = (c + d + e + f + g + h + i + j) % 10
    s4 = (d + e + f + g + h + i + j + k) % 10
    s5 = (e + f + g + h + i + j + k + l) % 10
    s6 = (f + g + h + i + j + k + l + m) % 10
    s7 = (g + h + i + j + k + l + m + n) % 10
    s8 = (h + i + j + k + l + m + n + o) % 10

    return f"{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}"