from cmath import inf
import os
import editdistance

def checkKeywordSpecialChar(token):
    '''
        gives a boolean response true if the token is a keyword or special character
    [Select, From, Where, Order By, Group By, Natural Join, And, Or, Not, Limit, Between, In, Sum, Count, Max, Avg, Min]
    [* = < > ( ) . ,]
    '''
    keywords = ["select","from","where"]
    specialCharacters = ["="]
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
    dic={}
    dic["tableName"] = ["Employees", "Salaries"]
    dic["attributeName"] = ["FirstName", "LastName"]
    dic["attributeValue"] = ["John", "Parth", "Shreyas", "Kritti"]

    return dic[token]


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
    idx = 0
    finalOutput = []
    while(idx < len(translatedOutput)):
        token = translatedOutput[idx]
        if not checkKeywordSpecialChar(token):
            startIndex = idx
            endIndex = rightMostNonLiteral(token, startIndex, translatedOutput)
            A, positions = enumerateStrings(startIndex, endIndex, translatedOutput)

            if (translatedOutput[idx-1].lower() == "select") or (translatedOutput[idx-1].lower() == "where"):
                B = retrieveCategory("attributeName")
            elif translatedOutput[idx-1].lower() == "from":
                B = retrieveCategory("tableName")
            elif translatedOutput[idx-1].lower() == "=":
                B = retrieveCategory("attributeValue")

            literal, position = literalAssignment(A, B, positions)
            finalOutput.append(literal)
            idx = position + 1
        else:
            idx+=1
            finalOutput.append(token)
    
    return finalOutput

# Example 1
translatedOutput = ["Select", "first", "name", "from", "Employers"]
bestStructure = ["Select", "x1", "from", "x2"]
print(literalFinder(translatedOutput, bestStructure))

# Example 2
translatedOutput = ["Select", "first", "name", "from", "Employers", "where", "first", "name", "=", "Jon"]
bestStructure = ["Select", "x1", "from", "x2", "where", "x3", "=", "x4"]
print(literalFinder(translatedOutput, bestStructure))