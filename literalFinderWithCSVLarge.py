from cmath import inf
import os
import editdistance
import pickle

def checkKeywordSpecialChar(token):
    '''
        gives a boolean response true if the token is a keyword or special character
    '''
    keywords = ["select","from","where","and","or","not","sum","count","max","min","avg","between","order","group",\
        "by","natural","join","eoq"]
    specialCharacters = ["=", "*", "<", ">", ".", ",", "(", ")"]
    token = token.lower()
    if (token in keywords) or (token in specialCharacters):
        return True
    else:
        return False


def rightMostNonLiteral(token, startIndex, translatedOutput):
    '''
        gives right most non literal after the token in the translated output
    '''
    endIndex = startIndex
    while (endIndex<len(translatedOutput)) and (not checkKeywordSpecialChar(translatedOutput[endIndex])):
        endIndex+=1  
    
    return endIndex


def phoneticRepresentation(token):
    '''
        gives the phonetic representation of the token
    '''
    pass


def enumerateStrings(startIndex, endIndex, translatedOutput):
    '''
        enumerates all possible strings between startIndex and endIndex
    '''
    A = []
    positions = []
    i = startIndex
    windowSize = endIndex - startIndex

    while(i<endIndex):

        j = i
        k = 0
        currentString = ""

        while (j<endIndex) and (k<windowSize) and (not checkKeywordSpecialChar(translatedOutput[j])):
            currentString = currentString + translatedOutput[j]
            # A.append(phoneticRepresentation(currentString))
            # slight variation from original pseudocode since phonetic representations are not available
            A.append(currentString)
            positions.append(j)
            j+=1
            k+=1
        
        i+=1
    
    return A, positions


def retrieveCategory(token):
    '''
        gives the set of all possible literals corresponding to the category of the token.
        the token categories are tableName, attributeName, attributeValue
    '''
    # generate the dictionary below from an actual database
    
    file = open('data-large.pkl', 'rb')
    data = pickle.load(file)
    file.close()

    output=list(data[token])
    output.sort()
    return output


def editDistance(a,b):
    '''
        gives the edit distance between tokens a and b
    '''
    return editdistance.eval(a.lower(), b.lower())


def literalAssignment(A, B, positions):
    '''
        assigns a literal based on edit distance
    '''
    count={}
    location={}
    for b in B:
        count[b] = 0
        location[b] = -1

    for aIndex in range(len(A)):
        a = A[aIndex]
        possibleLiterals = []
        minEditDistance = inf

        for b in B:
            if editDistance(a,b) < minEditDistance:
                possibleLiterals = []
                possibleLiterals.append(b)
                minEditDistance = editDistance(a,b)
            elif editDistance(a,b) == minEditDistance:
                possibleLiterals.append(b)

        for b in possibleLiterals:
            count[b] += 1
            location[b] = max(location[b], positions[aIndex])

    maxCountLiteral=None
    maxCount = -1
    for b in B:
        if count[b] > maxCount:
            maxCount = count[b]
            maxCountLiteral = b
    position = location[maxCountLiteral]
    return maxCountLiteral, position


