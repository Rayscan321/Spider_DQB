function encrypt(a, b) {
    if (b == null || b.length <= 0) {
        console.log("key cannot be empty");
        return null
    }
    var c = "";
    for (var i = 0; i < b.length; i++) {
        c += b.charCodeAt(i).toString()
    }
    var d = Math.floor(c.length / 5);
    var e = parseInt(c.charAt(d) + c.charAt(d * 2) + c.charAt(d * 3) + c.charAt(d * 4) + c.charAt(d * 5));
    var f = Math.ceil(b.length / 2);
    var g = Math.pow(2, 31) - 1;
    if (e < 2) {
        console.log("plesae change the key");
        return null
    }
    var h = Math.round(Math.random() * 1000000000) % 100000000;
    c += h;
    while (c.length > 10) {
        c = (parseInt(c.substring(0, 10)) + parseInt(c.substring(10, c.length))).toString()
    }
    c = (e * c + f) % g;
    var j = "";
    var k = "";
    for (var i = 0; i < a.length; i++) {
        j = parseInt(a.charCodeAt(i) ^ Math.floor((c / g) * 255));
        if (j < 16) {
            k += "0" + j.toString(16)
        } else
            k += j.toString(16);
        c = (e * c + f) % g
    }
    h = h.toString(16);
    while (h.length < 8)
        h = "0" + h;
    k += h;
    return k
}

function get_passname(oPass) {
    return encrypt(oPass, '27cab4a69ce48de0abf4936676a2154c')
}

console.log(get_passname('12345678'))
