import re
import sys

object_mentions = []


def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


path = sys.argv[1]

model_file = open(path, 'r')

model = []
intro = []
ignore = 0
source = model_file.readlines()
for line in source:
    ignoreText = re.findall(r'\\\\ignore', line)
    if len(ignoreText) > 0:
        if ignore == 0:
            ignore = 1
            continue
        elif ignore == 1:
            ignore = 0
            continue
    if ignore == 0:
        model.append(line)
    elif ignore == 1:
        intro.append(line)


for x in model:
    result = re.findall(r'[a-zA-Zа-яА-Я]+_[a-zA-Zа-яА-Я]+', x)
#    result = re.findall(r'\S*_\S*', x)
    if len(result) > 0:
        for item in result:
            object_mentions.append(item)


objects = unique(object_mentions)
objects.sort()

d = dict.fromkeys(objects, "Not Defined")


for x in model:
    for item in d:
        if x.find(item+" {") != -1:
            d[item] = "Defined"


for item in d:
    SearchForDef = False
    typeDef = []
    leftBrackets = 0
    rightBrackets = 0

    for x in model:
        if SearchForDef == True:
            if (leftBrackets == rightBrackets):
                if x.find("}") != -1:
                    SearchForDef = False
                else:
                    if x != '\n':
                        typeDef.append(x)

            if x.find("{") != -1:
                leftBrackets = leftBrackets + 1

            if x.find("}") != -1:
                rightBrackets = rightBrackets + 1

        if x.find(item+" {") != -1:
            SearchForDef = True

    allTypes = []
    if (len(typeDef) > 0):
        print(item)
        for string in typeDef:
            result = re.findall(r'[a-zA-Zа-яА-Я]+_[a-zA-Zа-яА-Я]+', string)
            if len(result) > 0:
                for item in result:
                    allTypes.append(item)
        uniqueTypes = unique(allTypes)
        uniqueTypes.sort()
        if len(uniqueTypes) > 0:
              for item in uniqueTypes:
                  if d[item] == "Defined":
                      print('\t' + '+ ' + str(item))
                  if d[item] == "Not Defined":
                      print('\t' + '- ' + str(item))


print('\n')


types_all = []
for item, val in d.items():
    type = str(item).split("_")[0]
    types_all.append(type)
types = unique(types_all)

print('Used types:')
for item in types:
    print('\t' + str(item))

print('\n')


print('Defined objectes:')

for item, val in d.items():
    if val == "Defined":
        print('\t' + str(item))
print('\n')

print('Undefined objectes:')

for item, val in d.items():
    if val == "Not Defined":
        print('\t' + str(item))
