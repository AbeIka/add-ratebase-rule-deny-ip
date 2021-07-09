import boto3
import os

def lambda_handler(event, context):
    client = boto3.client('wafv2')

    try:
        # Get IP addresses blocked by rate-based rules
        responseAddips = client.get_rate_based_statement_managed_keys(
            Scope=os.environ['WEBACL_SCOPE'],
            WebACLName=os.environ['WEBACL_NAME'],
            WebACLId=os.environ['WEBACL_ID'],
            RuleName=os.environ['RATEBASERULE_NAME']
        )
        # Get the list of IPv4 blocked by rate-based rules
        responseAddips = responseAddips['ManagedKeysIPV4']['Addresses']

        # If there are no IPs blocked by the rate-based rule, exit
        if len(responseAddips) == 0:
            print("There are no IP addresses blocked by the rate-based rule")
            return()

        # The following will be executed when there are IPs blocked by the rate-based rule

        # Get an existing IP set.
        IPSets = client.get_ip_set(
            Name=os.environ['IPSETRULE_NAME'],
            Scope=os.environ['WEBACL_SCOPE'],
            Id=os.environ['IPSETRULE_ID']
            )        
        IPSets = IPSets['IPSet']['Addresses']
        
        # Show IPs blocked by rate-based rules
        print("The IPs detected by the rate-based rule are as follows")
        print(responseAddips)
        
        # Display the current IP Sets.
        print("The current IP Sets are as follows")
        print(IPSets)
        
        #  Create a list of IPs that are blocked by rate-based rules and are not registered in the IP Set 
        addIPList = list(set(responseAddips) - set(IPSets))
        # Remove duplicates from IP list
        addIPList=list(set(addIPList))
        
        # If the IP being blocked by the rate-based rule is already registered in IPSet, it will be terminated
        if len(addIPList) == 0:
            print("The IP blocked by the rate-based rule has already been registered in IPSet.Ends the process")
            return()

        # Display the IP address to be added
        for ip in addIPList:
            print("Add " + ip + " to the IP set ")

        # update_ip_set replaces the specified IP, so match the existing IP list with the IP list to be added.
        addIPList = IPSets + addIPList

        # Get a token to update the IP Set.
        responseToken = client.get_ip_set(
            Name='IPset',
            Scope='REGIONAL',
            Id=os.environ['IPSETRULE_ID']
            )
        Token = responseToken["LockToken"]
        
        # Update the IP Set
        response = client.update_ip_set(
            Name='IPset',
            Scope='REGIONAL',
            Id=os.environ['IPSETRULE_ID'],
            Addresses=addIPList,
            LockToken=Token
            )
        
        # Indicate that the IP set update is complete.
        print("Addition to the IP set is complete.")
        
    except:
        # exception handling
        print("An error has occurred")

    return()