def literalFinder(translatedOutput, bestStructure):
    '''
        transalatedOutput : list of individual tokens from the translated ASR output
        bestStructure : list of individual tokens from the best structure given by structure determination
    '''
    # eoq - end of query
    translatedOutput.append("eoq")
    idx = 0
    finalOutput = []
    seenBY = False
    while(idx < len(translatedOutput)):
        token = translatedOutput[idx]
        if not checkKeywordSpecialChar(token):
            startIndex = idx
            endIndex = rightMostNonLiteral(token, startIndex, translatedOutput)
            A, positions = enumerateStrings(startIndex, endIndex, translatedOutput)

            if (translatedOutput[idx-1].lower() == "=" and translatedOutput[idx+1].lower() != ".") or \
                (translatedOutput[idx-1].lower() == "<" and translatedOutput[idx+1].lower() != ".") or \
                (translatedOutput[idx-1].lower() == ">" and translatedOutput[idx+1].lower() != ".") or \
                (translatedOutput[idx-1].lower() == "between") or \
                (translatedOutput[idx-1].lower() == "and" and translatedOutput[idx-3].lower() == "between"):
                
                B = retrieveCategory("attributeValue")

            elif (translatedOutput[idx-1].lower() == "select") or (translatedOutput[idx-1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "where" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == "and" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == "or" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == "not" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == "(" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == ")" and translatedOutput[idx+1].lower() != ".") or \
            (translatedOutput[idx-1].lower() == "by" and translatedOutput[idx+1].lower() != "."):

                B = retrieveCategory("attributeName")

            elif (translatedOutput[idx-1].lower() == "from") or (translatedOutput[idx-1].lower() == "join") or \
            (translatedOutput[idx-1].lower() == "," and (not seenBY)) or \
            (translatedOutput[idx-1].lower() == "," and seenBY and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "where" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "and" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "or" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "not" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "=" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "<" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == ">" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "(" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == ")" and translatedOutput[idx+1].lower() == ".") or \
            (translatedOutput[idx-1].lower() == "by" and translatedOutput[idx+1].lower() == "."):
                
                B = retrieveCategory("tableName")

            literal, position = literalAssignment(A, B, positions)
            finalOutput.append(literal)
            idx = position + 1
        else:
            idx+=1
            finalOutput.append(token)
            if token.lower()=="by":
                seenBY = True
    
    return finalOutput

space = " "

print("eoq is End-of-Query Marker")
print("-"*20)

# Example 1
translatedOutput = ["SELECT", "first", "name", "FROM", "Employers"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "x1", "FROM", "x2"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)

# Example 2
translatedOutput = ["SELECT", "first", "name", "FROM", "Employers", "WHERE", "first", "name", "=", "Pet"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "x1", "FROM", "x2", "WHERE", "x3", "=", "x4"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)

# Example 3
# commenting because salary attribute in Salaries table has numbers
# translatedOutput = ["SELECT", "last", "name", "FROM", "employers", ",", "slurry", "WHERE", "employers", ".", "id",\
#     "=", "slurry", ".", "employee_id", "AND", "slurry", ".", "solary", ">", "fiftee"]
# print("Input (ASR Transcription) :", space.join(translatedOutput))
# bestStructure = ["SELECT", "x1", "FROM", "x2", "WHERE", "x3", ".", "x4", "=", "x5", ".", "x6", "AND", "x7", ".", "x8",\
#     ">", "x9"]
# print("Input (Structure Determination) :", space.join(bestStructure))
# print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
# print("-"*20)

# Example 4
translatedOutput = ["SELECT", "SUM", "(", "solary", ")", "FROM", "slurry"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "SUM", "(", "x1", ")", "FROM", "x2"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)

# Example 5
translatedOutput = ["SELECT", "SUM", "(", "slurry", ".", "solary", ")", "FROM", "slurry"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "SUM", "(", "x1", ".", "x2", ")", "FROM", "x3"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)

# Example 6
# commenting because salary attribute in Salaries table has numbers
# translatedOutput = ["SELECT", "*", "FROM", "employers", ",", "slurry", "WHERE", "employers", ".", "id", "=", "slurry",\
#     ".", "employee_id", "AND", "slurry", ".", "solary", "BETWEEN", "thordee", "AND", "fortee"]
# print("Input (ASR Transcription) :", space.join(translatedOutput))
# bestStructure = ["SELECT", "*", "FROM", "x1", ",", "x2", "WHERE", "x3", ".", "x4", "=", "x5", "x6", "AND",\
#     "x7", ".", "x8", "BETWEEN", "x9", "AND", "x10"]
# print("Input (Structure Determination) :", space.join(bestStructure))
# print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
# print("-"*20)

# Example 7
translatedOutput = ["SELECT", "*", "FROM", "employers", ",", "slurry", "WHERE", "employers", ".", "employee_id", "=", "slurry",\
    ".", "employee_id", "ORDER", "BY", "slurry", ".", "solary", ",", "employers", ".", "employee_id"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "*", "FROM", "x1", ",", "x2", "WHERE", "x3", ".", "x4", "=", "x5", ".", "x6",\
    "ORDER", "BY", "x7", ".", "x8", ",", "x9", ".", "x10"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)

# Example 8
translatedOutput = ["SELECT", "*", "FROM", "employers", "NATURAL", "JOIN", "slurry"]
print("Input (ASR Transcription) :", space.join(translatedOutput))
bestStructure = ["SELECT", "*", "FROM", "x1", "NATURAL", "JOIN", "x2"]
print("Input (Structure Determination) :", space.join(bestStructure))
print("Output :", space.join(literalFinder(translatedOutput, bestStructure)))
print("-"*20)


# employees and salaries are actual table names

# [Limit, In]

# attribute name : preceding is {select,.}{where,and,or,not,(,),by(only when next is NOT .)}{,(seen BY and next is NOT .)}

# table name : preceding is {,(only when NOT seen BY)}{,(seen BY and next is .)}{from,join}
# {where,and,or,not,=,<,>,(,),by(only when next is .)}

# attribute value : preceding is {between}{=,<,>(only when next is NOT .)}}{and(only when preceding-2 is between)}