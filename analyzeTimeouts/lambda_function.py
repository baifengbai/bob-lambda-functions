import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()import traceback
import json
import boto3
import datetime
import time

from boto3.dynamodb.conditions import Key, Attr

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def displayTime(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def epochToTime(e):
    a = float(e) #last epoch recorded
    b = time.time() #current epoch time
    c = b - a #returns seconds
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60
    
    return (hours + minutes + seconds)

def lambda_handler(event, context):
    now = int(time.time())
    
    try:
        dynamodb = boto3.resource('dynamodb')
    
        table = dynamodb.Table('accounts')
        response = table.scan()
        data = response['Items']
    
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        accountCount = len(data)
        print('Number of accounts: ' + str(accountCount))

        i = 0
        
        while i < accountCount:
            accountId = data[i]['id']
            firstName = data[i]['firstName']
            lastName = data[i]['lastName']
            
            print('Currently Scanning: ' + firstName + ' ' + lastName + ' (' + accountId + ')')
            
            table = dynamodb.Table('actions')
            response = table.scan(FilterExpression=Attr('id').eq(accountId))
            #response = table.scan()
            
            actionData = response['Items']
        
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], FilterExpression=Attr('id').eq(accountId))
                actionData.extend(response['Items'])
            
            actionCount = len(actionData)
            print('Number of actions: ' + str(actionCount))
            
            latestTs = 0
            latestData = []
            latestDataIndex = 0
            latestTimeout = 0
            timeoutCollection =[]
            timeoutCount = 0
            longBeginCollection = []
            longEndCollection = []
            
            l = 0
            
            while (l < actionCount):
                if (actionData[l]['ts'] > latestTs):
                    #print('found greater value')
                    latestTs = actionData[l]['ts']
                    latestData = actionData[l]
                    latestDataIndex = l
                
                if (l != 0):
                    latestTimeout = (actionData[l]['ts'] - actionData[l - 1]['ts'])
                    timeout = actionData[l]['ts'] - actionData[l - 1]['ts']
                    
                    timeoutCollection.append(timeout)
                    
                    if timeout > 18000: #five hours
                        longBeginCollection.append(epochToTime(actionData[l - 1]['ts']))
                        longEndCollection.append(epochToTime(actionData[l]['ts']))
                    
                    timeoutCount = timeoutCount + 1
                    
                l = l + 1
                
            #print(latestData)
            print('Latest data index: ' + str(latestDataIndex))
            print('Latest full timeout: ' + str(latestTimeout))
            print('How long ago was a full timeout: ' + str(displayTime(now - latestTs)))
            print('Average timeout: ' + str(displayTime(sum(timeoutCollection)/timeoutCount)))
            
            if (len(longBeginCollection) != 0):
                print('Average wake up time: ' + str(datetime.timedelta(seconds=(sum(longBeginCollection)/len(longBeginCollection)))))
            #readab
            print("")
            print("")
            i = i + 1
    except Exception as e:
        traceback.print_exc()
