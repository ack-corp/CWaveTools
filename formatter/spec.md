Formater special C~ feature:

Ident 1 space (let anyone define the width).
var name / function name camelCase. (use fake display if any trouble with that)
class name UpperCamelCase.
const name SCREAMING_SNAKE_CASE.
bracket opening aways on a new line.
No line feed on single operation logic (if(...) function(arg...) function1().function2().function3()...). Let anyone define it as fake display;
No bracket on single line operation (even nested)
1 carriage return between each function / classes / include part and the rest. Let anyone define more with with a fake display.
No carriage return inside a function.
No carriage between function in header.
No carriage return between attribute in classes.
No carriage return between public private protected keywords in classes (let user fake it).
Function line count display FORCED (agressive display in case of more than a fixed limit (not configurable)) !


special feature.
Track heap allocated var, if one function call could be done with one heap allocated var, give a special color to that var. Try to track it perfectly.
Track unfree heap allocated var, give a special visual insight to it.