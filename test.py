import xml.etree.ElementTree as ET
def parsedocs(file1, file2):
    global EditScript
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()

def calc_update(node, node1):
    weight_att = 0.1
    weight_text = 0.4
    weight_tag = 0.5
    weight_structure = 0

    if node.tag == node1.tag:
        weight_tag = weight_tag * 0

    if node.attrib == node1.attrib:
        weight_att = weight_att * 0

    if node.text == node1.text:
        weight_text = weight_text * 0
    # Retrieve number of children under each node to be compared
    countChild1 = degree2(node, "")
    countChild2 = degree2(node1, "")
    if countChild1 == countChild2:
        weight_structure = weight_structure * 0
    # If there is a difference, we compute the difference in the number of children
    # The weight structure will be the computed difference
    else:
        if countChild1 > countChild2:
            temp = countChild1 - countChild2
        else:
            temp = countChild2 - countChild1
        weight_structure = temp
    # Sum the differences and return it
    sum_weights = weight_structure + weight_att + weight_tag + weight_text

    return sum_weights
def degree2(node, index):
    children = []
    count = 1
    if index == "":
        for child in node:
            count = count + degree2(child, "")
    else:
        for child in node:
            children.append(child)
        for child in children[index-1]:
            count = count + degree2(child, "")
    return count
parsedocs("file.xml", "file2.xml")