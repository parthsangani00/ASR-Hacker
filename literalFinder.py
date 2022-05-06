from cmath import inf
import os
import editdistance

def checkKeywordSpecialChar(token):
    '''
        gives a boolean response true if the token is a keyword or special character
    '''
    pass


def rightMostNonLiteral(token, translatedOutput):
    '''
        gives right most non literal after the token in the translated output
    '''
    pass


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
    i = 0
    windowSize = endIndex - startIndex

    while(i<endIndex):
        j = i
        k = 0
        currentString = ""

        while (not checkKeywordSpecialChar(translatedOutput[j])) and (j<endIndex) and (k<windowSize):
            currentString = currentString + translatedOutput[j]
            A.append(phoneticRepresentation(currentString))
            positions.append(j)
            j+=1
            k+=1
        
        i+=1
    
    return A, positions


def retrieveCategory(token):
    '''
        gives the set of all possible literals corresponding to the category of the token.
        the token categories are table_name, attribute_name, attribute_value
    '''
    pass


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

    for a in A:
        possibleLiteralsIndex = []
        minEditDistance = inf

        for bIndex in range(len(B)):
            b = B[bIndex]
            if editDistance(a,b) < minEditDistance:
                possibleLiteralsIndex = []
                possibleLiteralsIndex.append(bIndex)
                minEditDistance = editDistance(a,b)
            elif editDistance(a,b) < minEditDistance:
                possibleLiteralsIndex.append(bIndex)
        
        for bIndex in possibleLiteralsIndex:
            b = B[bIndex]
            count[b] += 1
            location[b] = max(location[b], positions[bIndex])

    maxCountLiteral=None
    maxCount = -1
    for b in B:
        if count[b] > maxCount:
            maxCount = count[b]
            maxCountLiteral = b
    
    position = location[b]

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
            endIndex = rightMostNonLiteral(token, translatedOutput)
            A, positions = enumerateStrings(startIndex, endIndex, translatedOutput)
            B = retrieveCategory(token)
            literal, position = literalAssignment(A, B, positions)
            finalOutput.append(literal)
            idx = position + 1
        else:
            idx+=1
            finalOutput.append(token)
    
    return finalOutput

